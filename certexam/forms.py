from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from certexam.models import Battalion, School, Cadet
from .utils import *


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', ]


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class BattalionForm(forms.ModelForm):
    group = forms.ChoiceField(choices=group)
    battalion = forms.ChoiceField(choices=group_dict.get('guwahati'))
    wing = forms.ChoiceField(choices=[('Army', 'Army'), ('Navy', 'Navy'), ('AF', 'AF')], initial='Army')

    class Meta:
        model = Battalion
        exclude = ['user', ]


class AddCadetForm(forms.ModelForm):
    school = forms.ChoiceField()
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')])

    class Meta:
        model = Cadet
        exclude = ['user', 'age', 'unit', 'wing', 'appeared', 'appeared_date']


class AddSchoolForm(forms.ModelForm):

    class Meta:
        model = School
        exclude = ['user', 'wing', ]
