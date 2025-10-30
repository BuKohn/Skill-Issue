from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Guide(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guides')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='guides/', blank=True, null=True)
    tags = models.JSONField(blank=True, default=list)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    stars = models.PositiveSmallIntegerField(default=5)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review({self.author.username} → {self.guide.title})"


class GuideRating(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name="ratings")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="guide_ratings")
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('guide', 'reviewer')

    def __str__(self):
        return f"{self.reviewer.username} → {self.guide.title}: {self.rating}"
