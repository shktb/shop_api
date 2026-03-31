from django.db import models
from django.contrib.auth.models import User
from users.models import CustomUser
from common.models import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    
STARS = ((i, '*' * i) for i in range(1, 6))

class Review(BaseModel):
    text = models.TextField(blank=True, null=True)
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.SET_NULL, related_name='reviews')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    stars = models.IntegerField(choices=STARS, null=True, default=5)

    
class UserConfirm(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='confirm')
    code = models.CharField(max_length=6)