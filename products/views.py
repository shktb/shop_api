from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Category, Review
from .serializer import ProductDetailSerializer, ProductListSerializer, CategoryListSerializer, CategoryDetailSerializer, ReviewListSerializer, ReviewDetailSerializer
from rest_framework import status
# Create your views here.

@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'film not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ProductDetailSerializer(product, many=False).data
    return Response(data=data)


@api_view(http_method_names=['GET'])
def product_list_api_view(request):
    # step 1: Collect films from DB (QuerySet)
    products = Product.objects.all()

    # step 2: Reformat (Serialize) to list of dictionaries
    data = ProductListSerializer(products, many=True).data

    # step 3: Return Response
    return Response(
        data=data,  
    )


@api_view(['GET'])
def category_list_api_view(request):
    category = Category.objects.all()
    data = CategoryListSerializer(category, many=True).data
    return Response(
        data=data, 
    )

@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': 'film not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    data = CategoryDetailSerializer(category, many=False).data
    return Response(data=data)


@api_view(['GET'])
def review_list_api_view(request):
    rewiew = Review.objects.all()
    data = ReviewListSerializer(rewiew, many=True).data
    return Response(
        data=data, 
    )

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        rewiew = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'film not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ReviewDetailSerializer(rewiew, many=False).data
    return Response(data=data)