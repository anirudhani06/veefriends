from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import PostForm
from chat.forms import RoomForm
from chat.models import ChatRoom, ChatMessage, Chat
from .models import Post, Comment, Bookmark, Activity
from django.db.models import Q, Prefetch
from accounts.models import Profile
from django.http import JsonResponse
from django.http import HttpResponse

# Create your views here.


@login_required(login_url="login")
def home(request):
    user = request.user.profile
    friends = user.following.values_list("id")
    all_posts = Post.objects.select_related("owner").filter(
        Q(owner=user) | Q(owner__in=friends)
    )

    chat_messages = ChatMessage.objects.filter(user=user)
    all_chats = []

    for msg in chat_messages:
        all_chats.append(msg.chat.room)

    my_rooms = ChatRoom.objects.filter(Q(members=user))

    bookmark, _ = Bookmark.objects.get_or_create(user=request.user.profile)

    context = {
        "posts": all_posts,
        "my_rooms": my_rooms,
        "bookmark": bookmark,
        "user": user,
        "chat_messages": all_chats,
    }
    return render(request, "posts/home.html", context)


@csrf_exempt
@login_required(login_url="login")
def create_post(request):
    user = request.user.profile
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = user
            post.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "posts/create_post.html", context)


@login_required(login_url="login")
def delete_post(request, post_id):
    post = Post.objects.filter(id=post_id).first()

    if post == None:
        return HttpResponse("Post dose not exists")

    if post.owner != request.user.profile:
        return HttpResponse("You can't delete this post")

    if request.user.profile == post.owner:
        post.delete()
        return redirect("home")


@login_required(login_url="login")
def view_post(request, post_id):
    user = request.user.profile
    post = Post.objects.get(id=post_id)
    bookmark, _ = Bookmark.objects.get_or_create(user=user)
    if not post.impressions.filter(id=user.id).exists():
        post.impressions.add(user)
        post.save()

    context = {"post": post, "user": user, "bookmark": bookmark}
    return render(request, "posts/post.html", context)


@csrf_exempt
@login_required(login_url="login")
def update_post(request, post_id):
    user = request.user.profile
    post = Post.objects.filter(id=post_id).first()

    if post is None:
        return HttpResponse("Post not fount!")

    if user != post.owner:
        return HttpResponse("You can't update this post!")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("view_post", post_id=post_id)

    context = {"post": post}
    return render(request, "posts/update_post.html", context)


@csrf_exempt
@login_required(login_url="login")
def like_post(request):
    post = Post.objects.get(id=request.POST.get("id"))
    user = request.user.profile

    if not post.likes.filter(id=user.id).exists():
        post.likes.add(user)
        post.save()
        like_count = post.likes.count()
        return JsonResponse({"data": True, "count": like_count})
    else:
        post.likes.remove(user)
        post.save()
        like_count = post.likes.count()
        return JsonResponse({"data": False, "count": like_count})


@csrf_exempt
@login_required(login_url="login")
def add_comment(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        comment = request.POST.get("comment")
        post = Post.objects.get(id=post_id)
        Comment.objects.create(owner=request.user.profile, post=post, body=comment)

        return redirect("view_post", post_id=post_id)


@login_required(login_url="login")
def search(request):
    user = request.user.profile
    q = request.GET.get("q") if request.GET.get("q") is not None else " "
    users = Profile.objects.filter(
        Q(username__startswith=q) | Q(name__startswith=q)
    ).exclude(id=request.user.profile.id)
    posts = Post.objects.filter(Q(body__icontains=q))
    room_list = ChatRoom.objects.filter(Q(room__icontains=q))
    bookmark, _ = Bookmark.objects.select_related("user").get_or_create(user=user)
    context = {
        "user": user,
        "users": users,
        "posts": posts,
        "room_list": room_list,
        "bookmark": bookmark,
    }

    return render(request, "posts/search.html", context)


@login_required(login_url="login")
def bookmark(request):
    user = request.user.profile
    bookmark, _ = Bookmark.objects.get_or_create(user=user)
    context = {"bookmark": bookmark}
    return render(request, "posts/bookmark.html", context)


@csrf_exempt
@login_required(login_url="login")
def add_to_bookmark(request):
    if request.method == "POST":
        user = request.user.profile
        post = Post.objects.get(id=request.POST.get("id"))
        bookmark, _ = Bookmark.objects.get_or_create(user=user)

        if not Bookmark.objects.filter(user=user, post=post).exists():
            bookmark.post.add(post)
            bookmark.save()
            return JsonResponse({"data": True})
        else:
            bookmark.post.remove(post)
            bookmark.save()
            return JsonResponse({"data": False})
