from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Review, Guide


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"]
        )
        UserProfile.objects.create(user=user)
        return user


class ReviewSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "author_username", "text", "stars", "created_at"]


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    rating = serializers.FloatField(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    guides = serializers.SerializerMethodField()  # <-- добавляем guides

    class Meta:
        model = UserProfile
        fields = ["username", "avatar", "bio", "rating", "reviews", "guides"]

    def get_guides(self, obj):
        guides = Guide.objects.filter(author=obj.user).order_by('-created_at')
        return GuideSerializer(guides, many=True).data


class GuideSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Guide
        fields = ['id', 'title', 'content', 'image', 'tags', 'rating', 'author_name', 'created_at']