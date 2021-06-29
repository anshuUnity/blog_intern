from django.core.mail import EmailMessage


def send_mail_task(subject, message, email_from, recepient_list):
    msg = EmailMessage(subject, message, email_from, recepient_list)
    msg.content_subtype = 'html'
    msg.send()
