from django import forms


class LoginForm(forms.Form):
    role = forms.ChoiceField(
        choices=[("customer", "Customer"), ("staff", "Staff")],
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}))


class RegisterForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={"class": "form-control", "style": "max-width: 88px;"}))


class BaseItemForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    brand = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}))
    stock = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))
    image_url = forms.URLField(required=False, widget=forms.URLInput(attrs={"class": "form-control", "placeholder": "https://..."}))


class LaptopItemForm(BaseItemForm):
    cpu = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    ram = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "16GB"}))
    storage = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "512GB SSD"}))
    screen_size = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "15.6 inches"}))


class MobileItemForm(BaseItemForm):
    chipset = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    ram = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "12GB"}))
    storage = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "256GB"}))
    battery = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "5000mAh"}))
