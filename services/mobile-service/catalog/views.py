from django.db.models import Q
from rest_framework import generics

from .models import Mobile
from .serializers import MobileSerializer


class MobileListCreateView(generics.ListCreateAPIView):
    serializer_class = MobileSerializer

    def get_queryset(self):
        queryset = Mobile.objects.filter(is_active=True).order_by("-id")
        query = self.request.query_params.get("q", "").strip()
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(brand__icontains=query)
                | Q(chipset__icontains=query)
                | Q(ram__icontains=query)
                | Q(storage__icontains=query)
            )
        return queryset


class MobileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Mobile.objects.all()
    serializer_class = MobileSerializer
