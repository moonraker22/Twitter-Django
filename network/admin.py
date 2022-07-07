from calendar import c
from re import L
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Posts, Comments, Followers, Likes, Dislikes


admin.site.register(User, UserAdmin)
admin.site.site_header = "Zwitter"
admin.site.site_title = "Zwitter"
admin.site.index_title = "Zwitter"


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ("user_id", "title", "content", "created_at", "updated_at")
    list_display_links = ("user_id", "title")
    list_filter = ("user_id", "created_at", "updated_at")
    search_fields = ("title", "content", "user_id")
    list_per_page = 25
    prepopulated_fields = {"slug": ("title", "user_id")}


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    # list_display = ("user_id", "comment", "timestamp")
    # list_display_links = ("user_id", "comment")
    # list_filter = ("user_id", "timestamp")
    # search_fields = ("user_id", "comment")
    list_per_page = 25


@admin.register(Followers)
class FollowersAdmin(admin.ModelAdmin):
    # list_display = ("user_id", "following_user_id")
    plural = "Followers"


@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    list_display = ("user_id", "post_id")


@admin.register(Dislikes)
class DisLikesAdmin(admin.ModelAdmin):
    list_display = ("user_id", "post_id")
