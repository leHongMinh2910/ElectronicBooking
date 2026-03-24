from django.db import models
from django.utils.text import slugify


class Laptop(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=120)
    slug = models.SlugField(max_length=255, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True)
    cpu = models.CharField(max_length=120)
    ram = models.CharField(max_length=60)
    storage = models.CharField(max_length=60)
    screen_size = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        base_slug = slugify(f"{self.brand}-{self.name}")
        self.slug = base_slug[:255] or "laptop"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.name}"
