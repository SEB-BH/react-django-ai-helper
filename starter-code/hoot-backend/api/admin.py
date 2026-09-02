from django.contrib import admin

from .models import Comment, Hoot

@admin.register(Hoot)
class HootAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "author", "created_at"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["text", "author", "hoot", "created_at"]