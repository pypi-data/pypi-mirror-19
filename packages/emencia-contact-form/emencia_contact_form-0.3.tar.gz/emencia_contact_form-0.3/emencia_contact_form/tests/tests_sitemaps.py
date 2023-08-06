from datetime import datetime

from django.test import SimpleTestCase

from ..sitemaps import ContactFormEntryBase, ContactFormSitemap


class TestContactFormSitemap(SimpleTestCase):
    def test_sitemap(self):
        sitemap = ContactFormSitemap()
        entry = ContactFormEntryBase()
        entry.url_name = "contact_form"

        assert sitemap.items() == []
        assert sitemap.location(entry) == "/"
        assert sitemap.priority(entry) == 1.0
        assert type(sitemap.lastmod(entry)) == datetime
