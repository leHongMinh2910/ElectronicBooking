from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import InventoryActionLog, User
from .serializers import CustomTokenSerializer, InventoryActionLogSerializer, StaffSerializer

from .service_clients import product_service_url, submit_to_product_service


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


class StaffRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = StaffSerializer


class StaffListView(generics.ListAPIView):
    queryset = User.objects.all().order_by("id")
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticated]


class MeView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StaffSerializer

    def get_object(self):
        return self.request.user


class InventoryActionListView(generics.ListAPIView):
    serializer_class = InventoryActionLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InventoryActionLog.objects.select_related("staff").order_by("-created_at")


class ImportItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        target_service = request.data.get("target_service")
        item_data = request.data.get("item", {})
        if target_service not in ("laptop", "mobile"):
            return Response({"detail": "target_service must be laptop or mobile"}, status=status.HTTP_400_BAD_REQUEST)

        payload, status_code = submit_to_product_service("POST", product_service_url(target_service, "/api/items/"), json=item_data)
        InventoryActionLog.objects.create(
            staff=request.user,
            action_type="import",
            target_service=target_service,
            product_id=(payload or {}).get("id"),
            product_name=item_data.get("name", ""),
            status="success" if status_code in (200, 201) else "failed",
            request_payload=item_data,
            response_payload=payload or {},
        )
        return Response(payload, status=status_code)


class UpdateItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, target_service, item_id):
        if target_service not in ("laptop", "mobile"):
            return Response({"detail": "target_service must be laptop or mobile"}, status=status.HTTP_400_BAD_REQUEST)

        item_data = request.data.get("item", {})
        payload, status_code = submit_to_product_service(
            "PUT",
            product_service_url(target_service, f"/api/items/{item_id}/"),
            json=item_data,
        )
        InventoryActionLog.objects.create(
            staff=request.user,
            action_type="update",
            target_service=target_service,
            product_id=item_id,
            product_name=item_data.get("name", ""),
            status="success" if status_code in (200, 201) else "failed",
            request_payload=item_data,
            response_payload=payload or {},
        )
        return Response(payload, status=status_code)
