from django.urls import path
from .import views

urlpatterns = [
    path('login/', views.AuthorizationAPIView.as_view()),
    path('register/', views.RegistrationAPIView.as_view()),
    path('confirm/', views.ConfirmAPIView.as_view()),
]