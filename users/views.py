from django.shortcuts import render
from django.contrib.auth.models import User 
from .models import CustomUser
from .serializer import (
    RegisterValidateSerializer,
    ConfirmationSerializer, 
    AuthValidateSerializer, 
)
from users.serializer import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from products.models import UserConfirm
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.response import Response

import random

from django.core.cache import cache
# Create your views here.

class AuthorizationAPIView(CreateAPIView):
    serializer_class = AuthValidateSerializer
    def post(self, request):
        serializer = AuthValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        print(user)
        if user:
            new_code = f"{random.randint(100000, 999999)}"
            # UserConfirm.objects.update_or_create(
                # user=user, 
                # defaults={'code': new_code}
            # )
            registration_data = {
                'code': new_code
            }
            cache.set(email, registration_data, 300)
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            return Response(data={'key': token.key, 'code': new_code}, status=status.HTTP_200_OK)
        else:
            return Response(data={'error': "User not Found"}, status=status.HTTP_404_NOT_FOUND)

class RegistrationAPIView(CreateAPIView):
    serializer_class = RegisterValidateSerializer
    def post(self, request):
        serializer = RegisterValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
    
        email = request.data.get('email')
        raw_password = request.data.get('password')
        phone_number = request.data.get('phone_number')
        code = f"{random.randint(100000, 999999)}"

        password = make_password(raw_password)
        if not phone_number or str(phone_number).strip() == "":
            phone_number = None
        # user = CustomUser.objects.create_user(email=email, phone_number=phone_number, password=password, is_active=False)
        # UserConfirm.objects.create(user=user, code=code)
        
        registration_data = {
            'email': email,
            'password': password,
            'phone_number': phone_number,
            'code': code
        }
        cache.set(email, registration_data, 300)


        return Response(data={'message': 'User created successfully', 'code': code}, status=status.HTTP_201_CREATED)
    
class ConfirmAPIView(CreateAPIView):
    serializer_class = ConfirmationSerializer

    def post(self, request):
        serializer = ConfirmationSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)

        email = request.data.get('email')
        code = request.data.get('code')
        cached_data = cache.get(email)

        if not cached_data:
            return Response(
                data={'error': 'Code expired or registration not found'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if str(cached_data['code']) != code:
            return Response(
                data={'error': 'Invalid code'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        # try:
        #     confirm_obj = UserConfirm.objects.get(code=code)
        # except UserConfirm.DoesNotExist:
        #     return Response(data={'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)
        
        # user = confirm_obj.user
        if not CustomUser.objects.filter(email=email):
            user = CustomUser(
                email=cached_data['email'],
                password=cached_data['password'],
                phone_number=cached_data.get('phone_number'),
                is_active=True
            )
            user.save()

        # user = CustomUser.objects.get(email=email)
        # user.is_active = True
        # confirm_obj.delete()
        cache.delete(email)
        
        return Response(data={'message': 'User activated successfully!'}, status=status.HTTP_200_OK)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer