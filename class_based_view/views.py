from datetime import datetime

from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from products.models import Product, Category, Review
from products.serializer import (
    ProductListSerializer,
    CategoryListSerializer,
    ReviewListSerializer,
    ProductValidateSerializer
)

from django.contrib.auth.models import User 
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from users.models import CustomUser
from common.permissions import (
    IsOwner, IsAnonymous, CanEditWithin15Minutes, IsModerator
)
from products.models import UserConfirm
import random
from django.db import transaction

from common.validators import validate_age

from .tasks import create_product

class ProductListApiView(ListCreateAPIView):
    queryset = Product.objects.all()
    pagination_class = PageNumberPagination
    filterset_fields = ['title', 'description']
    permission_classes = [IsModerator]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Product.objects.all()
        return Product.objects.filter(owner=user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductValidateSerializer
        return ProductListSerializer

    def create(self, request, *args, **kwargs):
        token_data = self.request.auth
        birthdate = datetime.strptime(token_data.get('birthdate'), '%Y-%m-%d').date()
        if not birthdate:
            raise ValidationError("Дата рождения не указана.")
        print(birthdate)
        validate_age(birthdate)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
    
         # 3. Подготовка данных для Celery (только простые типы!)
        product_data = serializer.validated_data
        user_id = request.user.id # Передаем только цифру (ID)
        # 4. Запуск задачи (передаем словарь с данными и ID пользователя)
        create_product.delay(product_data, user_id)
        return Response(data={'message': 'Product creating'}, status=status.HTTP_201_CREATED)



class CategoryListApiView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer

class ReviewListApiView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer


class ProductUpdateDestroyListApiView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    lookup_field = 'id' 
    permission_classes = [ IsModerator | IsAnonymous | (IsOwner & CanEditWithin15Minutes)]

class CategoryUpdateDestroyListApiView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    lookup_field = 'id'

class ReviewUpdateDestroyListApiView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    lookup_field = 'id'

class UserReviewListApiView(ListAPIView):
    serializer_class = ReviewListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(author=self.request.user)
    

class AuthorizationAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            new_code = f"{random.randint(100000, 999999)}"
            UserConfirm.objects.update_or_create(
                user=user, 
                defaults={'code': new_code}
            )
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            return Response(data={'key': token.key, 'code': new_code}, status=status.HTTP_200_OK)

        return Response(data={'error': "User not Found"}, status=status.HTTP_404_NOT_FOUND)

class RegistrationAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = User.objects.create_user(username=username, password=password, is_active=False)
        code = f"{random.randint(100000, 999999)}"
        UserConfirm.objects.create(user=user, code=code)

        return Response(data={'message': 'User created successfully', 'code': code}, status=status.HTTP_201_CREATED)
    
class ConfirmAPIView(APIView):
    def post(self, request):
        code = request.data.get('code')
        try:
            confirm_obj = UserConfirm.objects.get(code=code)
        except UserConfirm.DoesNotExist:
            return Response(data={'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = confirm_obj.user
        user.is_active = True
        user.save()
        confirm_obj.delete()
        
        return Response(data={'message': 'User activated successfully!'}, status=status.HTTP_200_OK)