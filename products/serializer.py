from rest_framework import serializers
from .models import Product, Category, Review
from django.db.models import Avg

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