from django.core.management.base import BaseCommand

from accounts.models import User


class Command(BaseCommand):
    help = "Seed a demo staff account for the electronics microservice demo."

    def handle(self, *args, **options):
        if User.objects.filter(email="staff@electrohub.local").exists():
            self.stdout.write(self.style.WARNING("Demo staff account already exists"))
            return

        User.objects.create_user(
            email="staff@electrohub.local",
            first_name="Demo",
            last_name="Staff",
            password="staff123",
            phone="0123456789",
            employee_code="STF001",
            department="Inventory",
            is_staff=True,
        )
        self.stdout.write(self.style.SUCCESS("Created demo staff account staff@electrohub.local / staff123"))
