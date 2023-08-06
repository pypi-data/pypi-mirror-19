# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string


def remove_all_newlines(string):
    # See https://docs.djangoproject.com/en/1.10/topics/email/
    return ' '.join(string.splitlines())


def send_mail_to_contact(contact):
    # We need to ensure headers does *not* contain any newline
    mail_settings = Site.objects.get(pk=settings.SITE_ID).contactformsettings
    subject = remove_all_newlines(mail_settings.subject)
    content = render_to_string('contact_form/contact_form_message.txt',
                               {'contact': contact})
    mail_from = mail_settings.email_from or contact.email
    mail_from = remove_all_newlines(mail_from)
    mail_to = [remove_all_newlines(elt.strip())
               for elt in mail_settings.email_to.split(",")]
    send_mail(subject, content, mail_from, mail_to,
              fail_silently=not settings.DEBUG)
