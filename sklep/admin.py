from django.contrib import admin
from .models import Product, Order, OrderedProduct, Complaint, DiscountCode
from .models import Rating, ProductRating

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderedProduct)
admin.site.register(Complaint)
admin.site.register(DiscountCode)
admin.site.register(Rating)
admin.site.register(ProductRating)
