from django.db import models
from django.contrib.auth.models import User
import os

# from django import
# Create your models     here.

'''class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    gender = models.CharField(max_length=15)
    userType = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username



class Skill(models.Model):
    skill_name = models.CharField(max_length=50, blank=False, unique=True)

    def __str__(self):
        return self.skill_name'''


class Freelancer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    # email = models.EmailField()
    # password = models.CharField(max_length=50)
    # image = models.ImageField(upload_to="")
    name = user.name
    #email = models.CharField(max_length=150)
    skills = models.CharField(max_length=500)
    gender = models.CharField(max_length=10)
    type = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username


class Hirer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    name = user.name
    # email = models.EmailField()
    # image = models.ImageField(upload_to="")
    gender = models.CharField(max_length=10)
    type = models.CharField(max_length=15)
    # status = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Job(models.Model):
    company = models.ForeignKey(Hirer, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    title = models.CharField(max_length=200)
    salary = models.FloatField()
    #image = models.ImageField(upload_to="")
    description = models.TextField(max_length=400)
    experience = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    skills = models.CharField(max_length=200)
    creation_date = models.DateField()

    def __str__ (self):
        return self.title


class Project(models.Model):
    creator = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    domain = models.CharField(max_length=50)
    price = models.IntegerField()
    demo = models.URLField(max_length=200)
    repo = models.URLField(max_length=200)
    description = models.TextField(max_length=400)

    def __str__(self):
        return self.title


class Application(models.Model):
    company = models.CharField(max_length=200, default="")
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    resume = models.ImageField(upload_to="")
    apply_date = models.DateField()

    def __str__(self):
        return str(self.freelancer)
