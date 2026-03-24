from django.db.models import Q
from rest_framework import generics

from .models import Laptop
from .serializers import LaptopSerializer


class LaptopListCreateView(generics.ListCreateAPIView):
    serializer_class = LaptopSerializer

    def get_queryset(self):
        queryset = Laptop.objects.filter(is_active=True).order_by("-id")
        query = self.request.query_params.get("q", "").strip()
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(brand__icontains=query)
                | Q(cpu__icontains=query)
                | Q(ram__icontains=query)
                | Q(storage__icontains=query)
            )
        return queryset


class LaptopDetailView(generics.RetrieveUpdateAPIView):
    queryset = Laptop.objects.all()
    serializer_class = LaptopSerializer
