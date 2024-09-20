from django.db import models
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver



# Create your models here.
class Level(models.Model):
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=1)

    def __str__(self):
        return self.name

class Gender(models.Model):
    acronym = models.CharField(max_length=1)
    description = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.description}"


class Payment(models.Model):
    payment_status = models.CharField(max_length=200)

    def __str__(self):
        return self.payment_status


class Progress(models.Model):
    progress_status = models.CharField(max_length=200)

    def __str__(self):
        return self.progress_status



