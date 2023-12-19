from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from myapp.models import StudentProfile

class RegistrationForm(UserCreationForm):

    class Meta:
        model=User
        fields=["username","email","password1",'password2',"first_name"]



class ProfileForm(forms.ModelForm):

    class Meta:
        model=StudentProfile
        exclude=("user",)

        widgets = {
            'gender': forms.Select(attrs={"class":"form-select form-control"}),
            'qualification': forms.TextInput(attrs={"class": "form-control "}),
            'resume': forms.FileInput(attrs={"class": "form-control "}),
            'skills': forms.Textarea(attrs={"class": "form-control","row":"3"}),
            'age': forms.TextInput(attrs={"class": "form-control " }),
            'gender': forms.Select(attrs={"class": "form-select form-control "}),
            'experience': forms.TextInput(attrs={"class": "form-control "}),
            'address': forms.TextInput(attrs={"class": "form-control "}),
            'phone': forms.TextInput(attrs={"class": "form-control "}),
            'profile_pic': forms.FileInput(attrs={"class": "form-control "}),
        }
        