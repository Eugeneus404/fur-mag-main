"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib import admin

class UserProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.FileField()

class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.SlugField(max_length=255, blank=True)
        
class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    remain = models.IntegerField()
    description = models.TextField(null=True, blank=True)

class Image(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    path = models.FileField()

class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    count = models.IntegerField()
    price = models.FloatField()
    
class Review(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    grade = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(UserProfile)
admin.site.register(Review)