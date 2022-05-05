from datetime import datetime

from celery import shared_task
import time

from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post


@shared_task
def SendEmail():
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
            subject=f'Здравствуй, Мы подготовили дайджест статей за неделю с нашего портала! Redis task',
            body='',

            from_email='',
            to=[f'{u.email}'],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем
        print(list_of_posts)