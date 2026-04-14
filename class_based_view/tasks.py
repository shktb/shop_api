from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def create_product(product_data, user_id):
    from products.models import Product
    from users.models import CustomUser
    from django.db import transaction

    user = CustomUser.objects.get(id=user_id)
    product = Product.objects.create(owner=user, **product_data)

    send_mail(
        "Уважаемый пользователь!",
        "Ваш продукт успешно создан",
        settings.EMAIL_HOST_USER,
        [user],
        fail_silently=False,
    )
    
    return f"Product {product.id} created successfully"