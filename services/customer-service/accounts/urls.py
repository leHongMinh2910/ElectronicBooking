from django.urls import path

from .views import AddCartItemView, CartDetailView, CustomerListView, CustomerRegisterView, DeleteCartItemView, MeView

urlpatterns = [
    path("customers/register/", CustomerRegisterView.as_view(), name="customer-register"),
    path("customers/", CustomerListView.as_view(), name="customer-list"),
    path("me/", MeView.as_view(), name="me"),
    path("carts/<int:customer_id>/", CartDetailView.as_view(), name="cart-detail"),
    path("carts/<int:customer_id>/items/", AddCartItemView.as_view(), name="cart-add-item"),
    path("carts/<int:customer_id>/items/<int:item_id>/", DeleteCartItemView.as_view(), name="cart-delete-item"),
]
