from typing import Iterable, Optional
from django.db import models
import uuid
from accounts.models import Profile
from django.db.models import Q

from django.urls import reverse

# Create your models here.


class Post(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="posts/", blank=True)
    body = models.TextField(blank=True)
    likes = models.ManyToManyField(Profile, related_name="post_likes")
    impressions = models.ManyToManyField(Profile, related_name="post_impressions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_absolute_url(self):
        return reverse("view_post", kwargs={"post_id": self.id})

    def __str__(self):
        return self.body

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"


class Comment(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    body = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class Bookmark(models.Model):
    user = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="bookmark"
    )
    post = models.ManyToManyField(Post, related_name="bookmark")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Bookmark"
        verbose_name_plural = "Bookmarks"


class Activity(models.Model):
    owner = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="activity",
    )
    message = models.ManyToManyField(
        "ActivityMessage", related_name="ActivityMessage_messages"
    )

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"


class ActivityMessage(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    notification = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Activity message"
        verbose_name_plural = "Activity messages"
