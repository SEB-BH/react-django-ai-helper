from django.db import models
from django.contrib.auth.models import User

class Hoot(models.Model):
    CATEGORY_CHOICES = [
        ("News", "News"),
        ("Sports", "Sports"),
        ("Games", "Games"),
        ("Movies", "Movies"),
        ("Music", "Music"),
        ("Television", "Television"),
        ("Other", "Other"),
    ]

    title = models.CharField(max_length=100)
    text = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="News"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="hoots", 
    )

    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title



class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    hoot = models.ForeignKey(
        Hoot,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.text[:40]