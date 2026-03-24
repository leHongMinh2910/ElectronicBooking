from django.urls import path

from .views import ImportItemView, InventoryActionListView, MeView, StaffListView, StaffRegisterView, UpdateItemView

urlpatterns = [
    path("staff/register/", StaffRegisterView.as_view(), name="staff-register"),
    path("staff/", StaffListView.as_view(), name="staff-list"),
    path("me/", MeView.as_view(), name="me"),
    path("items/import/", ImportItemView.as_view(), name="item-import"),
    path("items/update/<str:target_service>/<int:item_id>/", UpdateItemView.as_view(), name="item-update"),
    path("actions/", InventoryActionListView.as_view(), name="action-list"),
]
