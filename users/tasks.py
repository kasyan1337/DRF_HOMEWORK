from datetime import timezone, timedelta

from celery import shared_task
from django.core.mail import send_mail
from materials.tests import User


@shared_task
def send_course_update_email(course_id, user_emails):
    subject = 'Course Update'
    message = f'The course with ID {course_id} has been updated.'
    from_email = 'no-reply@example.com'

    for email in user_emails:
        send_mail(subject, message, from_email, [email])

    return f"Sent update emails to {len(user_emails)} users."



@shared_task
def check_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    for user in inactive_users:
        print(f"Deactivating user: {user.email}")
    inactive_users.update(is_active=False)
