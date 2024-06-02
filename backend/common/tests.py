# import os

# from django.conf import settings
# from django.test import TestCase

# from decouple import config

from common.utils.tests import TestCaseUtils


class TestIndexView(TestCaseUtils):
    view_name = "common:index"

    def test_returns_status_200(self):
        response = self.auth_client.get(self.reverse(self.view_name))
        self.assertResponse200(response)

# class SettingsTest(TestCase):
#     def test_django_settings_module(self):
#         if os.getenv('WEBSITE_HOSTNAME'):
#             self.assertEqual(settings.SETTINGS_MODULE, 'juvenotes.settings.production')
#         else:
#             self.assertEqual(settings.SETTINGS_MODULE, config("DJANGO_SETTINGS_MODULE"))