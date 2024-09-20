from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAdmin(UserAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "phone_number",
                    "role",
                    "first_name",
                    "middle_name",
                    "last_name",
                    "gender",
                    # "device_id",
                    # "is_teacher",
                    # "is_student",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "middle_name",
                    "last_name",
                    "gender",
                    "phone_number",
                    "role",
                    # "device_id",
                    # "is_teacher",
                    # "is_student",
                ),
            },
        ),
    )

    list_display = [
        "email",
        "first_name",
        "middle_name",
        "last_name",
        "gender",
        "phone_number",
        "role",
        # "is_teacher",
        # "is_student",
    ]

    search_fields = (
        "email",
        "first_name",
        "middle_name",
        "last_name",
        "gender",
        "phone_number",
        "role",
        "password",
        # "is_teacher",
        # "is_student",
    )

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "groups",
        "email",
    )

    ordering = ("id",)


admin.site.register(User, UserAdmin)
