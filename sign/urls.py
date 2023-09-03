from django.contrib.auth.views import *
from .views import *
from django.urls import path
from .views import  unsubscribe
from django.urls import path

from .views import logout_view,  login_view, otp_view





#
# urlpatterns = [
#     # path('login/',
#     #      LoginView.as_view(template_name='login.html'),
#     #      name='login'),
#     # path('logout/',
#     #      LogoutView.as_view(template_name='logout.html'),
#     #      name='logout'),
#     # path('login/signup/',
#     #      BaseRegisterView.as_view(template_name='signup.html'),
#     #      name='signup'),
#
#
#     # # path('loginUser/', loginUser, name='login'),
#     # path('otp_verification/', otp_verification, name='otp'),
#     path('upgrade/', upgrade_me, name='upgrade'),
#     path('unsubscribe/', unsubscribe, name='unsubscribe'),
#
#
#
# ]




urlpatterns = [
    path('', main_view, name='main'),
    path('login/', login_view, name='login'),
    # path('logout/', logout_view, name='logout'),

    # path('logout/',
    #      LogoutView.as_view(template_name='logout.html'),
    #      name='logout'),

    path('sign/logout/', logout_view, name='logoutt'),
    path('otp/', otp_view, name='otp'),


    path('login/signup/',
         BaseRegisterView.as_view(template_name='signup.html'),
         name='signup'),

    path('upgrade/', upgrade_me, name='upgrade'),
    path('unsubscribe/', unsubscribe, name='unsubscribe'),
]