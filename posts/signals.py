from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Post, Comment, Activity, ActivityMessage
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Comment)
def add_comment(sender, instance, created, *args, **kwargs):
    comment = instance
    notify = ActivityMessage()
    notification, _ = Activity.objects.get_or_create(owner=comment.post.owner)
    if created:
        if comment.owner != comment.post.owner:
            notify.user = comment.owner
            notify.notification = f"Commented '{comment.body[0:10]}'"
            notify.post = comment.post
            notify.save()
            notification.message.add(notify)
            notification.save()


@receiver(m2m_changed, sender=Post.likes.through)
def add_likes(sender, instance, action, *args, **kwargs):
    notification, _ = Activity.objects.get_or_create(owner=instance.owner)
    notify = ActivityMessage()
    if action == "post_add":
        user = kwargs.get("model").objects.filter(pk__in=kwargs.get("pk_set")).first()
        if instance.owner != user:
            notify.user = user
            notify.notification = f"Liked your post"
            notify.post = instance
            notify.save()
            notification.message.add(notify)
            notification.save()


@receiver(post_save, sender=ActivityMessage)
def send_activity(sender, instance, created, *args, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            instance.post.owner.username,
            {
                "type": "send_activity",
                "user": instance.user.username,
                "user_img": instance.user.avatar.url,
                "message": instance.notification,
                "post": instance.post.get_absolute_url,
            },
        )
