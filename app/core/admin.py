from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["email", "name"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("permissions"),
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "is_staff",
                )
            },
        ),
        (_("important Dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(User, UserAdmin)
admin.site.register(models.Recipe)
admin.site.register(models.Tag)
