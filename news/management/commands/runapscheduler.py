import logging
import datetime

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.models import User, Post


logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=7)


    for u in User.objects.all():

            list_of_posts = Post.objects.filter(createTime__range=(start_date, end_date),
                                                )
            full_url = ''.join(['http://', get_current_site(None).name, ':8000'])
            html_content = render_to_string(
                'news/week_mail.html',
                {
                    'news': list_of_posts,
                    'usr': u,
                    'full_url': full_url,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'Здравствуй, Мы подготовили дайджест статей за неделю с нашего портала!',
                body='',

                from_email='',
                to=[f'{u.email}'],  # это то же, что и recipients_list
                                      )
            msg.attach_alternative(html_content, "text/html")  # добавляем html

            msg.send()  # отсылаем
            print(list_of_posts)
            #print(full_url)

# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day="*/7"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
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