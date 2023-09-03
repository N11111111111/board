from django.views.generic.edit import CreateView
from .models import*
from django.contrib.auth.models import User
from news.models import Author, Category, SubscribedUsersCategory
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import UpdateView, FormView
from django.shortcuts import get_object_or_404
import random
from django.http import Http404
from django.shortcuts import render
from .models import*
from django.contrib.auth.models import User
import datetime
from django.contrib.auth import logout, authenticate, login
from random import SystemRandom
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
import math, random
from random import SystemRandom
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import forms
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.views.generic import View

from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
import math, random
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.views import View
from django.http import HttpResponse, HttpRequest
from django.http import HttpResponseBadRequest
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
import pyotp
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
import requests
from django.views.generic import TemplateView


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = 'login'



def login_view(request):

    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        user = authenticate(request, username=username, password=password)

        if user is not None:

            totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
            otp = totp.now()
            request.session['otp_secret_key'] = totp.secret
            valid_date = datetime.now() + timedelta(minutes=2)
            request.session['otp_valid_date'] = str(valid_date)

            request.session['username'] = username

            body = f"Уважаемый {username}, Ваш OTP  {otp}."
            send_mail('OTP request',body,'usjusj@yandex.ru',[email], fail_silently=False)

            return redirect('otp')
        else:
            error_message = 'Неправильные  данные! Проверьте имя, пароль и почту , или зерегистрируйтесь'

    return render(request, 'login.html', {'error_message': error_message})


def otp_view(request):

    error_message = None
    if request.method == 'POST':
        otp = request.POST['otp']
        username = request.session['username']

        otp_secret_key = request.session['otp_secret_key']
        otp_valid_until = request.session['otp_valid_date']

        if otp_secret_key and otp_valid_until is not None:
            valid_until = datetime.fromisoformat(otp_valid_until)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)

                if totp.verify(otp):
                    user = get_object_or_404(User, username=username)
                    login(request, user)

                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']


                    if not request.user.groups.filter(name='authors').exists():
                        premium_group = Group.objects.get(name='authors')
                        user = request.user.id
                        premium_group.user_set.add(user)


                        if not Author.objects.filter(authorUser=user).exists():
                            user = request.user
                            Author.objects.create(authorUser=user)


                        return redirect('/')



                else:
                    error_message = 'Неправильнo введенные данные (код)'
            else:
                error_message = 'неправильный код или  одноразового кода истек срок действия в 2 минутs'

        else:
            error_message = 'Извините, что-то пошло не так...'




    return render(request, 'otp.html', {'error_message': error_message})



@login_required
def main_view(request):
    if 'username' in request.session:
        del request.session['username']
    return render(request, 'news.html', {})



def logout_view(request):
    logout(request)
    return redirect('sign/login')


#
# def upgrade_me(request):
#     premium_group = Group.objects.get(name='authors')
#     if not request.user.groups.filter(name='authors').exists():
#         user = request.user
#         premium_group.user_set.add(user)
#
#     if not Author.objects.filter(authorUser=user).exists():
#         user = request.user
#         Author.objects.create(authorUser=user)



    # if not Author.objects.filter(authorUser=user).exists():
    #     Author.objects.create(authorUser=user)


    # if request.method == POST:
        # premium_group = Group.objects.get(name='authors')(code=code.objects.get(request.POST.get("code_from_form").code))
        # if not request.user.groups.filter(name='authors').exists():
        #       premium_group.user_set.add(user)



    # if not Author.objects.filter(authorUser=user).exists():
    #     Author.objects.create(authorUser=user)
    # premium_group = Group.objects.get(name='authors')

    # if not request.user.groups.filter(name='authors').exists():
    #     premium_group.user_set.add(user)
    #
    #     return redirect('/')

def upgrade_me(request):

    user = request.user
    premium_group = Group.objects.get(name='authors')
    if request.user.groups.filter(name='authors').exists():
        user.groups.clear()

        if Author.objects.filter(authorUser=user).exists():
            user.delete()

    return redirect('/accounts/login/')



def unsubscribe(request):
    user = request.user
    category_id = request.GET.get('category_id')
    category = Category.objects.get(id=category_id)
    if category.subscribed.filter(email=request.user.email).exists():
        SubscribedUsersCategory.objects.filter(subscribed=user, category=category).delete()

    return redirect('/')




























