from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.author = User.objects.create(username='Vasya')
        cls.reader = User.objects.create(username='Simple_reader')

    def test_page_change_profile_avalability_for_authorized_user(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.FORBIDDEN),)
        urls = (
            # ('users:profile', (self.author.username,)),
            ('users:edit_profile', (self.author.username,)),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name, arg in urls:
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=arg)
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_page_profile_avalability_for_authorized_user(self):
        urls = (
            ('users:profile', (self.author.username,)),
        )
        self.client.force_login(self.author)
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_for_anonymous_client(self):
        login_url = f'/auth/{settings.LOGIN_URL}/'
        urls = (
            ('users:profile', (self.author.username,)),
            ('users:edit_profile', (self.author.username,)),)
        for name, arg in urls:
            with self.subTest(name=name):
                url = reverse(name, args=arg)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
