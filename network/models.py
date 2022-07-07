from calendar import c
from os import times
from re import L, M, U
from abc import ABC, abstractmethod
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone


class User(AbstractUser):
    __tablename__ = "user"

    def get_followers(self):
        return self.followers.all()

    def get_following(self):
        return self.following.all()

    def __str__(self):
        return f"{self.username}, #{self.id}"


class Posts(models.Model):
    __tablename__ = "posts"

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Posts"
        ordering = ["-created_at"]

    def get_like_count(self):
        # return Likes.objects.filter(post=self).count()
        return self.likes.count()

    def get_comments(self):
        # return Comments.objects.filter(post=self)
        return self.comments.all()

    # @abstractmethod
    # def get_following_posts(self, users):
    #     return Posts.objects.filter(user__in=users).order_by("-created_at")

    def get_absolute_url(self):
        return reverse("listing_detail", args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.user_id.username}")
        if not self.created_at:
            self.created_at = timezone.now()
        if not self.updated_at:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class Followers(models.Model):
    __tablename__ = "followers"

    user_id = models.ForeignKey("User", related_name="followed", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey("User", related_name="following", on_delete=models.CASCADE)
    # posts_ref = models.ManyToManyField(Posts, related_name="posts")

    # @classmethod
    # def get_following_posts(self):
    #     return self.following_user_id.posts.all()

    # following_user_id = models.ManyToManyField(User, related_name="following")
    # posts_ref = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="posts", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Followers"

    def __str__(self):
        return f" {self.following_user_id} follows {self.user_id} "


class Comments(models.Model):
    __tablename__ = "comments"

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"{self.user} said {self.comment}"


class Likes(models.Model):
    __tablename__ = "likes"

    user_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="likes")
    post_id = models.ForeignKey("Posts", on_delete=models.CASCADE, related_name="likes")

    class Meta:
        verbose_name_plural = "Likes"

    def __str__(self):
        return f"{self.user_id} liked {self.post_id}"


class Dislikes(models.Model):
    __tablename__ = "dislikes"

    user_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="dislikes")
    post_id = models.ForeignKey("Posts", on_delete=models.CASCADE, related_name="dislikes")

    class Meta:
        verbose_name_plural = "Dislikes"

    def __str__(self):
        return f"{self.user_id} disliked {self.post_id}"
