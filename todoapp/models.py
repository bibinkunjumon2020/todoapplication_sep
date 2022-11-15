from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todos(models.Model):
    task_name = models.CharField(max_length=120)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.task_name


class Bird(models.Model):
    common_name = models.CharField(max_length=250)
    scientific_name = models.CharField(max_length=250)

    def __str__(self):
        return self.common_name

class Animal(models.Model):
    color=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    food=models.CharField(max_length=100)

class Human(models.Model):
    job=models.CharField(max_length=100)
    age=models.IntegerField()
    car=models.CharField(max_length=100)