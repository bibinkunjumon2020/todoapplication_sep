from django import forms
from django.contrib.auth.models import User
from todoapp.models import Todos
from django.contrib.auth.forms import UserCreationForm
'''
class RegistrationForm(forms.Form):
    first_name=forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email= forms.EmailField()
    password = forms.CharField() '''

class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    class Meta:
        model = User
        fields = ["first_name","last_name","username","email","password1","password2"]
        widgets={
                #here we style variables from model
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"})
        }


class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todos
        fields = ["task_name"]
        widgets={
            "task_name":forms.TextInput(attrs={"class":"form-control"})
        }

class TodoChangeForm(forms.ModelForm):
    class Meta:
        model=Todos
       # fields = "__all__"
        exclude=("user",)   # to include all fields and exclude user from that
