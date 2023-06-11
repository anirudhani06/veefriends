from django.urls import path
from . import views

urlpatterns = [
    path("create-chat-room", views.create_chat_room, name="create_chat_room"),
    path("room/<str:room_name>/", views.chat_room, name="chat_room"),
    path("request-room/<str:room_name>/", views.req_to_join, name="request_chat_room"),
    path(
        "accept-room/<str:room_name>/<str:username>/",
        views.accept_room_request,
        name="accept_chat_room_request",
    ),
    path(
        "remove-user/<str:room_name>/<str:username>/",
        views.remove_user,
        name="remove_user",
    ),
    path("exit-room/<str:room_name>//", views.exit_room, name="exit_room"),
    path("chat/<str:username>/", views.chat, name="chat"),
]
