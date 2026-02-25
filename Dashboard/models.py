from django.db import models


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=20)
    course = models.CharField(max_length=30)
    age = models.IntegerField()
    email = models.EmailField()
    gender = models.CharField(max_length=20,null=True ,blank=True)
    date = models.DateField(max_length=40,null=True ,blank=True)

    def __str__(self):
        return self.name

class Exam(models.Model):
    exam_code = models.IntegerField(max_length=40)
    date = models.DateField(max_length=40)

    def __str__(self):
        return self.exam_code
