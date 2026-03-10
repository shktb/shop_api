from rest_framework import serializers
from .models import Product, Category, Review
from django.db.models import Avg
from rest_framework.exceptions import ValidationError

class ProductDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = 'id title description price category_name created'.split()


class CategoryListSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = 'name products_count'.split()


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name'.split()



class ReviewListSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ('id product_title product_average_rating text stars').split()

    def get_product_average_rating(self, review):
        if review.product:
            avg = review.product.reviews.aggregate(Avg('stars'))['stars__avg']
            return round(avg, 2) if avg else 0
        return 0

class ReviewDetailSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)

    class Meta:
        model = Review
        fields = 'product_title text stars'.split()

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(default='Good product')
    stars = serializers.IntegerField(min_value=1, max_value=5)
    product_id = serializers.IntegerField()

    def validate_category_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('Product does not exist!')
        return product_id

class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=1, max_length=255)

class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=1, max_length=255)
    description = serializers.CharField(required=False, default='No text')
    price = serializers.IntegerField()
    category_id = serializers.IntegerField()


    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category does not exist!')
        return category_id