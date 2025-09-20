from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from posts.models import Advice, Category, Comment, Country, Post, Town

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.author = User.objects.create(username='Vasya')
        cls.reader = User.objects.create(username='Simple_reader')
        cls.category = Category.objects.create(
            title='Category title',
            description='Category descriptions',
            slug='ctg',
        )
        cls.country = Country.objects.create(
            title='Country title',
            description='Country descriptions',
            slug='cnt'
        )
        cls.town = Town.objects.create(
            title='Town title',
            description='Town descriptions',
            slug='twn',
            country=cls.country
        )
        cls.post = Post.objects.create(
            title='Post title',
            text='Post text',
            author=cls.author,
            category=cls.category,
            town=cls.town
        )
        cls.comment = Comment.objects.create(
            text='Comment text',
            post=cls.post,
            author=cls.author,
        )
        cls.advice = Advice.objects.create(
            text='Advice text',
            country=cls.country,
            author=cls.author
        )

    def test_page_avalability_for_anonymous_user(self):
        urls = (
            ('posts:index', None),
            ('posts:post_detail', (self.post.id,)),
            ('posts:category_posts', (self.category.slug,)),
            ('posts:town_posts', (self.town.slug,)),
            ('posts:country_town', (self.country.slug,)),
            ('login', None),
            ('registration', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_page_avalability_for_editing_deleating(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.FORBIDDEN),)
        urls = (
            ('posts:edit_post', (self.post.id,)),
            ('posts:delete_post', (self.post.id,)),
            ('posts:edit_comment', (self.post.id, self.comment.id,)),
            ('posts:delete_comment', (self.post.id, self.comment.id,)),
            ('posts:edit_advice', (self.country.slug, self.advice.id,)),
            ('posts:delete_advice', (self.country.slug, self.advice.id,)))

        for user, status in users_statuses:
            self.client.force_login(user)
            for name, arg in urls:
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=arg)
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_page_avalability_for_authorized_user(self):
        urls = (
            ('posts:create_post', None),
            ('posts:get_favorite', None),
            ('logout', None),)
        self.client.force_login(self.author)
        for name, arg in urls:
            with self.subTest(name=name):
                url = reverse(name, args=arg)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_for_anonymous_client(self):
        login_url = f'/auth/{settings.LOGIN_URL}/'
        urls = (
            ('posts:create_post', None),
            ('posts:get_favorite', None),
            ('posts:add_comment', (self.post.id,)),
            ('posts:add_advice', (self.country.slug,)),
            ('posts:add_favorite', (self.post.id,)),)
        for name, arg in urls:
            with self.subTest(name=name):
                url = reverse(name, args=arg)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
