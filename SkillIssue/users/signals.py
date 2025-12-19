from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Profile, GuideRating, Announcement, UserActivity, Guide


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

@receiver(post_save, sender=Guide)
def log_guide_creation_update(sender, instance, created, **kwargs):
    """
    Логирует создание или обновление руководства.
    """
    action = 'CREATE' if created else 'UPDATE'
    UserActivity.objects.create(
        user=instance.author,
        action=action,
        target_type='GUIDE',
        target_title=instance.title,
        guide=instance  # Опциональная ссылка на объект
    )


@receiver(post_delete, sender=Guide)
def log_guide_deletion(sender, instance, **kwargs):
    """
    Логирует удаление руководства.
    Сохраняет название, даже если объект уже удалён из БД.
    """
    UserActivity.objects.create(
        user=instance.author,
        action='DELETE',
        target_type='GUIDE',
        target_title=instance.title
        # Поле 'guide' остаётся null, так как объект удалён
    )


@receiver(post_save, sender=Announcement)
def log_announcement_creation_update(sender, instance, created, **kwargs):
    """
    Логирует создание или обновление объявления.
    """
    action = 'CREATE' if created else 'UPDATE'
    UserActivity.objects.create(
        user=instance.author,
        action=action,
        target_type='ANNOUNCEMENT',
        target_title=instance.title,
        announcement=instance  # Опциональная ссылка
    )


@receiver(post_delete, sender=Announcement)
def log_announcement_deletion(sender, instance, **kwargs):
    """
    Логирует удаление объявления.
    """
    UserActivity.objects.create(
        user=instance.author,
        action='DELETE',
        target_type='ANNOUNCEMENT',
        target_title=instance.title
    )