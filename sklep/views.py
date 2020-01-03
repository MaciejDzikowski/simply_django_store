from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from .models import Product, Order, Complaint, OrderedProduct, DiscountCode
from .models import Rating, ProductRating
from .forms import OrderForm, ComplaintForm, RatingForm


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
    form = RatingForm()
    context = {"product": product, "form": form}
    return render(
        request,
        "sklep/properties.html",
        context
    )


def order_details(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    names_list = order.get_ordered_products()
    total_price = order.get_total_price()
    context = {"names": names_list, "price": total_price}
    return render(request, "sklep/order_detalis.html", context)


def order(request):
    products_to_order = _get_products_in_cart(request)
    discount_codes = DiscountCode.objects.order_by("code")
    codes = [i.code for i in discount_codes]

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["discount_code"] in codes:
                order = Order(
                    name=form.cleaned_data["name"],
                    surname=form.cleaned_data["surname"],
                    address=form.cleaned_data["address"],
                    delivery=form.cleaned_data["delivery"],
                    discount_code=form.cleaned_data["discount_code"],
                    used_code=discount_codes[codes.index(form.cleaned_data
                                                         ["discount_code"])]
                )
                order.save()
            else:
                order = Order(
                    name=form.cleaned_data["name"],
                    surname=form.cleaned_data["surname"],
                    address=form.cleaned_data["address"],
                    delivery=form.cleaned_data["delivery"],
                    discount_code=form.cleaned_data["discount_code"]

                )
                order.save()

            # dodajemy wszystkie produkty z koszyka do zamowienia
            for product in products_to_order:
                OrderedProduct(
                    product=product,
                    order=order,
                    amount=products_to_order[product]
                ).save()
            return HttpResponseRedirect("/order/" + str(order.id))
    else:
        form = OrderForm()
    return render(request, "sklep/order_form.html",
                  {"form": form, "products": products_to_order})


def complaint(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = Complaint(
                name=form.cleaned_data["name"],
                surname=form.cleaned_data["surname"],
                message=form.cleaned_data["message"],
            )
            complaint.save()
            return HttpResponseRedirect("/complaint/" + str(complaint.id))
    else:
        form = ComplaintForm()
    return render(request, "sklep/complaint_form.html", {"form": form})


def complaint_details(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    context = {"complaint": complaint}
    return render(request, "sklep/complaint_detalis.html", context)


def add_to_cart(request):
    if request.method == "POST":
        if "cart" not in request.session:
            request.session["cart"] = []
        for i in range(int(request.POST["number"])):
            request.session["cart"].append(request.POST["item_id"])
            request.session.modified = True
    return HttpResponseRedirect("/cart")


def remove_from_cart(request):
    if request.method == "POST":
        for i in range(int(request.POST["number"])):
            try:
                request.session["cart"].remove(request.POST["item_id"])
            except:
                break
            request.session.modified = True
    return HttpResponseRedirect("/cart")


def _get_products_in_cart(request):
    products_in_cart = {}
    for item_id in request.session.get("cart", []):
        product = Product.objects.get(pk=item_id)
        if product not in products_in_cart:
            products_in_cart[product] = 1
        else:
            products_in_cart[product] += 1
    return products_in_cart


def cart(request):
    products_in_cart = _get_products_in_cart(request)
    return render(request, "sklep/cart.html", {"products": products_in_cart})


def rate(request):
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = Rating(
                rating=form.cleaned_data["rating"],
                comment=form.cleaned_data["comment"]
            ).save()
            ProductRating(
                rating=rating,
                product=Product.objects.get(id=int(request.POST["item_id"]))
            ).save()
            return HttpResponseRedirect("/products/"
                                        + str(request.POST["item_id"]))
