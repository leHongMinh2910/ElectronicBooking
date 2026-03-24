import requests
from django.conf import settings


def call_service(method, url, token=None, **kwargs):
    headers = kwargs.pop("headers", {})
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = requests.request(method, url, headers=headers, timeout=8, **kwargs)
        data = None
        if response.content:
            try:
                data = response.json()
            except ValueError:
                data = {"detail": response.text}
        if response.status_code >= 400:
            return data or {"detail": response.text}, response.status_code
        return data, response.status_code
    except requests.RequestException as exc:
        return {"detail": str(exc)}, 502


def customer_url(path):
    return f"{settings.CUSTOMER_SERVICE_URL}{path}"


def staff_url(path):
    return f"{settings.STAFF_SERVICE_URL}{path}"


def product_url(target_service, path):
    base_url = settings.LAPTOP_SERVICE_URL if target_service == "laptop" else settings.MOBILE_SERVICE_URL
    return f"{base_url}{path}"


def fetch_products(query=""):
    suffix = f"?q={query}" if query else ""
    laptops, _ = call_service("GET", product_url("laptop", f"/api/items/{suffix}"))
    mobiles, _ = call_service("GET", product_url("mobile", f"/api/items/{suffix}"))
    laptops = laptops if isinstance(laptops, list) else []
    mobiles = mobiles if isinstance(mobiles, list) else []
    products = []
    for item in laptops or []:
        products.append({**item, "service": "laptop", "service_label": "Laptop"})
    for item in mobiles or []:
        products.append({**item, "service": "mobile", "service_label": "Mobile"})
    return sorted(products, key=lambda item: item.get("id", 0), reverse=True)
