import random
import string
from django.core.mail import send_mail
from django.conf import settings
import pyotp
from datetime import datetime, timedelta
from .views import login_view
from django.core.mail import send_mail
from django.contrib.auth.models import User



# def generate_otp(length=6):
#     characters = string.digits
#     otp = ''.join(random.choice(characters) for _ in range(length))
#     return otp
#
# def send_otp_email(email, otp):
#     subject = 'Ваш OTP '
#     message = f'Your OTP is: {otp}'
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     send_mail(subject, message, from_email, recipient_list)




# def send_otp(request):
#
#    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
#    otp = totp.now()
#    request.session['otp_secret_key'] = totp.secret
#    valid_date = datetime.now() + timedelta(minutes=2)
#    request.session['otp_valid-date'] = str(valid_date)

