from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Cart, CartItem, User
from .serializers import CartSerializer, CustomTokenSerializer, CustomerSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


class CustomerRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerSerializer


class CustomerListView(generics.ListAPIView):
    queryset = User.objects.all().order_by("id")
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class MeView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomerSerializer

    def get_object(self):
        return self.request.user


class CartDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, customer_id):
        if request.user.id != customer_id:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        cart, _ = Cart.objects.get_or_create(customer=request.user)
        return Response({"cart": CartSerializer(cart).data})


class AddCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, customer_id):
        if request.user.id != customer_id:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        cart, _ = Cart.objects.get_or_create(customer=request.user)
        required_fields = ["product_service", "product_id", "product_name", "brand", "unit_price", "quantity"]
        missing = [field for field in required_fields if field not in request.data]
        if missing:
            return Response({"detail": f"Missing fields: {', '.join(missing)}"}, status=status.HTTP_400_BAD_REQUEST)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_service=request.data["product_service"],
            product_id=request.data["product_id"],
            defaults={
                "product_name": request.data["product_name"],
                "brand": request.data["brand"],
                "unit_price": request.data["unit_price"],
                "quantity": request.data["quantity"],
                "image_url": request.data.get("image_url", ""),
            },
        )
        if not created:
            item.quantity += int(request.data["quantity"])
            item.product_name = request.data["product_name"]
            item.brand = request.data["brand"]
            item.unit_price = request.data["unit_price"]
            item.image_url = request.data.get("image_url", item.image_url)
        item.save()
        return Response({"cart": CartSerializer(cart).data})


class DeleteCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, customer_id, item_id):
        if request.user.id != customer_id:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        cart, _ = Cart.objects.get_or_create(customer=request.user)
        deleted, _ = cart.items.filter(id=item_id).delete()
        if not deleted:
            return Response({"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
