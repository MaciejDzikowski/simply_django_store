from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    description = models.CharField(default="brak opisu", max_length=500)
    weight = models.FloatField(default=0)
    author = models.CharField(default="NN", max_length=100)

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    possibilities = [("l", "list"), ("p", "paczka"), ("k", "kurier")]
    shipment = models.CharField(max_length=1, choices=possibilities)

    def __str__(self):
        full_name = self.name + " " + self.surname
        return full_name
