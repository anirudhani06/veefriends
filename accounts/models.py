from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
import uuid
from django.urls import reverse

# Create your models here.


# Custom user manager
class UserManager(BaseUserManager):
    def create_user(self, username, email, name, password=None, **others):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        if not name:
            raise ValueError("Name is required")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, name=name, **others)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, name, password=None, **others):
        others.setdefault("is_superuser", True)
        others.setdefault("is_staff", True)
        others.setdefault("is_active", True)

        if others.get("is_superuser") is not True:
            raise ValueError("Superuser is must be True")
        if others.get("is_staff") is not True:
            raise ValueError("Staff is must be True")
        if others.get("is_active") is not True:
            raise ValueError("Active is must be True")

        return self.create_user(username, email, name, password, **others)


# Custom user model
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    username = models.CharField(max_length=60, unique=True)
    email = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=60)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "name"]

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


# base model inheritted by every model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    username = models.CharField(max_length=60)
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=255)
    avatar = models.ImageField(default="default/avatar.jpg", upload_to="profile/")
    cover_picture = models.ImageField(
        default="default/cover_picture.jpg", upload_to="cover/"
    )
    bio = models.TextField(blank=True)
    followers = models.ManyToManyField(
        "self", blank=True, symmetrical=False, related_name="follower"
    )
    following = models.ManyToManyField(
        "self", blank=True, symmetrical=False, related_name="follow"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_absolute_url(self):
        return reverse("profile", kwargs={"username": self.username})

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ["-created_at"]
