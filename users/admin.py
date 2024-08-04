from django.contrib import admin

from users.models import User


# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ("id", "email", "is_active", "is_staff", "is_superuser")
    list_display = ("id", "email", "is_active", "is_staff", "is_superuser")
    search_fields = ("email",)
    ordering = ("id",)
