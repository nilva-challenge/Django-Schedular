from django.core.mail import send_mail


def send_email_for_tasks(subject, message, recipient_list):
    return send_mail(subject, message, from_email=None, recipient_list=recipient_list)

