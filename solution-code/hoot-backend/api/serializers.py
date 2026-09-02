from django.contrib.auth.models import User
from .models import Comment, Hoot

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    _id = serializers.CharField(source="pk", read_only=True)

    class Meta:
        model = User
        fields = ["_id", "username"]


class CommentSerializer(serializers.ModelSerializer):
    _id = serializers.CharField(source="pk", read_only=True)
    author = UserSerializer(read_only=True)
    createdAt = serializers.DateTimeField(
        source="created_at",
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ["_id", "text", "author", "createdAt"]


class HootSerializer(serializers.ModelSerializer):
    _id = serializers.CharField(source="pk", read_only=True)
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    createdAt = serializers.DateTimeField(
        source="created_at",
        read_only=True
    )

    class Meta:
        model = Hoot
        fields = ["_id", "title", "text", "category", "author",
        "comments", "createdAt"]