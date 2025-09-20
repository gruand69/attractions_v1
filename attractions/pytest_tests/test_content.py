import pytest
from django.conf import settings
from django.urls import reverse


@pytest.mark.parametrize(
    'name, args, bulk, list, client_type',
    (
        ('posts:index', None, pytest.lazy_fixture('posts_bulk'),
         'object_list', pytest.lazy_fixture('client')),
        ('posts:post_detail', pytest.lazy_fixture('id_for_post'),
         pytest.lazy_fixture('comments_bulk'), 'comments',
         pytest.lazy_fixture('client')),
        ('posts:category_posts', pytest.lazy_fixture('slug_for_category'),
         pytest.lazy_fixture('posts_bulk'), 'page_obj',
         pytest.lazy_fixture('client')),
        ('posts:town_posts', pytest.lazy_fixture('slug_for_town'),
         pytest.lazy_fixture('posts_bulk'), 'page_obj',
         pytest.lazy_fixture('client')),
        ('posts:country_town', pytest.lazy_fixture('slug_for_country'),
         pytest.lazy_fixture('advices_bulk'), 'page_obj',
         pytest.lazy_fixture('client')),
        ('users:profile', pytest.lazy_fixture('username_for_author'),
         pytest.lazy_fixture('posts_bulk'), 'page_obj',
         pytest.lazy_fixture('author_client')),
    )
)
def test_objects_count(bulk, name, args, client_type, list):
    bulk
    url = reverse(name, args=args)
    response = client_type.get(url)
    object_list = response.context[list]
    objects_count = len(object_list)
    assert objects_count == settings.OBJECTS_COUNT_ON_PAGES


@pytest.mark.parametrize(
    'name, args, list, client_type',
    (
        ('posts:index', None, 'object_list', pytest.lazy_fixture('client')),
        ('posts:category_posts', pytest.lazy_fixture('slug_for_category'),
         'page_obj', pytest.lazy_fixture('client')),
        ('posts:town_posts', pytest.lazy_fixture('slug_for_town'), 'page_obj',
         pytest.lazy_fixture('client')),
        ('users:profile', pytest.lazy_fixture('username_for_author'),
         'page_obj', pytest.lazy_fixture('author_client')),
    )
)
def test_posts_order(posts_bulk, name, args, client_type, list):
    posts_bulk
    url = reverse(name, args=args)
    response = client_type.get(url)
    object_list = response.context[list]
    all_dates = [post.pub_date for post in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.parametrize(
    'name, args, bulk, list',
    (
        ('posts:post_detail', pytest.lazy_fixture('id_for_post'),
         pytest.lazy_fixture('comments_bulk'), 'comments'),
        ('posts:country_town', pytest.lazy_fixture('slug_for_country'),
         pytest.lazy_fixture('advices_bulk'), 'page_obj'),)
)
def test_comments_advuce_order(client, bulk, name, args, list):
    bulk
    url = reverse(name, args=args)
    response = client.get(url)
    object_list = response.context[list]
    all_dates = [object.created_at for object in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.parametrize(
    'name, args',
    (
        ('posts:create_post', None),
        ('posts:edit_post', pytest.lazy_fixture('id_for_post')),
        ('posts:post_detail', pytest.lazy_fixture('id_for_post')),
        ('posts:edit_comment', pytest.lazy_fixture('id_for_post_comment')),
        ('posts:country_town', pytest.lazy_fixture('slug_for_country')),
        ('posts:edit_advice', pytest.lazy_fixture('args_for_advice')),
    )
)
def test_pages_contains_form(author_client, name, args):
    url = reverse(name, args=args)
    response = author_client.get(url)
    assert 'form' in response.context
