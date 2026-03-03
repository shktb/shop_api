from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
STARS = ((i, '*' * i) for i in range(1, 6))

class Review(models.Model):
    text = models.TextField(blank=True, null=True)
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.SET_NULL, related_name='reviews')
    stars = models.IntegerField(choices=STARS, null=True, default=5)

    def product_names(self):
        return [i.title for i in self.product.all()]
