from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Pb_Categories(models.Model):
    category_name = models.TextField()


class Pb_Products(models.Model):
    product_name = models.TextField()
    brands = models.TextField(null=True)
    code = models.BigIntegerField()
    categories = models.TextField()
    nutrition_grades = models.CharField(max_length=1)
    stores = models.TextField(null=True)
    url = models.TextField()
    image_url = models.TextField()
    req100 = models.TextField()
    added_timestamp = models.BigIntegerField()
    updated_timestamp = models.BigIntegerField(null=True)


class Pb_Favorite(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(
        Pb_Products, on_delete=models.CASCADE)
    updated_timestamp = models.BigIntegerField()


class Pb_Categories_Products(models.Model):
    category = models.ForeignKey(
        Pb_Categories, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Pb_Products, on_delete=models.CASCADE)
