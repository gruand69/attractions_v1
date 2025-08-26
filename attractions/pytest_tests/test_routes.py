import pytest
from http import HTTPStatus

from django.conf import settings
from django.urls import reverse
from posts.models import Post

from pytest_django.asserts import assertRedirects

@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (('posts:index', None),
     ('posts:post_detail', pytest.lazy_fixture('id_for_post')),
     ('posts:category_posts', pytest.lazy_fixture('slug_for_category')),
     ('posts:town_posts', pytest.lazy_fixture('slug_for_town')),
     ('posts:country_town', pytest.lazy_fixture('slug_for_country')),     
     )
)
def test_home_availability_for_anonymous_user(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK

@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    (
        'posts:create_post',
        'posts:get_favorite',
        'logout'
    )
)
def test_home_availability_for_auth_user(admin_client, name):
    url = reverse(name)
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.OK

@pytest.mark.parametrize(
        'parametrized_client, expected_status',
        (
            (pytest.lazy_fixture('admin_client'), HTTPStatus.FORBIDDEN),
            (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
        )
)
@pytest.mark.parametrize(
    'name, args',
    (
    ('posts:edit_post', pytest.lazy_fixture('id_for_post')),
    ('posts:delete_post', pytest.lazy_fixture('id_for_post')),
    ('posts:edit_comment', pytest.lazy_fixture('id_for_post_comment')),
    ('posts:delete_comment', pytest.lazy_fixture('id_for_post_comment')),
    ('posts:edit_advice', pytest.lazy_fixture('args_for_advice')),
    ('posts:delete_advice', pytest.lazy_fixture('args_for_advice')),
    ))
def test_page_availability_for_different_users(
    parametrized_client, name, args, expected_status):
    url = reverse(name, args=args)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status

@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
    ('posts:create_post', None),
    ('posts:get_favorite', None),
    ('posts:add_comment', pytest.lazy_fixture('id_for_post')),
    ('posts:add_advice', pytest.lazy_fixture('slug_for_country')),
    ('posts:add_favorite', pytest.lazy_fixture('id_for_post')),
    ),
)
def test_redirects(client, name, args):
    login_url = f'/auth/{settings.LOGIN_URL}/'
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)

@pytest.mark.parametrize(
        'parametrized_client, expected_status',
        (
            (pytest.lazy_fixture('admin_client'), HTTPStatus.FORBIDDEN),
            (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
        ))
def test_page_change_profile_avalability_for_authorized_user(
    parametrized_client, expected_status, username_for_author):
    url = reverse('users:edit_profile',args=username_for_author)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status

def test_page_profile_avalability_for_authorized_user(admin_client, username_for_author):
        url = reverse('users:profile',args=username_for_author)
        response = admin_client.get(url)
        assert response.status_code == HTTPStatus.OK

@pytest.mark.parametrize(
    'name, args',
    (
    ('users:profile', pytest.lazy_fixture('username_for_author')),
    ('users:edit_profile', pytest.lazy_fixture('username_for_author')),
    ),
)
def test_redirect_for_anonymous_client(name, args, client):
        login_url = f'/auth/{settings.LOGIN_URL}/'
        url = reverse(name, args=args)
        redirect_url = f'{login_url}?next={url}'
        response = client.get(url)
        assertRedirects(response, redirect_url)
        