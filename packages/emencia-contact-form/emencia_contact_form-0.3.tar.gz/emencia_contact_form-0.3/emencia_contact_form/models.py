# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext, ugettext_lazy as _

from django_countries.fields import CountryField

from .choices import CIVILITY_CHOICES, CIVILITY_DICT


@python_2_unicode_compatible
class Contact(models.Model):
    creation_date = models.DateTimeField(_('Creation Date'), auto_now_add=True)
    civility = models.CharField(
        _('Civility'),
        choices=CIVILITY_CHOICES,
        blank=True,
        max_length=10)
    first_name = models.CharField(_('First Name'), max_length=50, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=50, blank=True)
    phone = models.CharField(_('phone'), max_length=15, blank=True)
    company = models.CharField(_('company'), max_length=255, blank=True)
    city = models.CharField(_('city'), max_length=255, blank=True)
    state = models.CharField(_('state/province'), max_length=255, blank=True)
    country = CountryField(_('Country'), blank=True)
    email = models.EmailField(_('Email'))
    message = models.TextField(_('Message'), blank=True)
    optin_newsletter = models.BooleanField(
        _("Do you wish to receive the newsletter?"), default=False)

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')

    @property
    def full_name(self):
        return "{first_name} {last_name}".format(
            first_name=self.first_name.strip(),
            last_name=self.last_name.strip(),
        ).strip()

    @property
    def contact_name(self):
        return "{civility} {full_name}".format(
            civility=CIVILITY_DICT.get(self.civility, ""),
            full_name=self.full_name,
        ).strip()

    def __str__(self):
        contact = self.contact_name if self.full_name else self.email
        return 'Contact from {contact}'.format(contact=contact)


@python_2_unicode_compatible
class ContactFormSettings(models.Model):
    site = models.OneToOneField(Site, default=settings.SITE_ID)
    subject = models.CharField(
        _("Subject"),
        max_length=255,
        default="Contact Request",
        help_text=_("Email subject for the contact form."))
    email_to = models.TextField(
        _("Send mail to"),
        default="example@example.com",
        help_text=_("You can specify multiple mail address."))
    email_from = models.EmailField(
        _("Send contact email as"),
        default="do_not_answer@emencia.com")
    success_html = models.TextField(
        _("Success Message (in html)"),
        default="<h2>Success</h2>\n"
                "<p>Thank you for your message, "
                "we will get back to you quickly !</p>")

    class Meta:
        verbose_name = _("Contact Form Settings")
        verbose_name_plural = _("Contact Form Settings")

    def __str__(self):
        return ugettext("Contact Form Settings")
