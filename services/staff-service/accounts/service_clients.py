import requests
from django.conf import settings


def product_service_url(target_service, path):
    base_url = settings.LAPTOP_SERVICE_URL if target_service == "laptop" else settings.MOBILE_SERVICE_URL
    return f"{base_url}{path}"


def submit_to_product_service(method, url, **kwargs):
    try:
        response = requests.request(method, url, timeout=8, **kwargs)
        data = None
        if response.content:
            try:
                data = response.json()
            except ValueError:
                data = {"detail": response.text}
        return data, response.status_code
    except requests.RequestException as exc:
        return {"detail": str(exc)}, 502
