import json

from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import PostForm
from .models import Dislikes, Followers, Likes, Posts, User


def index(request):

    post_obj = Posts.objects.all()
    paginator = Paginator(post_obj, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "user": request.user,
        "post": Posts.objects.get(id=1),
        "page_obj": page_obj,
        "post_obj": post_obj,
    }
    return render(request, "network/index.html", context=context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {"message": "Invalid username and/or password."})
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {"message": "Passwords must match."})

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {"message": "Username already taken."})
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def posts(request):
    return {"posts": Posts.objects.all().order_by("-created_at")}


def likes_api(request, post_id):

    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get("user_id")
        post = Posts.objects.get(pk=post_id)
        user = User.objects.get(pk=user_id)
        likes = Likes.objects.filter(post_id=post_id).all().count()
        dislikes = Dislikes.objects.filter(post_id=post_id).all().count()

        # Check if user has already liked post
        if Likes.objects.filter(post_id=post, user_id=user).exists():
            return JsonResponse({"success": False, "likes": likes, "dislikes": dislikes})
        elif Dislikes.objects.filter(post_id=post, user_id=user).exists():
            obj = Dislikes.objects.filter(post_id=post, user_id=user)
            obj.delete()
            Likes.objects.create(post_id=post, user_id=user)
            return JsonResponse({"success": True, "likes": likes + 1, "dislikes": dislikes - 1})
        else:
            Likes.objects.create(post_id=post, user_id=user)
            return JsonResponse({"success": True, "likes": likes + 1, "dislikes": dislikes})
    else:
        return JsonResponse({"success": False})


def dislikes_api(request, post_id):

    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get("user_id")
        post = Posts.objects.get(pk=post_id)
        user = User.objects.get(pk=user_id)
        dislikes = Dislikes.objects.filter(post_id=post_id).all().count()
        likes = Likes.objects.filter(post_id=post_id).all().count()

        # Check if user has already liked/disliked post
        if Dislikes.objects.filter(post_id=post, user_id=user).exists():
            return JsonResponse({"success": False, "dislikes": dislikes, "likes": likes})

        elif Likes.objects.filter(post_id=post, user_id=user).exists():
            obj = Likes.objects.filter(post_id=post, user_id=user)
            obj.delete()
            Dislikes.objects.create(post_id=post, user_id=user)
            return JsonResponse({"success": True, "dislikes": dislikes + 1, "likes": likes - 1})

        else:
            Dislikes.objects.create(post_id=post, user_id=user)
            return JsonResponse({"success": True, "dislikes": dislikes + 1, "likes": likes})
    else:
        return JsonResponse({"success": False})


def follow_api(request):

    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        following_user_id = data.get("following_user_id")
        user = User.objects.get(username=username)
        follower = User.objects.get(pk=following_user_id)
        followers = Followers.objects.filter(user_id=user).count()
        following = Followers.objects.filter(following_user_id=user).count()

        if Followers.objects.filter(following_user_id=follower, user_id=user).exists():
            return JsonResponse(
                {"success": False, "followers": followers, "following": following, "is_following": True}
            )
        else:
            Followers.objects.create(following_user_id=follower, user_id=user)
            return JsonResponse(
                {"success": True, "followers": followers + 1, "following": following, "is_following": True}
            )
    return JsonResponse({"Success": False})


def unfollow_api(request):

    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        following_user_id = data.get("following_user_id")
        user = User.objects.get(username=username)
        follower = User.objects.get(pk=following_user_id)
        followers = Followers.objects.filter(user_id=user).count()
        following = Followers.objects.filter(following_user_id=user).count()

        if Followers.objects.filter(following_user_id=follower, user_id=user).exists():
            obj = Followers.objects.filter(following_user_id=follower, user_id=user)
            obj.delete()
            return JsonResponse(
                {"success": True, "followers": followers - 1, "following": following, "is_following": False}
            )
        else:
            return JsonResponse(
                {"success": False, "followers": followers, "following": following, "is_following": False}
            )
    return JsonResponse({"Success": False})


def new_post(request):

    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            user = request.user
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            post = Posts.objects.create(user_id=user, title=title, content=content)
            post.save()
            return HttpResponseRedirect(reverse("index"))

    form = PostForm()
    return render(request, "network/new_post.html", {"form": form})


def edit_post(request, post_id):

    if request.method == "POST":
        data = json.loads(request.body)
        data = json.loads(data)
        # user = data.get("user_id")
        content = data.get("content")
        post = Posts.objects.get(id=post_id)
        post.content = content
        post.save()
        return JsonResponse({"status": "success"})


def profile(request, user):

    req_user = request.user
    page_number = request.GET.get("page")
    user_obj = User.objects.filter(username=user).first()
    post_obj = Posts.objects.filter(user_id=user_obj.id)
    paginator = Paginator(post_obj, 4)
    page_obj = paginator.get_page(page_number)
    is_following = Followers.objects.filter(user_id=user_obj, following_user_id=req_user)

    # Check if profile is current user
    is_current_user = req_user == user_obj

    followers = Followers.objects.filter(user_id=user_obj).count()
    following = Followers.objects.filter(following_user_id=user_obj).count()

    context = {
        "page_obj": page_obj,
        "post_obj": post_obj,
        "user_obj": user_obj,
        "following": following,
        "is_following": is_following,
        "followers": followers,
        "is_current_user": is_current_user,
    }
    return render(request, "network/profile.html", context)


def following(request):

    obj = Followers.objects.filter(following_user_id=request.user.id).all()

    # Get all users that current user is following
    following_id = []
    for item in obj:
        following_id.append(item.user_id.id)

    user = request.user
    post_obj = Posts.objects.filter(user_id__in=following_id)
    paginator = Paginator(post_obj, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "user": request.user,
        "page_obj": page_obj,
        "post_obj": post_obj,
    }
    return render(request, "network/following.html", context=context)
