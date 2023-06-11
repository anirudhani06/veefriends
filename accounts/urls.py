from django.urls import path
from . import views

urlpatterns = [
    path("login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    path("register", views.user_register, name="register"),
    path("validate-user/<uidb64>/<token>/", views.validate_user, name="validate_user"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("settings", views.settings, name="settings"),
    path("notifications", views.notifications, name="notifications"),
    path("follow/<str:user_id>", views.follow, name="follow"),
    path("followers", views.followers, name="followers"),
    path("followings", views.followings, name="followings"),
    path(
        "change-password",
        views.PasswordChangeView.as_view(template_name="user/change_password.html"),
        name="change_password",
    ),
]
