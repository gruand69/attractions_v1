from http import HTTPStatus

import pytest
from django.conf import settings
from django.urls import reverse
from posts.models import Advice, Comment, Post
from pytest_django.asserts import assertRedirects


def test_user_can_create_post(author_client, post_form_data):
    url = reverse('posts:create_post')
    response = author_client.post(url, data=post_form_data)
    assertRedirects(response, reverse('posts:index'))
    assert Post.objects.count() == 1
    new_post = Post.objects.get()
    assert new_post.title == post_form_data['title']
    assert new_post.text == post_form_data['text']
    assert new_post.category.id == post_form_data['category']
    assert new_post.town.id == post_form_data['town']


@pytest.mark.django_db
def test_anomymous_user_cant_create_post(client, post_form_data):
    url = reverse('posts:index')
    response = client.post(url, data=post_form_data)
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    assert Post.objects.count() == 0


def test_user_can_create_comment(admin_client, comment_form_data, id_for_post):
    url = reverse('posts:add_comment', args=id_for_post)
    response = admin_client.post(url, data=comment_form_data)
    assertRedirects(response, reverse('posts:post_detail', args=id_for_post))
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == comment_form_data['text']
    assert new_comment.post.id == comment_form_data['post']


@pytest.mark.django_db
def test_anomymous_user_cant_create_comment(client, comment_form_data,
                                            id_for_post):
    url = reverse('posts:post_detail', args=id_for_post)
    response = client.post(url, data=comment_form_data)
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    assert Comment.objects.count() == 0


def test_user_can_create_advice(admin_client, advice_form_data,
                                slug_for_country):
    url = reverse('posts:add_advice', args=slug_for_country)
    response = admin_client.post(url, data=advice_form_data)
    assertRedirects(response, reverse('posts:country_town',
                                      args=slug_for_country))
    assert Advice.objects.count() == 1
    new_advice = Advice.objects.get()
    assert new_advice.text == advice_form_data['text']
    assert new_advice.country.slug == advice_form_data['country']


@pytest.mark.django_db
def test_anomymous_user_cant_create_advice(client, advice_form_data,
                                           slug_for_country):
    url = reverse('posts:add_advice', args=slug_for_country)
    response = client.post(url, data=advice_form_data)
    login_url = f'/auth/{settings.LOGIN_URL}/'
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Advice.objects.count() == 0


def test_author_can_edit_post(
        author_client, post_form_data, post, id_for_post):
    url = reverse('posts:edit_post', args=id_for_post)
    response = author_client.post(url, data=post_form_data)
    assertRedirects(response, reverse('posts:index'))
    post.refresh_from_db()
    assert post.title == post_form_data['title']
    assert post.text == post_form_data['text']
    assert post.category.id == post_form_data['category']
    assert post.town.id == post_form_data['town']


def test_other_user_cant_edit_post(
        admin_client, post_form_data, post, id_for_post):
    url = reverse('posts:edit_post', args=id_for_post)
    response = admin_client.post(url, data=post_form_data)
    assert response.status_code == HTTPStatus.FORBIDDEN
    post_from_db = Post.objects.get(id=post.id)
    assert post.title == post_from_db.title
    assert post.text == post_from_db.text
    assert post.category.id == post_from_db.category.id
    assert post.town.id == post_from_db.town.id

# def test_author_can_delete_post(author_client, id_for_post):
#     url = reverse('posts:delete_post', args=id_for_post)
#     response = author_client.post(url)
#     assertRedirects(response, reverse('posts:index'))
#     assert Post.objects.count() == 0

# def test_other_user_cant_delete_post(admin_client, id_for_post):
#     url = reverse('posts:delete_post', args=id_for_post)
#     response = admin_client.post(url)
#     assert response.status_code == HTTPStatus.FORBIDDEN
#     assert Post.objects.count() == 1


@pytest.mark.parametrize(
    'name, args, redirect_addresses, redirect_args, models',
    (
        ('posts:delete_comment',
         pytest.lazy_fixture('id_for_post_comment'), 'posts:post_detail',
         pytest.lazy_fixture('id_for_post'), Comment),
        ('posts:delete_advice',
         pytest.lazy_fixture('args_for_advice'), 'posts:country_town',
         pytest.lazy_fixture('slug_for_country'), Advice),
        ('posts:delete_post',
         pytest.lazy_fixture('id_for_post'), 'posts:index', None, Post)
    ),)
def test_author_can_delete_his_objects(author_client,
                                       name, args, redirect_addresses,
                                       redirect_args, models):
    url = reverse(name, args=args)
    response = author_client.post(url)
    assertRedirects(response, reverse(redirect_addresses, args=redirect_args))
    assert models.objects.count() == 0


@pytest.mark.parametrize(
    'name, args, models',
    (
        ('posts:delete_comment',
         pytest.lazy_fixture('id_for_post_comment'),
         Comment),
        ('posts:delete_advice', pytest.lazy_fixture(
            'args_for_advice'), Advice),
        ('posts:delete_post',
         pytest.lazy_fixture('id_for_post'), Post)
    ),)
def test_other_user_cant_delete_object(admin_client, name, args, models):
    url = reverse(name, args=args)
    response = admin_client.post(url)
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert models.objects.count() == 1


@pytest.mark.parametrize(
    'name, args, model, form_data, redirect_url, redirect_args',
    (
        ('posts:edit_comment',
         pytest.lazy_fixture('id_for_post_comment'),
         pytest.lazy_fixture('comment'),
         pytest.lazy_fixture('comment_form_data'),
         'posts:post_detail',
         pytest.lazy_fixture('id_for_post'),
         ),
        ('posts:edit_advice',
         pytest.lazy_fixture('args_for_advice'),
         pytest.lazy_fixture('advice'),
         pytest.lazy_fixture('advice_form_data'),
         'posts:country_town',
         pytest.lazy_fixture('slug_for_country'),
         ),
    ))
def test_author_can_edit_object(author_client,
                                name, args, form_data, model, redirect_url,
                                redirect_args):
    url = reverse(name, args=args)
    response = author_client.post(url, data=form_data)
    assertRedirects(response, reverse(redirect_url, args=redirect_args))
    model.refresh_from_db()
    assert model.text == form_data['text']


@pytest.mark.parametrize(
    'name, args, model, form_data, clas',
    (
        ('posts:edit_comment',
         pytest.lazy_fixture('id_for_post_comment'),
         pytest.lazy_fixture('comment'),
         pytest.lazy_fixture('comment_form_data'),
         Comment
         ),
        ('posts:edit_advice',
         pytest.lazy_fixture('args_for_advice'),
         pytest.lazy_fixture('advice'),
         pytest.lazy_fixture('advice_form_data'),
         Advice
         ),
    ))
def test_other_user_cant_edit_object(admin_client, name, args, form_data,
                                     model, clas):
    url = reverse(name, args=args)
    response = admin_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.FORBIDDEN
    clas_from_db = clas.objects.get(id=model.id)
    assert model.text == clas_from_db.text
