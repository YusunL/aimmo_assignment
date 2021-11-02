from django.db import models


class User(models.Model):
    """custom simplified user model"""

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name}"
