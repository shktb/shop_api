from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from products.models import Product, Category, Review
from products.serializer import ProductListSerializer, CategoryListSerializer, ReviewListSerializer

from django.contrib.auth.models import User 
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response

from products.models import UserConfirm
import random

class ProductListApiView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    pagination_class = PageNumberPagination
    filterset_fields = ['title', 'description']

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