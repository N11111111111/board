from .models import *
from django.core.mail import send_mail
from django.conf import settings
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import Post, Author, Comment
from django.db.models.signals import m2m_changed, post_save
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User





#отсылка если отклонили или одобрили отклик
@receiver(post_save, sender=Comment)
def accept_responses(instance, created, *args, **kwargs):
    if not created:

        if instance.active == 'True':

            email_s = User.objects.get(pk=instance.user_sender.id).email

            html_context = render_to_string(
                'email/accept_responses.html',
                {
                    'user_a': instance.user_sender,
                    'link': f'http://127.0.0.1:8000/news/news/{instance.post.id}',
                    'title': instance.post.title,

                }
            )

            msg = EmailMultiAlternatives(
                subject='Ответ по отклику',
                body='',
                from_email=None,
                to=[email_s]
            )

            msg.attach_alternative(html_context, 'text/html')
            msg.send()


        elif instance.active == 'False':

            email_s = User.objects.get(pk=instance.user_sender.id).email
            html_context = render_to_string(
                'email/denied_responses.html',
                {
                    'user_a': instance.user_sender,
                    'link': f'http://127.0.0.1:8000/news/news/{instance.post.id}',
                    'title': instance.post.title,
                }
            )

            msg = EmailMultiAlternatives(
                subject='Ответ по отклику',
                body='',
                from_email=None,
                to=[email_s]
            )

            msg.attach_alternative(html_context, 'text/html')
            msg.send()
        else:
            pass



# Отправка подписок категорий


dict_message = dict()


@receiver(post_save, sender=Post)
def notify_managers_post(sender, instance, created, **kwargs):
    for category in instance.category.all():
        recipients = [user.email for user in category.subscribed.all()]
        if created:
            start_word = 'Новое'
        else:
            start_word = 'Обновленщ'
        subject=f'На сайте NewsPaper {start_word.lower()} объявление: {instance.title}'
        message=f'NewsPaper.\n{instance.title}:\n{instance.text[:50]}...\nПодробнее: http://127.0.0.1:8000/news/news/{instance.id}'
        from_email=settings.SERVER_EMAIL

        send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipients,
                fail_silently=False
            )


@receiver(m2m_changed, sender=Post.category.through)
def notify_managers_posts(instance, action, pk_set, *args, **kwargs):
    if action == 'post_add':
        html_content = render_to_string(
            'post_create.html',
            {'post': instance, }
        )
        for pk in pk_set:
            category = Category.objects.get(pk=pk)
            recipients = [user.email for user in category.subscribed.all()]
            subject=f'На сайте NewsPaper новое объявление: {instance.title}'
            message=f'NewsPaper.\n{instance.title}:\n{instance.text[:30]}...\nПодробнее: http://127.0.0.1:8000/news/news/{instance.id}'
            from_email=settings.SERVER_EMAIL
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipients,
                fail_silently=False
            )



