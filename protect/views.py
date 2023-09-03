from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from news.models import *
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
from sign.models import*
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
import math, random
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
import math, random
from django.views.generic.edit import CreateView
from .models import *
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
from django.contrib.auth import authenticate, login
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

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import logout, authenticate, login
import pyotp
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
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
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
import math, random
from sign.models import*
from sign.views import *
import pyotp
from django.db.models import Q
from news.filters import RequestsFilter
from django_filters import FilterSet

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


    def get_object(self, **kwargs):
        username = self.request.user.username
        return User.objects.get(username=username)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        context['user_category'] = Category.objects.filter(subscribed=self.request.user)
        context['posts'] = Post.objects.filter(author__authorUser__username=self.request.user)
        context['comments'] = Comment.objects.filter(post__author__authorUser__username=self.request.user)

        return context

