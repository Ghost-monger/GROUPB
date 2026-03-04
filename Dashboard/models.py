from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Student(models.Model):
    image = models.ImageField(upload_to='students/',null=True ,blank=True)
    name = models.CharField(max_length=20)
    course = models.CharField(max_length=30)
    age = models.IntegerField()
    email = models.EmailField()
    gender = models.CharField(max_length=20,null=True ,blank=True)
    date = models.DateField(null=True ,blank=True)

    def __str__(self):
        return self.name

class Exam(models.Model):
    exam_code = models.IntegerField(max_length=40)
    date = models.DateField(max_length=40)

    def __str__(self):
        return self.exam_code

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    amount = models.IntegerField()
    checkout_request_id = models.CharField(max_length=40)
    status = models.CharField(max_length=40, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone

