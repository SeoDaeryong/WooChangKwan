from django.db import models

class Category(models.Model):
    category = models.CharField(max_length=144)
    order = models.IntegerField()

class Item(models.Model):
    category = models.CharField(max_length=144)
    name = models.CharField(max_length=144)
    count = models.IntegerField()
    limit = models.IntegerField()
