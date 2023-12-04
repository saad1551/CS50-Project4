from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Follow


def index(request):
    if request.method == "POST":
        post_text = request.POST['text']
        p = Post(user = request.user, text = post_text)
        p.save()
        return HttpResponseRedirect(reverse("index"))
    posts = Post.objects.all().order_by('-timestamp')
    return render(request, "network/index.html", {
        "posts": posts
    })


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    

def profile(request, name):
    if request.method == "POST":
        if request.POST.get('follow'):
            f = Follow(follower=request.user, followed=User.objects.get(username=name))
            f.save()
        elif request.POST.get('unfollow'):
            f = Follow.objects.get(follower=request.user, followed=User.objects.get(username=name))
            f.delete()
        return HttpResponseRedirect(reverse("profile", kwargs={
            "name": name
        }))
    user = User.objects.get(username = name)
    return render(request, "network/profile.html", {
        "profile": user,
        "follow": bool(not request.user in user.followers.all())
    })

def following(request):
    followed_users = request.user.following.all().values_list('followed')
    posts = []
    for followed_user in followed_users:
        user_posts = Post.objects.filter(user = followed_user[0])
        for user_post in user_posts:
            posts.append(user_post)
    return render(request, "network/index.html", {
        "posts": posts
    })

