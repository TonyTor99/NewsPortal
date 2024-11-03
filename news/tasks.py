from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

from .models import Post, Subscription


@shared_task
def send_created_news(post_pk):
    post = Post.objects.get(pk=post_pk)
    post_cat = post.category.values_list('id', flat=True)
    subs = Subscription.objects.filter(category__in=post_cat).values_list('user_id', flat=True)

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
        f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">'
        f'Ссылка на пост</a>'
    )

    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def send_last_week_posts():
    now = timezone.now()
    last_week = now - timezone.timedelta(weeks=1)
    subs = Subscription.objects.all()

    for sub in subs:

        new_posts = Post.objects.filter(category=sub.category, time_in__gte=last_week)

        if new_posts.exists():
            news_links = "\n".join(
                [f"{post.title}:http://127.0.0.1:8000{post.get_absolute_url()}" for post in new_posts]
            )

            html_links = '<br>'.join(
                [f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">{post.title}<a/>' for post in
                 new_posts]
            )

            subject = f'Новые посты за неделю в категории: {sub.category.cat_name}'
            text_message = f'Ссылки на посты:\n {news_links}'
            html_message = f'<h1>Ссылки на посты:</h1><br>{html_links}'

            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_message,
                from_email=None,
                to=[sub.user.email]
            )
            msg.attach_alternative(html_message, 'text/html')
            msg.send()
