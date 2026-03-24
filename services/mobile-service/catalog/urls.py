from django.urls import path

from .views import MobileDetailView, MobileListCreateView

urlpatterns = [
    path("items/", MobileListCreateView.as_view(), name="mobile-list-create"),
    path("items/<int:pk>/", MobileDetailView.as_view(), name="mobile-detail"),
]
