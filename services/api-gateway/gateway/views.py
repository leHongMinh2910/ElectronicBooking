from decimal import Decimal

from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import AddToCartForm, LaptopItemForm, LoginForm, MobileItemForm, RegisterForm
from .service_clients import call_service, customer_url, fetch_products, product_url, staff_url


def _get_token(request):
    return request.session.get("access_token")


def _get_user(request):
    return request.session.get("user")


def _get_role(request):
    return request.session.get("role")


def _require_role(request, role):
    user = _get_user(request)
    return bool(user and _get_role(request) == role)


def _refresh_cart(request):
    user = _get_user(request)
    if not user or _get_role(request) != "customer":
        request.session["cart_count"] = 0
        return {"items": [], "item_count": 0, "total_amount": 0}
    payload, status_code = call_service(
        "GET",
        customer_url(f"/api/carts/{user['id']}/"),
        token=_get_token(request),
    )
    if status_code == 200 and payload:
        cart = payload.get("cart", {})
        request.session["cart_count"] = cart.get("item_count", 0)
        return cart
    request.session["cart_count"] = 0
    return {"items": [], "item_count": 0, "total_amount": 0}


def _get_item_form(target_service, *args, **kwargs):
    return LaptopItemForm(*args, **kwargs) if target_service == "laptop" else MobileItemForm(*args, **kwargs)


def _json_ready(value):
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, dict):
        return {key: _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    return value


def home(request):
    return render(request, "gateway/home.html", {"products": fetch_products()[:6]})


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        role = form.cleaned_data["role"]
        base = customer_url if role == "customer" else staff_url
        payload, status_code = call_service(
            "POST",
            base("/api/token/"),
            json={"email": form.cleaned_data["email"], "password": form.cleaned_data["password"]},
        )
        if status_code == 200 and payload:
            me_payload, me_status = call_service("GET", base("/api/me/"), token=payload.get("access"))
            if me_status == 200:
                request.session["access_token"] = payload.get("access")
                request.session["refresh_token"] = payload.get("refresh")
                request.session["user"] = me_payload
                request.session["role"] = role
                _refresh_cart(request)
                messages.success(request, "Dang nhap thanh cong.")
                return redirect("customer-dashboard" if role == "customer" else "staff-dashboard")
        messages.error(request, (payload or {}).get("detail", "Dang nhap that bai."))
    return render(request, "gateway/login.html", {"form": form})


def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        payload, status_code = call_service(
            "POST",
            customer_url("/api/customers/register/"),
            json=form.cleaned_data,
        )
        if status_code in (200, 201):
            messages.success(request, "Dang ky customer thanh cong. Hay dang nhap de tao gio hang.")
            return redirect("login")
        messages.error(request, str(payload))
    return render(request, "gateway/register.html", {"form": form})


def logout_view(request):
    request.session.flush()
    messages.info(request, "Ban da dang xuat.")
    return redirect("home")


def customer_dashboard(request):
    query = request.GET.get("q", "").strip()
    return render(
        request,
        "gateway/customer_dashboard.html",
        {
            "products": fetch_products(query),
            "query": query,
            "add_to_cart_form": AddToCartForm(),
        },
    )


def add_to_cart(request, target_service, product_id):
    if not _require_role(request, "customer"):
        messages.warning(request, "Chi customer moi duoc tao gio hang.")
        return redirect("login")
    form = AddToCartForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        product, status_code = call_service("GET", product_url(target_service, f"/api/items/{product_id}/"))
        if status_code != 200 or not product:
            messages.error(request, "Khong tim thay san pham.")
            return redirect("customer-dashboard")
        payload = {
            "product_service": target_service,
            "product_id": product["id"],
            "product_name": product["name"],
            "brand": product["brand"],
            "unit_price": str(product["price"]),
            "quantity": form.cleaned_data["quantity"],
            "image_url": product.get("image_url", ""),
        }
        _, add_status = call_service(
            "POST",
            customer_url(f"/api/carts/{_get_user(request)['id']}/items/"),
            token=_get_token(request),
            json=payload,
        )
        if add_status == 200:
            _refresh_cart(request)
            messages.success(request, "Da them vao gio hang.")
        else:
            messages.error(request, "Khong the them vao gio hang.")
    return redirect("customer-dashboard")


def cart_view(request):
    if not _require_role(request, "customer"):
        return redirect("login")
    return render(request, "gateway/cart.html", {"cart": _refresh_cart(request)})


def delete_cart_item(request, item_id):
    if not _require_role(request, "customer"):
        return redirect("login")
    if request.method == "POST":
        _, status_code = call_service(
            "DELETE",
            customer_url(f"/api/carts/{_get_user(request)['id']}/items/{item_id}/"),
            token=_get_token(request),
        )
        if status_code == 204:
            messages.success(request, "Da xoa khoi gio hang.")
        else:
            messages.error(request, "Khong the xoa san pham.")
        _refresh_cart(request)
    return redirect("cart")


def staff_dashboard(request):
    if not _require_role(request, "staff"):
        messages.warning(request, "Vui long dang nhap bang tai khoan staff.")
        return redirect("login")
    laptop_items, _ = call_service("GET", product_url("laptop", "/api/items/"))
    mobile_items, _ = call_service("GET", product_url("mobile", "/api/items/"))
    action_logs, _ = call_service("GET", staff_url("/api/actions/"), token=_get_token(request))
    laptop_items = laptop_items if isinstance(laptop_items, list) else []
    mobile_items = mobile_items if isinstance(mobile_items, list) else []
    action_logs = action_logs if isinstance(action_logs, list) else []
    return render(
        request,
        "gateway/staff_dashboard.html",
        {
            "laptop_items": laptop_items or [],
            "mobile_items": mobile_items or [],
            "action_logs": action_logs or [],
        },
    )


def create_item(request, target_service):
    if not _require_role(request, "staff"):
        return redirect("login")
    form = _get_item_form(target_service, request.POST or None)
    if request.method == "POST" and form.is_valid():
        payload, status_code = call_service(
            "POST",
            staff_url("/api/items/import/"),
            token=_get_token(request),
            json={"target_service": target_service, "item": _json_ready(form.cleaned_data)},
        )
        if status_code in (200, 201):
            messages.success(request, "Nhap item thanh cong.")
            return redirect("staff-dashboard")
        messages.error(request, str(payload))
    return render(
        request,
        "gateway/product_form.html",
        {"form": form, "target_service": target_service, "page_title": f"Them {target_service}"},
    )


def update_item(request, target_service, item_id):
    if not _require_role(request, "staff"):
        return redirect("login")
    item_payload, status_code = call_service("GET", product_url(target_service, f"/api/items/{item_id}/"))
    if status_code != 200 or not item_payload:
        messages.error(request, "Khong tim thay item can sua.")
        return redirect("staff-dashboard")
    form = _get_item_form(target_service, request.POST or None, initial=item_payload)
    if request.method == "POST" and form.is_valid():
        payload, update_status = call_service(
            "PUT",
            staff_url(f"/api/items/update/{target_service}/{item_id}/"),
            token=_get_token(request),
            json={"item": _json_ready(form.cleaned_data)},
        )
        if update_status == 200:
            messages.success(request, "Cap nhat item thanh cong.")
            return redirect("staff-dashboard")
        messages.error(request, str(payload))
    return render(
        request,
        "gateway/product_form.html",
        {"form": form, "target_service": target_service, "page_title": f"Cap nhat {target_service} #{item_id}"},
    )
