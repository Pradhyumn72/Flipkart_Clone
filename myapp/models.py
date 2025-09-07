from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage

# Create your models here.

class Register(models.Model):
    name=models.CharField(max_length=60)
    email=models.EmailField(unique=True)
    contact=models.IntegerField(unique=True)
    password=models.CharField(max_length=16)



class User(models.Model):
    email = models.EmailField(unique=True)  
    password = models.CharField(max_length=16) 


class Admin(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)  
    password = models.CharField(max_length=16)

class Cart(models.Model):
    pass


class Product(models.Model):
    title = models.CharField(max_length=200)
    label = models.CharField(max_length=100, blank=True)
    price = models.PositiveIntegerField()
    image=models.FileField(upload_to='images/',storage=MediaCloudinaryStorage,null=True,blank=True)
    image_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, default='General')
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title} (₹{self.price})"


class AdminUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username