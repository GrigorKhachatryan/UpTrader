from django.db import models

class Menu(models.Model):
    title = models.CharField(max_length=50)
    parent = models.CharField(max_length=50, null=True)
    level = models.IntegerField()