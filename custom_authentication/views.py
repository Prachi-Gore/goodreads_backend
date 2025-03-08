from .serializers import UserRegistraionSerializer,UserLoginSerializer,UserResetPasswordSerializer,RequestOTPSerializer,VerifyOTPSerializer,ForgotPasswordSerializer;
from rest_framework.views import APIView;
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated,AllowAny
# Create your views here.


def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
    permission_classes = [AllowAny] 
    def post(self,request):
        print("*** post call")
        serializer = UserRegistraionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        token=get_tokens_for_user(user)
        return Response({'token':token,'message':"User Created Successfully"},status.HTTP_201_CREATED)


class UserLoginView(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
      serializer = UserLoginSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      email = serializer.data.get('email')
      password = serializer.data.get('password')
      user = authenticate(email=email, password=password)
      if user is not None:
        token = get_tokens_for_user(user)
        return Response({'token':token,'username':user.username, 'message':'Login Success'}, status=status.HTTP_200_OK)
      else:
        return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
      

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class UserResetPassword(APIView):
   permission_classes=[IsAuthenticated]
   def post(self,request):
      serializer=UserResetPasswordSerializer(data=request.data,context={'request': request})
      if serializer.is_valid():
         request.user.set_password(serializer.validated_data['new_password'])
         request.user.save()
         return Response({"message": "Password Reset Successfully."}, status=200)
      return Response(serializer.errors, status=400)   

class RequestOTPView(APIView):
    def post(self,request):
       serializer=RequestOTPSerializer(data=request.data)
       if serializer.is_valid():
        response_data=  serializer.save() 
        return Response(response_data,status=status.HTTP_200_OK)
       return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)        

class VerifyOTPView(APIView):
    def post(self,request):
         serializer=VerifyOTPSerializer(data=request.data)
         if serializer.is_valid():
              return Response(serializer.validated_data, status=status.HTTP_200_OK)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
     def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 