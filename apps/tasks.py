import os

from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from apps.models import Subscribe, New


# Send email
@shared_task
def send_email_customer(email, message, name, phone):
    print('Sending message')
    msg = f'''
    {email}, {message}, {name}, {phone}
    '''
    print(msg)
    send_mail(
        subject="Hello",
        message=msg,
        from_email=os.getenv("EMAIL_HOST_USER"),
        recipient_list=[email],
        fail_silently=False,
    )


# Send new user_email
@shared_task()
def send_email_customer1(pk):
    new = get_object_or_404(New, id=pk)
    for i in Subscribe.objects.all():
        print('sending message')
        send_mail(
            subject=i.pk,
            # message=new,
            from_email=os.getenv("EMAIL_HOST_USER"),
            recipient_list=[i.email],
            fail_silently=False,
        )
