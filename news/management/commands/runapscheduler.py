import logging
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from news.models import Subscription, Post

logger = logging.getLogger(__name__)


def my_job():
    now = timezone.now()
    last_week = now - timezone.timedelta(weeks=1)
    subscribers = Subscription.objects.all()

    for sub in subscribers:

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


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week='fri', hour=18, minute=0),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
