from django.test import TestCase
from django.test.client import Client
from django.contrib.admin.sites import AdminSite
from django.contrib.sites.models import Site
from django.conf import settings
from django.core.urlresolvers import reverse, resolve
from django.utils.timezone import datetime, timedelta
from django.utils.translation import ugettext_lazy as _
from bs4 import BeautifulSoup


class CampaignAdminTestCase(TestCase):
    client = Client()

    def setUp(self):
        super(CampaignAdminTestCase, self).setUp()
        #self.ca = CampaignAdmin(Campaign, AdminSite())
        #self.default_site = Site.objects.get(domain='netdoktor.dev')
        self.create_admin_user()

    def create_admin_user(self):
        logged_in = self.client.login(username=settings.SITE_SUPERUSER_USERNAME,
                                      password=settings.SITE_SUPERUSER_PASSWORD)
        self.assertTrue(logged_in, 'User is not logged in')
