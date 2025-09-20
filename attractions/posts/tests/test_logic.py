from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse, reverse_lazy

from posts.models import Advice, Category, Comment, Country, Post, Town

User = get_user_model()


class TestCommentCreation(TestCase):
    COMMENT_TEXT = 'Comment text'

    @classmethod
    def setUpTestData(cls) -> None:
        cls.author = User.objects.create(username='Vasya')
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
        cls.url = reverse('posts:add_comment', args=(cls.post.id,))
        cls.redirect_url = reverse('posts:post_detail', args=(cls.post.id,))
        cls.user = User.objects.create(username='user')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.form_data = {'text': cls.COMMENT_TEXT}

    def test_anonimous_user_cant_create_comment(self):
        self.client.post(self.url, data=self.form_data)
        comments_count = Comment.objects.count()
        self.assertEqual(comments_count, 0)

    def test_reader_can_create_comment(self):
        response = self.auth_client.post(
            self.url, data=self.form_data)
        self.assertRedirects(response, self.redirect_url)
        comments_count = Comment.objects.count()
        self.assertEqual(comments_count, 1)
        comment = Comment.objects.get()
        self.assertEqual(comment.text, self.COMMENT_TEXT)
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.author, self.user)


class TestAdviceCreation(TestCase):
    ADVICE_TEXT = 'Advice text'

    @classmethod
    def setUpTestData(cls) -> None:
        cls.country = Country.objects.create(
            title='Country title',
            description='Country descriptions',
            slug='cnt'
        )
        cls.url = reverse('posts:add_advice', args=(cls.country.slug,))
        cls.redirect_url = reverse('posts:country_town', args=(
            cls.country.slug,))
        cls.user = User.objects.create(username='user')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.form_data = {'text': cls.ADVICE_TEXT}

    def test_anonimous_user_cant_create_advice(self):
        self.client.post(self.url, data=self.form_data)
        advices_count = Advice.objects.count()
        self.assertEqual(advices_count, 0)

    def test_reader_can_create_advice(self):
        response = self.auth_client.post(
            self.url, data=self.form_data)
        self.assertRedirects(response, self.redirect_url)
        advices_count = Advice.objects.count()
        self.assertEqual(advices_count, 1)
        advice = Advice.objects.get()
        self.assertEqual(advice.text, self.ADVICE_TEXT)
        self.assertEqual(advice.country, self.country)
        self.assertEqual(advice.author, self.user)


class TestPostCreation(TestCase):
    POST_TEXT = 'Post text'
    POST_TITLE = 'Post title'

    @classmethod
    def setUpTestData(cls) -> None:
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
        cls.url = reverse('posts:create_post')
        cls.redirect_url = reverse_lazy('posts:index')
        cls.user = User.objects.create(username='user')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.form_data = {'text': cls.POST_TEXT,
                         'title': cls.POST_TITLE,
                         'category': cls.category.id,
                         'town': cls.town.id
                         }

    def test_anonimous_user_cant_create_post(self):
        self.client.post(self.url, data=self.form_data)
        posts_count = Post.objects.count()
        self.assertEqual(posts_count, 0)

    def test_reader_can_create_post(self):
        response = self.auth_client.post(
            self.url, data=self.form_data)
        self.assertRedirects(response, self.redirect_url)
        posts_count = Post.objects.count()
        self.assertEqual(posts_count, 1)
        post = Post.objects.get()
        self.assertEqual(post.text, self.POST_TEXT)
        self.assertEqual(post.title, self.POST_TITLE)
        self.assertEqual(post.category.id, self.category.id)
        self.assertEqual(post.town.id, self.town.id)
        self.assertEqual(post.author, self.user)


class TestCommentEditDelete(TestCase):
    COMMENT_TEXT = 'Comment text'
    NEW_COMMENT_TEXT = 'New Comment text'

    @classmethod
    def setUpTestData(cls) -> None:
        cls.author = User.objects.create(username='Vasya')
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
        # cls.post_url = reverse('posts:post_detail', args=(cls.post.id,))
        cls.redirect_url = reverse('posts:post_detail', args=(cls.post.id,))
        cls.user = User.objects.create(username='user')
        cls.user_client = Client()
        cls.user_client.force_login(cls.user)
        cls.reader = User.objects.create(username='reader')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

        cls.comment = Comment.objects.create(
            text=cls.COMMENT_TEXT,
            post=cls.post,
            author=cls.user)

        cls.edit_url = reverse('posts:edit_comment', args=(
            cls.post.id, cls.comment.id))
        cls.delete_url = reverse('posts:delete_comment', args=(
            cls.post.id, cls.comment.id))
        cls.form_data = {'text': cls.  NEW_COMMENT_TEXT}

    def test_author_can_delete_comment(self):
        response = self.user_client.delete(self.delete_url)
        self.assertRedirects(response, self.redirect_url)
        comments_count = Comment.objects.count()
        self.assertEqual(comments_count, 0)

    def test_user_cant_delete_comment_of_another_user(self):
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        comments_count = Comment.objects.count()
        self.assertEqual(comments_count, 1)

    def test_author_can_edit_comment(self):
        response = self.user_client.post(self.edit_url, data=self.form_data)
        self.assertRedirects(response, self.redirect_url)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, self.NEW_COMMENT_TEXT)

    def test_user_cant_edit_comment_of_another_user(self):
        response = self.reader_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, self.COMMENT_TEXT)


class TestAdviceEditDelete(TestCase):
    ADVICE_TEXT = 'Comment text'
    NEW_ADVICE_TEXT = 'New Comment text'

    @classmethod
    def setUpTestData(cls) -> None:
        cls.country = Country.objects.create(
            title='Country title',
            description='Country descriptions',
            slug='cnt'
        )
        cls.redirect_url = reverse('posts:country_town', args=(
            cls.country.slug,))
        cls.user = User.objects.create(username='user')
        cls.user_client = Client()
        cls.user_client.force_login(cls.user)
        cls.reader = User.objects.create(username='reader')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.advice = Advice.objects.create(
            text=cls.ADVICE_TEXT,
            country=cls.country,
            author=cls.user)
        cls.edit_url = reverse('posts:edit_advice', args=(
            cls.country.slug, cls.advice.id))
        cls.delete_url = reverse('posts:delete_advice', args=(
            cls.country.slug, cls.advice.id))

        cls.form_data = {'text': cls.  NEW_ADVICE_TEXT}

    def test_author_can_delete_advice(self):
        response = self.user_client.delete(self.delete_url)
        self.assertRedirects(response, self.redirect_url)
        advices_count = Advice.objects.count()
        self.assertEqual(advices_count, 0)

    def test_user_cant_delete_advice_of_another_user(self):
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        advices_count = Advice.objects.count()
        self.assertEqual(advices_count, 1)

    def test_author_can_edit_advice(self):
        response = self.user_client.post(self.edit_url, data=self.form_data)
        self.assertRedirects(response, self.redirect_url)
        self.advice.refresh_from_db()
        self.assertEqual(self.advice.text, self.NEW_ADVICE_TEXT)

    def test_user_cant_edit_advice_of_another_user(self):
        response = self.reader_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.advice.refresh_from_db()
        self.assertEqual(self.advice.text, self.ADVICE_TEXT)


class TestPostEditDelete(TestCase):
    POST_TEXT = 'Post text'
    NEW_POST_TEXT = 'New Post text'
    POST_TITLE = 'Post title'
    NEW_POST_TITLE = 'New Post text'

    @classmethod
    def setUpTestData(cls) -> None:
        cls.author = User.objects.create(username='Vasya')
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
        cls.redirect_url = reverse('posts:index')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='reader')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.edit_url = reverse('posts:edit_post', args=(cls.post.id,))
        cls.delete_url = reverse('posts:delete_post', args=(cls.post.id,))
        cls.form_data = {'text': cls.NEW_POST_TEXT,
                         'title': cls.NEW_POST_TITLE,
                         'category': cls.category.id,
                         'town': cls.town.id,
                         }

    def test_author_can_delete_post(self):
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, self.redirect_url)
        posts_count = Post.objects.count()
        self.assertEqual(posts_count, 0)

    def test_user_cant_delete_post_of_another_user(self):
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        posts_count = Post.objects.count()
        self.assertEqual(posts_count, 1)

    def test_author_can_edit_post(self):
        response = self.author_client.post(
            self.edit_url, data=self.form_data)
        self.assertRedirects(response, self.redirect_url)
        self.post.refresh_from_db()
        self.assertEqual(self.post.text, self.NEW_POST_TEXT)
        self.assertEqual(self.post.title, self.NEW_POST_TITLE)

    def test_user_cant_edit_post_of_another_user(self):
        response = self.reader_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.post.refresh_from_db()
        self.assertEqual(self.post.text, self.POST_TEXT)
        self.assertEqual(self.post.title, self.POST_TITLE)
