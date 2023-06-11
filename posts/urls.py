from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create-post/", views.create_post, name="create_post"),
    path("delete-post/<str:post_id>/", views.delete_post, name="delete_post"),
    path("post/<str:post_id>/", views.view_post, name="view_post"),
    path("update-post/<str:post_id>/", views.update_post, name="update_post"),
    path("like-post", views.like_post, name="like_post"),
    path("comment-post", views.add_comment, name="comment_post"),
    path("search/", views.search, name="search"),
    path("bookmark/", views.bookmark, name="bookmark"),
    path("add-bookmark", views.add_to_bookmark, name="add_to_bookmark"),
]
