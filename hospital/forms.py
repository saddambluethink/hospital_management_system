from django import forms

from django.contrib.auth.models import User


from .models import  CustomUser, Doctor, Patient,Appointment
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth import get_user_model
User = get_user_model()

class CustomUserform(UserCreationForm):
    class Meta:
        model =User
        fields = ['username', 'usertype']


class patientform(forms.ModelForm):
    class Meta:
        model =Patient
        fields = '__all__'

        # fields = ['name', 'gender', 'mobile', 'age', 'address']

class doctorform(forms.ModelForm):
    class Meta:
        model =Doctor
        fields = '__all__'


class appointmentform(forms.ModelForm):
    class Meta:
        model =Appointment
        fields = ['dep','date','time']
# class patientform(forms.ModelForm):
#     class Meta:
#         model =Patient
#         fields = '__all__'       

class appointmentforms(forms.ModelForm):
    class Meta:
        model =Appointment
        fields = ['prescription',]