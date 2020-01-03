from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("widok/<str:tekst>", views.index),
    path("products/", views.products_list),
    path("products/<int:product_id>", views.product_properties),
    path("order/<int:order_id>", views.order_details),
    path("order/", views.order),
    path("complaint/<int:complaint_id>", views.complaint_details),
    path("complaint/", views.complaint),
    path("cart/", views.cart),
    path("cart/add/", views.add_to_cart),
    path("cart/remove/", views.remove_from_cart),
    path("products/rate/", views.rate)
]
