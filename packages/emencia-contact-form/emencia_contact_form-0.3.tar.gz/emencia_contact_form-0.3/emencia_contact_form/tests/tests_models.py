# -*- coding: utf-8 -*-

from django.contrib.sites.models import Site
from django.test import SimpleTestCase, TestCase

from ..choices import MR
from ..models import Contact, ContactFormSettings


class TestContact(SimpleTestCase):
    def test_full_empty(self):
        contact = Contact()
        assert contact.contact_name == ""
        assert contact.full_name == ""

    def test_full_name_first_name_only(self):
        contact = Contact(first_name="  foo ")
        assert contact.full_name == "foo"

    def test_full_name_last_name_only(self):
        contact = Contact(last_name="  bar ")
        assert contact.full_name == "bar"

    def test_full_name_both_field(self):
        contact = Contact(first_name="  foo ", last_name="  bar ")
        assert contact.full_name == "foo bar"

    def test_contact_name_civility_only(self):
        contact = Contact(civility=MR)
        assert contact.contact_name == "Mr"

    def test_contact_name_full_name_only(self):
        contact = Contact(first_name="  foo ", last_name="  bar ")
        assert contact.contact_name == contact.full_name

    def test_contact_name_all_fields(self):
        contact = Contact(first_name="foo", last_name="bar", civility=MR)
        assert contact.contact_name == "Mr foo bar"

    def test_str_method(self):
        contact = Contact(email="a@a.com")
        assert contact.__str__() == "Contact from a@a.com"

        contact = Contact(first_name="foo", last_name="bar", civility=MR)
        assert contact.__str__() == "Contact from Mr foo bar"


class TestContactFormSettings(TestCase):
    def test__str(self):
        settings = ContactFormSettings()
        assert settings.__str__() == "Contact Form Settings"

    def test_email_to(self):
        from django.conf import settings

        # this solely ensures arrayField behave as expected
        site = Site.objects.get(pk=settings.SITE_ID)
        # with our migration, we do already have a related settings
        csettings, createde = \
            ContactFormSettings.objects.get_or_create(site__pk=site.pk)
        assert csettings.email_to == "example@example.com"

        two_mails = ["a@a.fr", "b@b.fr"]
        csettings.email_to = two_mails
        csettings.save()
        assert csettings.email_to == two_mails
