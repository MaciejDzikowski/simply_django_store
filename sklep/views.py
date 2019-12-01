from django.shortcuts import render
from .models import Product

# Create your views here.


def home(request):
    return render(
        request,
        "sklep/home.html"
    )


def index(request, tekst):
    return render(
        request,
        "sklep/glowna.html",
        {"imie_klienta": tekst}
    )


def products_list(request):
    products = Product.objects.order_by("id")
    context = {"products": products}
    return render(
        request,
        "sklep/list.html",
        context
    )


def product_properties(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {"product": product}
    return render(
        request,
        "sklep/properties.html",
        context
    )
