from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from datetime import date

"""Custom User Manager"""
class CustomUserManager(BaseUserManager):
    """Manager for CustomUser using email as the unique identifier"""

    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "Admin")
        extra_fields.setdefault("membership_type", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)

"""Custom User Model"""
def user_profile_photo_upload_to(instance, filename):
    return f"profile_photos/{instance.username}/{filename}"


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True, help_text="Format: YYYY-MM-DD")
    profile_photo = models.ImageField(upload_to=user_profile_photo_upload_to, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    MEMBERSHIP_CHOICES = [
        ("basic", "Basic"),
        ("premium", "Premium"),
        ("admin", "Admin"),
    ]
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES, default="basic")

    ROLE_CHOICES = [
        ("Admin", "Admin"),
        ("Librarian", "Librarian"),
        ("Member", "Member"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="Member")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        permissions = [
            ("can_access_premium", "Can access premium features"),
            ("can_manage_content", "Can manage all content"),
            ("can_manage_users", "Can manage users"),
        ]

    def __str__(self):
        return self.email

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        return (
            today.year
            - self.date_of_birth.year
            - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        )

# ---------------------------
# Domain Models
# ---------------------------

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    is_premium = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("can_create_book", "Can create book"),
            ("can_view", "Can view books"),
            ("can_edit_book", "Can edit book"),
            ("can_delete_book", "Can delete book"),
            ("can_view_premium_books", "Can view premium books"),
            ("can_publish_book", "Can publish new books"),
            ("can_delete_any_book", "Can delete any book"),
        ]

    def __str__(self):
        return f"{self.title} by {self.author.name}"

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name="libraries")

    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name="librarian")

    def __str__(self):
        return f"{self.name} ({self.library.name})"

