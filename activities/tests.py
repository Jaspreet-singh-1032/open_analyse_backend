from django.test import TestCase


class ActivityTypesApiTestCase(TestCase):
    def setUp(self):
        user = self.client.post()
