from celery import shared_task
from .models import Post, Category
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import datetime


@shared_task
def notify_subscribers(post_id):
    post = Post.objects.get(pk=post_id)
    categories = post.category.all()
    subscribers = list()
    for cat in categories:
        cat_subs = cat.subscribers.all()
        subscribers += list(cat_subs)

    for user in set(subscribers):
        html_content = render_to_string(
            'new_post.html',
            {
                'name': post.name,
                'text': post.text,
                'id': post_id,
                'username': user.username
            }
        )
        msg = EmailMultiAlternatives(
            subject=post.name,
            body=f'Hello, {user.username}. New post in your favorite category!',
            to=[user.email]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task
def newsletter():
    tomorrow = datetime.date.today() + datetime.timedelta(1)
    week_ago = tomorrow - datetime.timedelta(7)
    for cat in Category.objects.all():
        post_list = list(cat.post_set.filter(date__range=(week_ago, tomorrow)))
        recepients = list(cat.subscribers.all().values('email'))
        if recepients:
            html_content = render_to_string(
                'weekly_posts.html',
                {
                    'category': cat.name,
                    'post_list': post_list
                }
            )
            msg = EmailMultiAlternatives(
                subject='Weekly Newsletter',
                body=f'Hello! Here are posts published during the week in {cat.name}:',
                to=[address['email'] for address in recepients]
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
