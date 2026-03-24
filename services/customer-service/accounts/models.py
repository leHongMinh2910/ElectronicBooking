from decimal import Decimal

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
    address = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email


class Cart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_amount(self):
        return round(sum(item.subtotal for item in self.items.all()), 2)

    @property
    def item_count(self):
        return self.items.count()


class CartItem(models.Model):
    SERVICE_CHOICES = (
        ("laptop", "Laptop"),
        ("mobile", "Mobile"),
    )

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product_service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=120)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    image_url = models.URLField(blank=True)

    class Meta:
        unique_together = ("cart", "product_service", "product_id")

    def save(self, *args, **kwargs):
        self.subtotal = Decimal(self.unit_price) * self.quantity
        super().save(*args, **kwargs)
