from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("customer/", views.customer_dashboard, name="customer-dashboard"),
    path("cart/", views.cart_view, name="cart"),
    path("products/<str:target_service>/<int:product_id>/add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path("cart/items/<int:item_id>/delete/", views.delete_cart_item, name="delete-cart-item"),
    path("staff/", views.staff_dashboard, name="staff-dashboard"),
    path("staff/<str:target_service>/create/", views.create_item, name="create-item"),
    path("staff/<str:target_service>/<int:item_id>/edit/", views.update_item, name="update-item"),
]
