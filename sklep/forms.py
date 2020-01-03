from django.forms import ModelForm
from .models import Order, Complaint, Rating


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["name", "surname", "address", "delivery", "discount_code"]


class ComplaintForm(ModelForm):
    class Meta:
        model = Complaint
        fields = ["name", "surname", "message"]


class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ["rating", "comment"]
