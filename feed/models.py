from django.conf import settings
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    bio = models.CharField(max_length=280, blank=True)
    avatar_url = models.URLField(blank=True)
    cover_url = models.URLField(blank=True)

    avatar_image = models.ImageField(
        upload_to="profiles/avatars/",
        blank=True,
        null=True
    )

    cover_image = models.ImageField(
        upload_to="profiles/covers/",
        blank=True,
        null=True
    )

    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followers",
        blank=True
    )

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("profile", args=[self.user.username])


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    content = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_posts",
        blank=True
    )

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{self.author}: {self.content[:30]}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    content = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created"]