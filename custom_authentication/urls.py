from django.urls import path ;
from .views import UserRegistrationView,UserLoginView,UserLogoutView,UserResetPassword,RequestOTPView,VerifyOTPView,ForgotPasswordView;
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns=[
path('register/',UserRegistrationView.as_view()),
path('login/',UserLoginView.as_view()),
path('logout/',UserLogoutView.as_view()),
path('refresh_access_token/',TokenRefreshView.as_view()),
path('reset_password/',UserResetPassword.as_view()),
path('request_otp/',RequestOTPView.as_view()),
path('verify_otp/',VerifyOTPView.as_view()),
path('forgot_password/',ForgotPasswordView.as_view())
]