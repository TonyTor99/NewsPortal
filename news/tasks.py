from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

from .models import Post, Subscription


@shared_task
def send_created_news(post_pk):
    post = Post.objects.get(pk=post_pk)
    post_cat = post.category.values_list('id', flat=True)
    subs = Subscription.objects.filter(category__in=post_cat).values_list('id', flat=True)

    emails = set()
    for sub in subs:
        email = User.objects.filter(id=sub).values_list('email', flat=True)
        emails.update(email)

    subject = f'Новый пост в ваших категориях'

    text_content = (
        f'Заголовок: {post.title}\n\n'
        f'Preview: \n{post.text[:150]}\n\n'
        f'Ссылка на пост: http://127.0.0.1:8000{post.get_absolute_url()}'
    )
    html_content = (
        f'Заголовок: {post.title}<br><br>'
        f'Preview: <br>{post.text[:150]}<br><br>'
        f'<a href="http://127.0.0.1{post.get_absolute_url()}">'
        f'Ссылка на пост</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

