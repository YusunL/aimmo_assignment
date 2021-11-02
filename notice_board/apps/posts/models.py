from django.db import models
from apps.users.models import User


class Post(models.Model):
    """Custom Post Model"""

    title = models.CharField(max_length=100)
    content = models.TextField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
