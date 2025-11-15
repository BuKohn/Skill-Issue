from django.contrib import admin
from .models import Profile, Guide, Review, GuideRating


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "rating")
    list_filter = ("created_at", "author")
    search_fields = ("title", "content", "author__username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "rating", "created_at")
    search_fields = ("user__username",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("guide", "author", "stars", "created_at")
    list_filter = ("stars", "created_at")
    search_fields = ("guide__title", "author__username", "text")


@admin.register(GuideRating)
class GuideRatingAdmin(admin.ModelAdmin):
    list_display = ("guide", "reviewer", "rating", "created_at")
    list_filter = ("rating",)

