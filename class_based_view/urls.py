from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.ProductListApiView.as_view()),
    path('category/', views.CategoryListApiView.as_view()),
    path('review/', views.ReviewListApiView.as_view()),
    
    path('product/<int:id>/', views.ProductUpdateDestroyListApiView.as_view()),
    path('category/<int:id>/', views.CategoryUpdateDestroyListApiView.as_view()),
    path('review/<int:id>/', views.RetrieveUpdateDestroyAPIView.as_view()),
    path('user/reviews/', views.UserReviewListApiView.as_view()),

    path('user/register/', views.RegistrationAPIView.as_view()),
    path('user/login/', views.AuthorizationAPIView.as_view()),
    path('user/confirm/', views.ConfirmAPIView.as_view()),

]