from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterForm, UpdateUserForm, ChangePassword
from .decorators import is_unauthenticated
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import email_verification
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from chat.models import ChatRoom
from .models import Profile
from posts.models import Post, Bookmark
from chat.models import ChatRoomRequest
from django.utils.decorators import method_decorator
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.


@is_unauthenticated
def validate_user(request, uidb64, token):
    try:
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(id=user_id)
    except:
        user = None

    if user is not None and email_verification.check_token(user, token):
        user.is_active = True
        user.save()

        return redirect("login")

    else:
        return HttpResponse("Invalid url")


@is_unauthenticated
def validate_email(request, user, to_email):
    user = get_user_model().objects.filter(email=to_email).first()
    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
    token = email_verification.make_token(user)
    domain = get_current_site(request).domain
    protocol = "http"

    url = f"{protocol}://{domain}/user/validate-user/{uidb64}/{token}/"

    return render(request, "email/email_send.html", {"url": url})


@csrf_exempt
@is_unauthenticated
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        messages.error(request, "User dose not found!")

    return render(request, "user/login.html")


@csrf_exempt
@is_unauthenticated
def user_register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.name = user.name.capitalize()
            user.is_active = False
            user.save()

            return validate_email(request, user, form.cleaned_data["email"])

    context = {"form": form}
    return render(request, "user/register.html", context)


def user_logout(request):
    logout(request)

    return redirect("home")


@login_required(login_url="login")
def profile(request, username):
    try:
        user = Profile.objects.get(username=username)
    except:
        user = None

    if user == None:
        return HttpResponse("User dose not exists!")

    posts = Post.objects.select_related("owner").filter(owner=user)
    bookmark, _ = Bookmark.objects.select_related("user").get_or_create(
        user=request.user.profile
    )

    context = {"user": user, "posts": posts, "bookmark": bookmark}
    return render(request, "user/profile.html", context)


@csrf_exempt
@login_required(login_url="login")
def settings(request):
    user = request.user.profile
    chat_rooms = ChatRoom.objects.select_related("owner").filter(owner=user)
    if request.method == "POST":
        form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form = form.save(commit=False)
            form.username = form.username.lower()
            form.name = form.name.capitalize()
            form.save()
            return redirect("profile", user.username)
    else:
        form = UpdateUserForm(instance=user)
    context = {"user": user, "form": form, "chat_rooms": chat_rooms}
    return render(request, "user/settings.html", context)


@login_required(login_url="login")
def notifications(request):
    rooms = ChatRoom.objects.filter(owner=request.user.profile)
    chat_room_requests = ChatRoomRequest.objects.filter(room__in=rooms)

    all_notifications = []
    context = {"all_notifications": chat_room_requests}
    return render(request, "user/notification.html", context)


@login_required(login_url="login")
def follow(request, user_id):
    user = request.user.profile
    follower = Profile.objects.get(id=user_id)

    if user != follower:
        if (
            user not in follower.followers.all()
            and follower not in user.following.all()
        ):
            follower.followers.add(user)
            follower.save()
            user.following.add(follower)
            user.save()
        else:
            follower.followers.remove(user)
            follower.save()
            user.following.remove(follower)
            user.save()

    return redirect("home")


@login_required(login_url="login")
def followers(request):
    user = request.user.profile
    user_followers = user.followers.all()
    context = {"followers": user_followers}
    return render(request, "user/followers.html", context)


@login_required(login_url="login")
def followings(request):
    user = request.user.profile
    user_followings = user.following.all()
    context = {"followings": user_followings}
    return render(request, "user/followings.html", context)


@method_decorator(login_required(login_url="login"), name="dispatch")
class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("home")
