from django.contrib import admin
from project_finder_web_app.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

# Register your models here.


class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class UserAdmin(UserAdmin):
    form = UserChangeForm

    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                )
            },
        ),
    )


admin.site.register(User)  # import UserAdmin and check for documentation for authentication
