from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser
# Create your models here.

departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Allergists','Allergists'),
('Anesthesiologists','Anesthesiologists')
]


class CustomUser(AbstractUser):
    
   # image=models.ImageField(upload)
    userchoice = ((1,"Doctor"),(2,"Patient"))
    usertype = models.IntegerField(default=1, choices=userchoice)



class Doctor(models.Model):
    user=models.OneToOneField(CustomUser, on_delete=CASCADE, related_name='Doctor')
    name=models.CharField(max_length=50)
    mobile=models.IntegerField()
    specielist=models.CharField(max_length=50,choices=departments,default='Cardiologist')

    def __str__(self):
        return self.name

class Patient(models.Model):
    user=models.OneToOneField(CustomUser, on_delete=CASCADE, related_name='patient')
    name=models.CharField(max_length=50)
    gender=models.CharField(max_length=10)
    mobile=models.IntegerField()
    age=models.IntegerField()
    address=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Appointment(models.Model):
   # doctor=models.ForeignKey(Doctor, on_delete=CASCADE)
    patientname=models.ForeignKey(CustomUser, on_delete=CASCADE)
    dep=models.CharField(max_length=50,choices=departments,default='Cardiologist')
    date=models.DateField() 
    time=models.TimeField()
    prescription=models.TextField(null=True, blank=True)
     

    def __str__(self):
        return str(self.patientname)
