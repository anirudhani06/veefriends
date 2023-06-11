from django.db import models
import uuid
from accounts.models import Profile
from django.urls import reverse

# Create your models here.


class ChatRoom(models.Model):
    avatar = models.ImageField(upload_to="room/", default="room.jpg")
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    room = models.CharField(max_length=60, unique=True)
    members = models.ManyToManyField(
        Profile, related_name="members", through="ChatRoomMember"
    )
    category = models.ForeignKey(
        "ChatRoomCategory", on_delete=models.CASCADE, null=True, blank=True
    )
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_absolute_url(self):
        return reverse("chat_room", kwargs={"room_name": self.room})

    def __str__(self):
        return self.room

    class Meta:
        verbose_name = "Chat room"
        verbose_name_plural = "Chat rooms"


class ChatRoomMember(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    member = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Chat room member"
        verbose_name_plural = "Chat rooms members"


class ChatRoomMessage(models.Model):
    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="chat_room_messages"
    )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = "Chat room message"
        verbose_name_plural = "Chat rooms messages"


class ChatRoomCategory(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Chat room category"
        verbose_name_plural = "Chat rooms categories"


class ChatRoomRequest(models.Model):
    room = models.OneToOneField(
        ChatRoom, on_delete=models.CASCADE, related_name="chat_room_requests"
    )
    users = models.ManyToManyField(Profile, related_name="chat_room_requests")

    def __str__(self):
        return self.room.room

    class Meta:
        verbose_name = "Chat room request"
        verbose_name_plural = "Chat rooms requests"


class Chat(models.Model):
    room = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.room


class ChatMessage(models.Model):
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name="chat_messages"
    )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
