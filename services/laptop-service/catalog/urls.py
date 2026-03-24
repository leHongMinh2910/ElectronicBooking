from django.urls import path

from .views import LaptopDetailView, LaptopListCreateView

urlpatterns = [
    path("items/", LaptopListCreateView.as_view(), name="laptop-list-create"),
    path("items/<int:pk>/", LaptopDetailView.as_view(), name="laptop-detail"),
]
