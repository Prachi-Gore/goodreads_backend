from rest_framework import serializers
from .models import CustomUser,ForgotPasswordOtp
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from .utils import get_user_by_email
from .models import CustomUser


class UserRegistraionSerializer(serializers.ModelSerializer):
    print("*** UserRegistraionSerializer called")
    # confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password',]
        extra_kwargs = {
            'password': {'write_only': True} #  only put and post. can't get
        }

    # def validate(self,data):
    #     print("*** validate called")

    #     if(data['password']!=data['confirm_password']):
    #         raise serializers.ValidationError("Passwords do not match.")
    #     return data    
    
    def create(self, validated_data):
        print("*** create called")
        # validated_data.pop('confirm_password')  # Remove confirm_password before saving
        print("*** validated_data ",validated_data)
       # Create the user with the hashed password
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])  # Hashes the password
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
#    Basic user details for review API

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']
        
class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = CustomUser
    fields = ['email', 'password']    

class UserResetPasswordSerializer(serializers.Serializer):
   old_password=serializers.CharField(required=True,write_only=True)
   new_password=serializers.CharField(required=True,write_only=True)

   def validate(self, data):
      user=self.context['request'].user # in views we have passed this context
      old_password,new_password=data['old_password'],data['new_password']
      
      if not user.check_password(old_password):
        raise serializers.ValidationError({"old_password": "Incorrect password."})
       
      if old_password==new_password:
        raise serializers.ValidationError({"new_password": "New password cannot be the same as the old password."})
      
      if not (6<=len(new_password)<=10):
        raise serializers.ValidationError({"new_password": "Password must be between 6 and 10 characters."})
      
      return data
   
class RequestOTPSerializer(serializers.Serializer):
      email=serializers.EmailField()

      def validate_email(self,value):
        #  User=get_user_model()
        #  user=User.objects.filter(email=value).first()
        #  if not user:
        #     raise serializers.ValidationError("No account found with this email.")
        #  return value
        if(get_user_by_email(value)):
            return value
      
      def save(self):
         email=self.validated_data['email']
         User=get_user_model()
         user=User.objects.get(email=email)
        
        # Invalidate previous OTPs
         ForgotPasswordOtp.objects.filter(user=user,is_verified=False).update(is_verified=True)
        
        # Create and send new OTP
         otp=ForgotPasswordOtp.generate_otp()
         ForgotPasswordOtp.objects.create(user=user,otp=otp)
         send_mail(
            subject="Your Password Reset OTP",
            message=f"Your OTP is {otp}. It is valid for {settings.OTP_EXPIRY_TIME} minutes.",
            from_email="prastaprasta408@gmail.com", # take from setting
            recipient_list=[email],
          )
         return {"message": "OTP has been sent to your email."}

class VerifyOTPSerializer(serializers.Serializer):
    email=serializers.EmailField()   
    otp=serializers.CharField(min_length=6, max_length=6)   

    def validate(self,data):
        email = data['email']
        otp = data['otp']

        # User = get_user_model()
        # user = User.objects.filter(email=email).first()
        # if not user:
        #     raise serializers.ValidationError("No account found with this email.")
        user=get_user_by_email(email)
        otp_entry = ForgotPasswordOtp.objects.filter(user=user, otp=otp, is_verified=False).last()
        if not otp_entry:
            raise serializers.ValidationError("Invalid OTP.")
        
        if otp_entry.is_expired():
            raise serializers.ValidationError("OTP has expired. Please request a new one.")

        # Mark OTP as verified
        otp_entry.is_verified = True
        otp_entry.save()

        return {"message": "OTP verified successfully."}
    
class ForgotPasswordSerializer(serializers.Serializer):
    email=serializers.EmailField()
    new_password=serializers.CharField(min_length=6,max_length=10,write_only=True)

    def validate(self, data):
        email=data['email']
        
        user=get_user_by_email(email)
        # User=get_user_model()
        # user=User.objects.filter(email=email).first()
        # if not user :
        #    raise serializers.ValidationError('No account found with this email.')
        otp_entry = ForgotPasswordOtp.objects.filter(user=user, is_verified=True).last()
        if not otp_entry:
            raise serializers.ValidationError("OTP not verified.")

        return data
    
    def save(self):
        User=get_user_model()
        user = User.objects.get(email=self.validated_data["email"])
        user.set_password(self.validated_data["new_password"])
        user.save()

        # Delete used OTPs
        ForgotPasswordOtp.objects.filter(user=user).delete()

        return {"message": "Password Updated successfully."}