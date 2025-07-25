from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class TestRoutes(TestCase):
    def test_pages_availability(self):
        urls = (
            'pages:about',
            'pages:rules'
        )
        for address in urls:
            with self.subTest(address=address):
                url = reverse(address)
                response = self.client.get(url)
                self.assertEqual(response.status_code,
                                 HTTPStatus.OK)
