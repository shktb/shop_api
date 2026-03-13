from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Product, Category, Review, UserConfirm
from .serializer import (
    ProductDetailSerializer, 
    ProductListSerializer, 
    CategoryListSerializer, 
    CategoryDetailSerializer, 
    ReviewListSerializer, 
    ReviewDetailSerializer,
    ProductValidateSerializer,
    CategoryValidateSerializer,
    ReviewValidateSerializer
)
from rest_framework import status
from django.db.models import Count
from django.db import transaction

from django.contrib.auth.models import User 
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

import random
# Create your views here.

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'product not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductDetailSerializer(product, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category_id = request.data.get('category_id')
        product.save()
        return Response(data=ProductDetailSerializer(product).data,
                        status=status.HTTP_201_CREATED)


@api_view(http_method_names=['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        # step 1: Collect films from DB (QuerySet)
        products = Product.objects.all()

        # step 2: Reformat (Serialize) to list of dictionaries
        data = ProductListSerializer(products, many=True).data

        # step 3: Return Response
        return Response(
            data=data,  
        )
    
    elif request.method == 'POST':
        # step 0:
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        # step 1: Receive data from RequestBody
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category_id = serializer.validated_data.get('category_id')
        

        # step 2: Create film
        with transaction.atomic():
            product = Product.objects.create(
                title=title,
                description=description,
                price=price,
                category_id=category_id
            )
            
            product.save()

        # step 3: Return Response
        return Response(status=status.HTTP_201_CREATED,
                        data=ProductListSerializer(product).data)


@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        category = Category.objects.annotate(products_count=Count('product'))
        data = CategoryListSerializer(category, many=True).data
        return Response(
            data=data, 
        )
    elif request.method == 'POST':
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        name = serializer.validated_data.get('name')
        
        with transaction.atomic():
            category = Category.objects.create(name=name)
        
        category.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryListSerializer(category).data)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': 'category not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = CategoryDetailSerializer(category, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category.name = request.data.get('name')
        category.save()
        return Response(data=CategoryDetailSerializer(category).data,
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        review = Review.objects.all()
        data = ReviewListSerializer(review, many=True).data
        return Response(
            data=data, 
        )
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        text = serializer.validated_data.get('text')
        product_id = serializer.validated_data.get('product_id')
        stars = serializer.validated_data.get('stars')
        
        with transaction.atomic():
            review = Review.objects.create(
                text=text,
                product_id=product_id,
                stars=stars
            )
        
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewListSerializer(review).data)

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'review not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        data = ReviewDetailSerializer(review, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review.text = request.data.get('text')
        review.product_id = request.data.get('product_id')
        review.stars = request.data.get('stars')
        review.save()
        return Response(data=ReviewDetailSerializer(review).data,
                        status=status.HTTP_201_CREATED)
    

# =====================================

@api_view(['POST'])
def authorization(request):
    if request.method == "POST":
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
            # try:
            #     token = Token.objects.get(user=user)
            #
            # except Token.DoesNotExist:

            token = Token.objects.create(user=user)
            return Response(data={'key': token.key, 'code': new_code},
                            status=status.HTTP_200_OK)

        return Response(data={'error': "User not Found"},
                        status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def registration(request):
    if request.method == "POST":
        username = request.data.get('username')
        password = request.data.get('password')
        # User.objects.create_user(username=username, password=password)

        user = User.objects.create_user(username=username, password=password, is_active=False)
        code = f"{random.randint(100000, 999999)}"
        UserConfirm.objects.create(user=user, code=code)

        return Response(data={'message': 'User created successfully', 'code': code},
                        status=status.HTTP_201_CREATED)

@api_view(['POST'])
def confirm(request):
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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_reviews(request):
    reviews =  Review.objects.filter(author=request.user)
    serializers = ReviewListSerializer(reviews, many=True)
    return Response(data=serializers.data)