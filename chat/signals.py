from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import ChatRoom, ChatRoomRequest


@receiver(post_save, sender=ChatRoom)
def create_room(sender, instance, created, *args, **kwargs):
    chat_room = instance
    if created:
        chat_room.members.add(chat_room.owner)
        chat_room.save()
