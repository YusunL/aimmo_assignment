from django.db import models
from apps.users.models import User


class Category(models.Model):
    name = models.CharField(default="", max_length=50)


class Post(models.Model):
    """Custom Post Model"""

    title = models.CharField(max_length=100)
    body = models.TextField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    hit = models.IntegerField(default=0)


class Comment(models.Model):
    """Custom Comment Model"""

    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class NestedComment(models.Model):
    """Custom Nested-comment Model"""

    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    comment = models.ForeignKey(Comment, on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
