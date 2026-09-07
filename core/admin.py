from django.contrib import admin

from core.models import Navigation, UserProfile


class BaseModelAdmin(admin.ModelAdmin):
    exclude = [
        "created_by",
        "modified_by",
    ]

    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.created_by = request.user
        obj.modified_by = request.user

        super().save_model(request, obj, form, change)


@admin.register(UserProfile)
class UserProfileAdmin(BaseModelAdmin):
    pass


@admin.register(Navigation)
class NavigationAdmin(BaseModelAdmin):
    pass
