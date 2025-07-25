from datetime import datetime, timedelta

from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone


from posts.models import Advice, Category, Comment, Country, Favorite, Town, Post

User = get_user_model()


class TestHomePage(TestCase):

    HOME_URL = reverse('posts:index')

    @classmethod
    def setUpTestData(cls) -> None:
        today =datetime.today()
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
            country=cls.country,
            
        )
        Post.objects.bulk_create(
            Post(title=f'Post title {index}',
            text='Post text',
            author=cls.author,
            category=cls.category,
            town=cls.town,
            pub_date=today - timedelta(days=index)
            )
            for index in range(settings.OBJECTS_COUNT_ON_PAGES + 1))
    
    def test_posts_count(self):
        response = self.client.get(self.HOME_URL)
        object_list = response.context['object_list']
        posts_count = len(object_list)
        self.assertEqual(posts_count, settings.OBJECTS_COUNT_ON_PAGES)

    def test_posts_order(self):
        response = self.client.get(self.HOME_URL)
        object_list = response.context['object_list']
        all_dates = [post.pub_date for post in object_list]
        sorted_dates = sorted(all_dates, reverse=True)
        self.assertEqual(all_dates, sorted_dates)
        
        
class Test_Post_Detail_Page(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.author = User.objects.create(username='Vasya')
        cls.reader=User.objects.create(username='Simple_reader')        
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
            country=cls.country,
            
        )
        cls.post = Post.objects.create(
            title='Post title {index}',
            text='Post text',
            author=cls.author,
            category=cls.category,
            town=cls.town,
            )
        cls.detail_url = reverse('posts:post_detail', args=(cls.post.id,))
        now = timezone.now()
        for index in range(settings.OBJECTS_COUNT_ON_PAGES+1):
            comment = Comment.objects.create(
            text=f'Comment text {index}',
            post=cls.post,
            author=cls.reader)
            comment.created_at = now + timedelta(days=index)
            comment.save()
 
    def test_comments_count(self):
        response = self.client.get(self.detail_url)
        self.assertIn('comments', response.context)
        all_comments = response.context['comments']
        posts_count = len(all_comments)
        self.assertEqual(posts_count, settings.OBJECTS_COUNT_ON_PAGES)

    def test_comments_order(self):
        response = self.client.get(self.detail_url)
        all_comments = response.context['comments']
        all_dates = [comment.created_at for comment in all_comments]
        sorted_dates = sorted(all_dates, reverse=True)
        self.assertEqual(all_dates, sorted_dates)

    def test_anonymous_client_has_no_form(self):
        response = self.client.get(self.detail_url)
        self.assertNotIn('form', response.context)

    def test_authorized_client_has_form(self):
        self.client.force_login(self.author)
        response = self.client.get(self.detail_url)
        self.assertIn('form', response.context)



class Test_Category_Detail_Page(TestCase):

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
            country=cls.country,
            
        )
        cls.detail_url = reverse('posts:category_posts', args=(cls.category.slug,))
        now = timezone.now()
        Post.objects.bulk_create(
            Post(title=f'Post title {index}',
            text='Post text',
            author=cls.author,
            category=cls.category,
            town=cls.town,
            pub_date=now - timedelta(days=index)
            )
            for index in range(settings.OBJECTS_COUNT_ON_PAGES + 1))

    def test_posts_count(self):
        response = self.client.get(self.detail_url)
        self.assertIn('page_obj', response.context)
        object_list = response.context['page_obj']
        posts_count = len(object_list)
        self.assertEqual(posts_count, settings.OBJECTS_COUNT_ON_PAGES)

    def test_posts_order(self):
        response = self.client.get(self.detail_url)
        object_list = response.context['page_obj']
        all_dates = [post.pub_date for post in object_list]
        sorted_dates = sorted(all_dates, reverse=True)
        self.assertEqual(all_dates, sorted_dates)


class Test_Town_Detail_Page(TestCase):

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
            country=cls.country,
            
        )
        cls.detail_url = reverse('posts:town_posts', args=(cls.town.slug,))
        now = timezone.now()
        Post.objects.bulk_create(
            Post(title=f'Post title {index}',
            text='Post text',
            author=cls.author,
            category=cls.category,
            town=cls.town,
            pub_date=now - timedelta(days=index)
            )
            for index in range(settings.OBJECTS_COUNT_ON_PAGES + 1))

    def test_posts_count(self):
        response = self.client.get(self.detail_url)
        self.assertIn('page_obj', response.context)
        object_list = response.context['page_obj']
        posts_count = len(object_list)
        self.assertEqual(posts_count, settings.OBJECTS_COUNT_ON_PAGES)

    def test_posts_order(self):
        response = self.client.get(self.detail_url)
        object_list = response.context['page_obj']
        all_dates = [post.pub_date for post in object_list]
        sorted_dates = sorted(all_dates, reverse=True)
        self.assertEqual(all_dates, sorted_dates)


class Test_Favorite_Detail_Page(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.author = User.objects.create(username='Vasya')
        cls.reader=User.objects.create(username='Simple_reader')
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
            country=cls.country,
            
        )
        cls.detail_url = reverse('posts:get_favorite')
        now = timezone.now()
        posts = Post.objects.bulk_create(
            Post(title=f'Post title {index}',
            text='Post text',
            author=cls.author,
            category=cls.category,
            town=cls.town,
            pub_date=now - timedelta(days=index)
            )
            for index in range(settings.OBJECTS_COUNT_ON_PAGES + 1))

        for post in posts:
            Favorite.objects.create(
                user=cls.reader,
                post=post 
            )
                    

    def test_posts_count(self):
        self.client.force_login(self.reader)
        response = self.client.get(self.detail_url)
        self.assertIn('page_obj', response.context)
        object_list = response.context['page_obj']
        posts_count = len(object_list)
        self.assertEqual(posts_count, settings.OBJECTS_COUNT_ON_PAGES)

    def test_posts_order(self):
        self.client.force_login(self.reader)
        response = self.client.get(self.detail_url)
        object_list = response.context['page_obj']
        all_dates = [post.pub_date for post in object_list]
        sorted_dates = sorted(all_dates, reverse=True)
        self.assertEqual(all_dates, sorted_dates)


class Test_User_Profile_Page(TestCase):

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
            country=cls.country,
            
        )
        cls.detail_url = reverse('users:profile', args=(cls.author.username,))
        print(cls.detail_url)
        now = timezone.now()
        Post.objects.bulk_create(
            Post(title=f'Post title {index}',
            text='Post text',
            author=cls.author,
            category=cls.category,
            town=cls.town,
            pub_date=now - timedelta(days=index)
            )
            for index in range(settings.OBJECTS_COUNT_ON_PAGES + 1))

    def test_posts_count(self):
        self.client.force_login(self.author)
        response = self.client.get(self.detail_url)
        self.assertIn('page_obj', response.context)
        object_list = response.context['page_obj']
        posts_count = len(object_list)
        self.assertEqual(posts_count, settings.OBJECTS_COUNT_ON_PAGES)

    def test_posts_order(self):
        self.client.force_login(self.author)
        response = self.client.get(self.detail_url)
        object_list = response.context['page_obj']
        all_dates = [post.pub_date for post in object_list]
        sorted_dates = sorted(all_dates, reverse=True)
        self.assertEqual(all_dates, sorted_dates)


class Test_Country_Detail_Page(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.author = User.objects.create(username='Vasya')
        cls.reader=User.objects.create(username='Simple_reader')        
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
            country=cls.country,
            
        )
        cls.post = Post.objects.create(
            title='Post title {index}',
            text='Post text',
            author=cls.author,
            category=cls.category,
            town=cls.town,
            )
        cls.detail_url = reverse('posts:country_town', args=(cls.country.slug,))
        now = timezone.now()
        for index in range(settings.OBJECTS_COUNT_ON_PAGES+1):
            advice = Advice.objects.create(
            text=f'Advice text {index}',
            country=cls.country,
            author=cls.author)
            advice.created_at = now + timedelta(days=index)
            advice.save()
 
    def test_advices_count(self):
        response = self.client.get(self.detail_url)
        self.assertIn('page_obj', response.context)
        all_advices = response.context['page_obj']
        advices_count = len(all_advices)
        self.assertEqual(advices_count, settings.OBJECTS_COUNT_ON_PAGES)

    def test_advices_order(self):
        response = self.client.get(self.detail_url)
        all_advices = response.context['page_obj']
        all_dates = [advice.created_at for advice in all_advices]
        sorted_dates = sorted(all_dates, reverse=True)
        self.assertEqual(all_dates, sorted_dates)

    def test_anonymous_client_has_no_form(self):
        response = self.client.get(self.detail_url)
        self.assertNotIn('form', response.context)

    def test_authorized_client_has_form(self):
        self.client.force_login(self.author)
        response = self.client.get(self.detail_url)
        self.assertIn('form', response.context)

