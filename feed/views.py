from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CommentForm, PostForm, ProfileForm, RegisterForm
from .models import Post


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.save())
        return redirect("feed")
    return render(request, "registration/register.html", {"form": form})


@login_required
def feed(request):
    """Posts from people I follow, plus my own."""
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("feed")
    else:
        form = PostForm()
    ids = list(request.user.profile.following.values_list("user_id", flat=True)) + [request.user.id]
    posts = Post.objects.filter(author_id__in=ids).select_related("author__profile").prefetch_related("likes", "comments")
    return render(request, "feed.html", {"posts": posts, "form": form, "title": "Home"})


@login_required
def explore(request):
    posts = Post.objects.select_related("author__profile").prefetch_related("likes", "comments")
    people = User.objects.exclude(pk=request.user.pk).select_related("profile")[:20]
    return render(request, "feed.html", {"posts": posts, "people": people, "title": "Explore"})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post.objects.select_related("author__profile"), pk=pk)
    form = CommentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        c = form.save(commit=False)
        c.post, c.author = post, request.user
        c.save()
        return redirect("post_detail", pk=pk)
    return render(request, "post_detail.html", {"post": post, "form": form})


@login_required
@require_POST
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.delete()
    messages.success(request, "Post deleted.")
    return redirect("feed")


@login_required
@require_POST
def like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(pk=request.user.pk).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"liked": liked, "count": post.likes.count()})
    return redirect(request.META.get("HTTP_REFERER", "feed"))


@login_required
def profile(request, username):
    owner = get_object_or_404(User.objects.select_related("profile"), username=username)
    posts = owner.posts.prefetch_related("likes", "comments")
    return render(request, "profile.html", {
        "owner": owner,
        "posts": posts,
        "is_following": request.user.profile.following.filter(pk=owner.profile.pk).exists(),
    })


@login_required
@require_POST
def follow_toggle(request, username):
    target = get_object_or_404(User, username=username)
    if target == request.user:
        messages.error(request, "You can't follow yourself.")
    else:
        me = request.user.profile
        if me.following.filter(pk=target.profile.pk).exists():
            me.following.remove(target.profile)
        else:
            me.following.add(target.profile)
    return redirect("profile", username=username)


@login_required
def profile_edit(request):
    form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user.profile
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("profile", username=request.user.username)

    return render(request, "profile_edit.html", {"form": form})