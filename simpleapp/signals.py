from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import NewAuthor


@receiver(m2m_changed, sender=NewAuthor)
def new_created(instance, sender, **kwargs):
    if not kwargs['action'] == 'post_add':
        return

    emails = User.objects.filter(
        subscriptions__author=instance.author
    ).values_list('email', flat=True)

    subject = f'Свежая новость у автора {instance.author}'

    text_content = (
        f'Новость: {instance.new}\n'
        f'Автор: {instance.author}\n\n'
        f'Ссылка на новость: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Новость: {instance.new}<br>'
        f'Автор: {instance.author}<br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на новость</a>'
    )

    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None,[email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()









