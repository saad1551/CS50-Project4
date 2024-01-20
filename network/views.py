from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Post, Follow, Like


def index(request):
    if request.method == "POST":
        if request.POST.get('text'):
            post_text = request.POST['text']
            p = Post(user = request.user, text = post_text)
            p.save()
            return HttpResponseRedirect(reverse("index"))
        # elif request.POST.get('like'):
        #     post_to_like = Post.objects.get(id=int(request.POST['like']))
        #     l = Like(post = post_to_like, user = request.user)
        #     l.save()
        # elif request.POST.get('unlike'):
        #     post_to_unlike = Post.objects.get(id=int(request.POST['unlike']))
        #     l = Like.objects.get(post = post_to_unlike, user = request.user)
        #     l.delete()
        elif request.POST.get('edit'):
            post_id = request.POST['editPostID']
            edited_text = request.POST['edit']
            post_to_edit = Post.objects.get(id = post_id)
            post_to_edit.text = edited_text
            post_to_edit.save()
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_no = request.GET.get('page')
    page_obj = paginator.get_page(page_no)
    return render(request, "network/index.html", {
        "page_obj": page_obj
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
        "profile_posts": Post.objects.filter(user = user.id).order_by('-timestamp'),
        "follow": bool(not user.followers.filter(follower=request.user).exists())
    })

def following(request):
    followed_users = request.user.following.all().values_list('followed', flat=True)
    posts = []
    for followed_user in followed_users:
        user_posts = Post.objects.filter(user = followed_user)
        for user_post in user_posts:
            posts.append(user_post)
    posts = sorted(posts, key= lambda x:x.timestamp, reverse=True)
    paginator = Paginator(posts, 10)
    page_no = request.GET.get('page')
    page_obj = paginator.get_page(page_no)
    return render(request, "network/index.html", {
        "page_obj": page_obj
    })

def edit(request, postID):
    if request.method == 'POST':
        post_to_edit = Post.objects.get(id = int(postID))
        post_to_edit.text = request.POST["edited_text"]
        post_to_edit.save()
        return HttpResponseRedirect(reverse(index))
    return render(request, "network/edit.html", {
        "post": Post.objects.get(id = int(postID))
    })

@csrf_exempt
def like(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    post_to_like = Post.objects.get(id = int(data.get('postID')))
    liker = User.objects.get(username = data.get('liker'))

    if data.get('operation') == 'like':
        try:
            l = Like(post = post_to_like, user = liker)
        except:
            return JsonResponse({"message": "failure"}, status=201)

        l.save()
    
    elif data.get('operation') == 'unlike':
        try:
            l = Like.objects.get(post = post_to_like, user = liker)
        except:
            return JsonResponse({"message": "failure"}, status=201)
        
        l.delete()

    return JsonResponse({"message": "success."}, status=201)