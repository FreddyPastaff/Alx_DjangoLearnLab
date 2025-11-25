from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")
    list_filter = ("publication_year", "author")
    search_fields = ("title", "author")

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "date_of_birth")
    search_fields = ("username", "email")
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("date_of_birth", "profile_photo", "phone_number", "bio", "membership_type", "role")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

   # add_fieldsets control the layout of the create form
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "is_staff", "is_active", "date_of_birth", "profile_photo", "phone_number", "bio", "membership_type", "role"),
        }),
    )             
                
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.site_header = "Bookshelf Admin"
admin.site.site_title = "Bookshelf Admin Portal"