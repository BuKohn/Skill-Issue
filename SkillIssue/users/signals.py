from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import GuideRating
from .models import Profile


@receiver([post_save, post_delete], sender=GuideRating)
def update_profile_rating(sender, instance, **kwargs):
    guide = instance.guide
    author = guide.author

    try:
        profile = author.profile
    except Profile.DoesNotExist:
        return

    avg_rating = GuideRating.objects.filter(
        guide__author=author
    ).aggregate(Avg('rating'))['rating__avg']

    profile.rating = round(avg_rating or 0.00, 2)
    profile.save(update_fields=['rating'])