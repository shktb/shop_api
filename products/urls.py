from django.urls import path
from .import views

urlpatterns = [
    path('products/', views.product_list_api_view),
    path('products/<int:id>/', views.product_detail_api_view),
    path('categories/', views.category_list_api_view),
    path('categories/<int:id>/', views.category_detail_api_view),
    path('reviews/', views.review_list_api_view),
    path('reviews/<int:id>/', views.review_detail_api_view),
    path('login/', views.authorization),
    path('registration/', views.registration),
    path('users/confirm/', views.confirm),
    path('users/reviews/', views.user_reviews),
]