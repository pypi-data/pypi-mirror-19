# -*- coding: utf-8 -*-

import pytest

from django.contrib.sites.models import Site
from django.test import SimpleTestCase

from ..mails import remove_all_newlines, send_mail_to_contact
from ..models import Contact, ContactFormSettings


class TestMail(SimpleTestCase):
    def test_remove_all_newlines(self):
        string_test = '\r\n foo \n\t\r\n \n\n\r\n\r\rbar'
        expected = '  foo  \t       bar'
        assert expected == remove_all_newlines(string_test)


@pytest.mark.django_db
def test_send_mail_to_contact(mocker):
    site = Site.objects.get_current()
    ContactFormSettings.objects.get_or_create(site__pk=site.pk)
    contact = Contact(first_name="foo", last_name="bar")

    mock = mocker.patch('emencia_contact_form.mails.send_mail')
    assert not mock.called

    send_mail_to_contact(contact)
    assert mock.called
