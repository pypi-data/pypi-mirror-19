# -*- coding: utf-8 -*-
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_mail(subject, to_emails, from_email, html_template,
              text_template=None, data={}, headers={}, **kwargs):
    """Sends an email.

    subject       -- subject of the email
    to_emails     -- list of recipients
    from_email    -- from address
    html_template -- html template location
    text_template -- plain text template location
    data          -- data needed in the templates
    headers       -- any extra headers
    kwargs        -- extra arguments passed on to Django's `EmailMessage`
    """
    msg = create_mail(subject, to_emails, from_email, html_template,
                      text_template, data=data, headers=headers, **kwargs)
    msg.send()


def create_mail(subject, to_emails, from_email, html_template,
                text_template=None, data={}, headers={}, **kwargs):
    """Returns an EmailMultiAlternatives object.

    subject       -- subject of the email
    to_emails     -- list of recipients
    from_email    -- from address
    html_template -- html template location
    text_template -- plain text template location
    data          -- data needed in the templates
    headers       -- any extra headers

    TODO: It might not be the best thing to use EmailMultiAlternatives when
          we only want HTML or text.
    """
    html_content = render_to_string(html_template, data)
    text_content = ''
    if text_template:
        text_content = render_to_string(text_template, data)

    msg = EmailMultiAlternatives(subject, text_content, from_email,
                                 to_emails, headers=headers, **kwargs)
    msg.attach_alternative(html_content, "text/html")
    msg.return_path = settings.DEFAULT_FROM_EMAIL
    return msg
