from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory, Subscription


@receiver(m2m_changed, sender=PostCategory)
def post_created(sender, instance, **kwargs):
    if not kwargs['action'] == 'post_add':
        return

    categories = instance.category.all()
    subscribers = Subscription.objects.filter(
        category__in=categories
    ).values_list('user', flat=True)

    emails = set()
    for sub in subscribers:
        email_ = User.objects.filter(
            id=sub
        ).values_list('email', flat=True)
        emails.update(email_)

    subject = f'Новый пост в ваших категориях'

    text_content = (
        f'Заголовок: {instance.title}\n\n'
        f'Preview: \n{instance.text[:150]}\n\n'
        f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Заголовок: {instance.title}<br><br>'
        f'Preview: <br>{instance.text[:150]}<br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на пост</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
