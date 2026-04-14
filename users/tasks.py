from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_email(email, code):
    print("SENDING...")
    send_mail(
        "Регистрация в shop_api",
        f"Код подтверждения: {code}",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    print("SENT.")
    return "OK"


@shared_task
def send_funny_notification():
    print("SENDING...")
    send_mail(
        "СРОЧНО!!!",
        "Купи слона",
        settings.EMAIL_HOST_USER,
        ["dauletsaktybekov@gmail.com"],
        fail_silently=False,
    )
    print("SENT.")
    return "OK"

# @shared_task
