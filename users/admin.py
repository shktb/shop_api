from django.contrib import admin

# Register your models here.
from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ["id", "email", 'phone_number', "is_active", "is_staff", "birth_date"]
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("phone_number", "password", "is_active", "is_staff")}),
        ("Important dates", {"fields": ("last_login", "birth_date")}),
    )