from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, first_name, last_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    employee_code = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100, default="Inventory")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "employee_code"]

    def __str__(self):
        return f"{self.employee_code} - {self.email}"


class InventoryActionLog(models.Model):
    ACTION_CHOICES = (
        ("import", "Import"),
        ("update", "Update"),
    )
    TARGET_CHOICES = (
        ("laptop", "Laptop"),
        ("mobile", "Mobile"),
    )

    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inventory_actions")
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    target_service = models.CharField(max_length=20, choices=TARGET_CHOICES)
    product_id = models.IntegerField(null=True, blank=True)
    product_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="success")
    request_payload = models.JSONField(default=dict, blank=True)
    response_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
