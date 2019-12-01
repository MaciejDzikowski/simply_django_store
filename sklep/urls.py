from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("widok/<str:tekst>", views.index),
    path("products/", views.products_list),
    path("products/<int:product_id>", views.product_properties)
]
