from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post, Author
from .tasks import send_created_news


@receiver(post_save, sender=Post)
def post_created(sender, instance, created, **kwargs):
    if created:
        send_created_news.delay(instance.pk)


@receiver(post_save, sender=User)
def create_author(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_author(sender, instance, **kwargs):
    instance.author.save()
