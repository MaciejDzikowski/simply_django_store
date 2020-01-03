from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    description = models.CharField(default="brak opisu", max_length=500)
    weight = models.FloatField(default=0)
    author = models.CharField(default="NN", max_length=100)
    product_ratings = models.ManyToManyField(
        "Rating",
        through="ProductRating"
    )

    def __str__(self):
        return self.name

    def get_rating(self):
        amount = 0
        ratings_sum = 0
        product_ratings = ProductRating.objects.filter(product_id=self)
        if product_ratings:
            for product_rating in product_ratings:
                amount += 1
                ratings_sum += product_rating.rating.rating
            return ratings_sum / amount
        else:
            return "Brak ocen"

    def get_comments(self):
        comments = []
        product_ratings = ProductRating.objects.filter(product_id=self)
        if product_ratings:
            for product_rating in product_ratings:
                comments.append(product_rating.rating.comment)
            return comments


class DiscountCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )

    def __str__(self):
        code = self.code
        return code


class Order(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    possibilities = [("l", "list"), ("p", "paczka"), ("k", "kurier")]
    delivery = models.CharField(max_length=1, choices=possibilities)
    discount_code = models.CharField(max_length=100, blank=True, null=True)
    used_code = models.ForeignKey(DiscountCode, on_delete=models.CASCADE,
                                  blank=True, null=True)
    ordered_products = models.ManyToManyField(
        "Product",
        through="OrderedProduct"
    )

    def __str__(self):
        full_name = self.name + " " + self.surname
        return full_name

    def get_total_price(self):
        total = 0
        used_code = self.used_code
        ordered_products = OrderedProduct.objects.filter(order=self)

        if used_code:
            for ordered_product in ordered_products:
                total += ordered_product.amount \
                         * ordered_product.product.price \
                         * (1 - used_code.discount)
        else:
            for ordered_product in ordered_products:
                total += ordered_product.amount * ordered_product.product.price
        return total

    def get_ordered_products(self):
        ordered_products_names = []
        ordered_products = OrderedProduct.objects.filter(order=self)
        for ordered_product in ordered_products:
            ordered_products_names.append((ordered_product.product.name,
                                           ordered_product.amount))
        return ordered_products_names


class OrderedProduct(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(default=1)

    def __str__(self):
        name = self.product.name + " x " + str(self.amount)
        return name


class Complaint(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=200)
    message = models.CharField(max_length=2000)

    def __str__(self):
        full_name = self.name + " " + self.surname
        return full_name


class Rating(models.Model):
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 11)]
    )
    comment = models.CharField(max_length=1000)

    def __str__(self):
        name = "Comment no. " + str(self.id)
        return name


class ProductRating(models.Model):
    rating = models.ForeignKey(
        Rating,
        on_delete=models.PROTECT
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
