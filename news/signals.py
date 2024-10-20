from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post, Subscription


@receiver(post_save, sender=Post)
def post_created(instance, created, **kwargs):
    if not created:
        return

    categories = instance.category.all()

    print('***********************')
    print(categories)
    print('***********************')

    subscribers = Subscription.objects.filter(
        category__in=categories
    ).values_list('user', flat=True)

    print('!!!!!!!!!!!!!!!!!!!!!!')
    print(subscribers)
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!')

    emails = set()
    for sub in subscribers:
        email_ = User.objects.filter(
            id=sub
        ).values_list('email', flat=True)
        emails.update(email_)

    print('---------------------------------')
    print(emails)
    print('----------------------------------')
    subject = f'Новый пост в категории {instance.category}'

    text_content = (
        f'Заголовок: {instance.title}\n\n'
        f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Заголовок: {instance.title}<br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на пост</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
