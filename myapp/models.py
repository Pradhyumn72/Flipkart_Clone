from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)  
    password = models.CharField(max_length=255) 


class Admin(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)  
    password = models.CharField(max_length=255) 