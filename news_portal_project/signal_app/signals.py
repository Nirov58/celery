from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
# Obsolete imports
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
from news_portal_app.models import Post, Category, PostCategory
from news_portal_app.exceptions import LimitError
from news_portal_app.tasks import notify_subscribers
import datetime


@receiver(m2m_changed, sender=PostCategory)
def post_category_added(sender, instance, action, **kwargs):
    if action == 'post_add':
        notify_subscribers.apply_async(args=[instance.pk])


@receiver(pre_save, sender=Post)
def news_user_daily_limit(sender, instance, **kwargs):
    today = datetime.date.today()
    user = instance.author
    datetimes = user.post_set.all().order_by('-date').values('date')
    if len(datetimes) >= 3:
        last_dates = [d['date'].date() for d in datetimes[0:3]]
        if all([
            last_dates[0] == last_dates[1] == last_dates[2] == today,
            instance.author.user.is_superuser == 0
        ]):
            raise LimitError('Daily limit of posts created reached')


# Now-obsolete weekly newsletter function
"""def weekly_posts():
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
            msg.send()"""
