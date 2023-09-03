from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.db import models
from django import forms
from django.contrib.auth.models import User
import random
from django.conf import settings
from django.db import models
import random
from django.shortcuts import render
from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from verified_email_field.models import VerifiedEmailField
from django.forms import ModelForm
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import logout, authenticate, login
import pyotp
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required


class BaseRegisterForm(UserCreationForm):

    email = forms.EmailField(label= "Email")

    class Meta:
        model = User
        fields = ("username",
                  "email",
                  "password1",
                  'password2'

             )
        success_url = 'login'

# class BasicSignupForm(UserCreationForm):
#     email = forms.EmailField(max_length=200, help_text='Required')
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')

class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)

        success_url = 'login'
        return user















