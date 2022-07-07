from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.posts, name="posts"),
    path("following", views.following, name="following"),
    path("likes_api/<int:post_id>", views.likes_api, name="likes_api"),
    path("dislikes_api/<int:post_id>", views.dislikes_api, name="dislikes_api"),
    path("follow_api", views.follow_api, name="follow_api"),
    path("unfollow_api", views.unfollow_api, name="unfollow_api"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<str:user>/", views.profile, name="profile"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
]
