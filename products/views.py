from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Category, Review
from .serializer import ProductDetailSerializer, ProductListSerializer, CategoryListSerializer, CategoryDetailSerializer, ReviewListSerializer, ReviewDetailSerializer
from rest_framework import status
from django.db.models import Count
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
        # step 1: Receive data from RequestBody
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category_id')
        

        # step 2: Create film
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
        name = request.data.get('name')
        
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
        text = request.data.get('text')
        product_id = request.data.get('product_id')
        stars = request.data.get('stars')
        
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
        review.text = request.data.get('text')
        review.product_id = request.data.get('product_id')
        review.stars = request.data.get('stars')
        review.save()
        return Response(data=ReviewDetailSerializer(review).data,
                        status=status.HTTP_201_CREATED)