from django import forms
from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["full_name", "line1", "line2", "city", "state", "postal_code", "country"]
