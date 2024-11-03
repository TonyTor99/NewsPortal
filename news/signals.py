from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post
from .tasks import send_created_news


@receiver(post_save, sender=Post)
def post_created(sender, instance, created, **kwargs):
    if created:
        send_created_news.delay(instance.pk)
