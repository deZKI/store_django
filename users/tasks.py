import uuid
from datetime import timedelta

from celery import shared_task

from django.contrib.auth.forms import PasswordResetForm
from django.utils.timezone import now

from users.models import User, EmailVerification


# не передаем обьекты

@shared_task(name='sendEmailVerification')
def send_email_verification(user_id):
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(hours=48)
    code = uuid.uuid4()
    email = EmailVerification.objects.create(code=code, user=user, expiration=expiration)
    email.send_verification_email()


@shared_task(name='changePasswordEmail')
def send_password_reset(subject_template_name, email_template_name, context,
                        from_email, to_email, html_email_template_name):
    context['user'] = User.objects.get(pk=context['user'])

    PasswordResetForm.send_mail(
        None,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name
    )
