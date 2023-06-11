from django.contrib import admin
from .models import ChatRoom, ChatRoomMessage, ChatRoomRequest, Chat

# Register your models here.

admin.site.register([ChatRoom, ChatRoomMessage, ChatRoomRequest, Chat])
