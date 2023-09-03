from django.urls import path
from .views import *
from .views import*
from . import views
from django.contrib.auth.views import *


urlpatterns = [
    path('', IndexView.as_view(), name="index"),

    path('protect/logout',
         LogoutView.as_view(template_name='logout.html'),
         name='logout'),
    path('/logout/entrance',
         LoginView.as_view(template_name='entrance.html'),
         name='entrance'),

]

