from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import (
    ChatRoom,
    ChatRoomMessage,
    ChatRoomRequest,
    ChatRoomCategory,
    ChatRoomMember,
    ChatMessage,
    Chat,
)
from accounts.models import Profile

# Create your views here.


@csrf_exempt
@login_required(login_url="login")
def create_chat_room(request):
    room_categories = ChatRoomCategory.objects.all()
    if request.method == "POST":
        avatar = request.FILES.get("avatar")
        room_name = request.POST.get("room_name").capitalize()
        room_category = request.POST.get("room_category").capitalize()
        is_private = request.POST.get("is_private")
        room_category, _ = ChatRoomCategory.objects.get_or_create(name=room_category)

        chat_room = ChatRoom()
        chat_room.avatar = avatar
        chat_room.owner = request.user.profile
        chat_room.room = room_name
        chat_room.category = room_category
        chat_room.is_private = False if is_private == None else True
        chat_room.save()

    context = {"room_categories": room_categories}
    return render(request, "chat/create_room.html", context)


@login_required(login_url="login")
def chat_room(request, room_name):
    room = ChatRoom.objects.filter(room=room_name).first()
    if room == None:
        return HttpResponse(f"{room_name} - invalid room name")

    chat_messages = ChatRoomMessage.objects.select_related("room").filter(room=room)
    room_name = room.room.upper()
    room_members = room.members.all()

    if room.is_private:
        if not request.user.profile in room.members.all():
            return HttpResponse("Private Room!")

    if not room.is_private:
        if request.user.profile not in room.members.all():
            room.members.add(request.user.profile)
            room.save()

    context = {
        "room_name": room_name,
        "chat_messages": chat_messages,
        "room": room,
        "room_members": room_members,
    }
    return render(request, "chat/chat_room.html", context)


@login_required(login_url="login")
def req_to_join(request, room_name):
    room = ChatRoom.objects.filter(room=room_name).first()
    if room == None:
        return HttpResponse("Room dose not exists")

    if not room.is_private:
        return redirect("home")

    if room.owner == request.user.profile:
        return HttpResponse("You are the owner")

    room_requests, _ = ChatRoomRequest.objects.get_or_create(room=room)
    if (
        request.user.profile in room_requests.users.all()
        and room.owner != request.user.profile
    ):
        room_requests.users.remove(request.user.profile)
        room_requests.save()
        return redirect("home")

    room_requests.users.add(request.user.profile)
    room_requests.save()

    return redirect("home")


@login_required(login_url="login")
def accept_room_request(request, room_name, username):
    room = ChatRoom.objects.filter(room=room_name).first()
    user = Profile.objects.filter(username=username).first()

    if room.owner != request.user.profile:
        return HttpResponse("owner only")

    if room == None:
        return HttpResponse("Room dose not exists")
    if user == None:
        return HttpResponse("User dose not exists")

    if user not in room.members.all():
        room.members.add(user)
        room.chat_room_requests.users.remove(user)
        room.save()

    return redirect("home")


@login_required(login_url="login")
def remove_user(request, room_name, username):
    room = ChatRoom.objects.filter(room=room_name).first()
    user = Profile.objects.filter(username=username).first()

    if room.owner != request.user.profile:
        return HttpResponse("owner only")

    if room == None:
        return HttpResponse("Room dose not exists")
    if user == None:
        return HttpResponse("User dose not exists")

    if user in room.members.all():
        room.members.remove(user)
        room.save()

    return redirect("home")


@login_required(login_url="login")
def exit_room(request, room_name):
    room = ChatRoom.objects.filter(room=room_name).first()

    if room == None:
        return HttpResponse("Room dose not exists")

    if room.owner == request.user.profile:
        room.delete()
        return redirect("home")
    else:
        if request.user.profile in room.members.all():
            room.members.remove(request.user.profile)
            room.save()
            return redirect("home")


@login_required(login_url="login")
def chat(request, username):
    user = Profile.objects.filter(username=username).first()

    if user == None:
        return HttpResponse("User dose not exists")

    try:
        thread = Chat.objects.get(room=f"chat-{request.user.profile.id}-{user.id}")
    except:
        thread, _ = Chat.objects.get_or_create(
            room=f"chat-{user.id}-{request.user.profile.id}"
        )

    mesages = ChatMessage.objects.filter(chat=thread)

    context = {"user": user, "messages": mesages}

    return render(request, "chat/message.html", context)
