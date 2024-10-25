from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_mail(email, data):
    """
    This function sends an email to the recipient.
    Args: email (str): Email address of the recipient.
          data (list): List of dictionaries containing the processed data.
    Return: None
    """

    html_content = render_to_string(
        "home/mail.html", {"data": data}
    )
    subject = "Python Assigment - Vineet Kumar"
    text_content = strip_tags(html_content)
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    email.attach_alternative(html_content, "text/html")
    email.send()