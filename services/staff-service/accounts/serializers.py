from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import InventoryActionLog, User


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "phone",
            "employee_code",
            "department",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["is_staff"] = True
        return User.objects.create_user(**validated_data)


class InventoryActionLogSerializer(serializers.ModelSerializer):
    staff_name = serializers.SerializerMethodField()

    class Meta:
        model = InventoryActionLog
        fields = [
            "id",
            "staff",
            "staff_name",
            "action_type",
            "target_service",
            "product_id",
            "product_name",
            "status",
            "request_payload",
            "response_payload",
            "created_at",
        ]

    def get_staff_name(self, obj):
        return f"{obj.staff.first_name} {obj.staff.last_name}"


class CustomTokenSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD

    def validate(self, attrs):
        data = super().validate(attrs)
        data["id"] = self.user.id
        data["email"] = self.user.email
        data["first_name"] = self.user.first_name
        data["last_name"] = self.user.last_name
        data["employee_code"] = self.user.employee_code
        data["role"] = "staff"
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["role"] = "staff"
        return token
