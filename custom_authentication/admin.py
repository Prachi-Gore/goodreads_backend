from django.contrib import admin
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django_rest_passwordreset.models import ResetPasswordToken

# this model has been registered in admin panel by default so remove them from admin panel

if admin.site.is_registered(OutstandingToken):
    admin.site.unregister(OutstandingToken)

if admin.site.is_registered(BlacklistedToken):
    admin.site.unregister(BlacklistedToken)

if admin.site.is_registered(ResetPasswordToken):
    admin.site.unregister(ResetPasswordToken)