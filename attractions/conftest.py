import pytest

from posts.models import Advice, Post, Category, Town, Country, Comment

@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Author')

@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client

@pytest.fixture
def category():
    category = Category.objects.create(
        title='Category title',
        description='Category description',
        slug='category-slug',
    )
    return category

@pytest.fixture
def country():
    country = Country.objects.create(
        title='Country title',
        description='Country description',
        slug='country-slug',
    )
    return country


@pytest.fixture
def town(country):
    town = Town.objects.create(
        title='Town title',
        description='Town description',
        slug='town-slug',
        country=country
    )
    return town

@pytest.fixture
def post(author, category,town):
    post = Post.objects.create(
        title='Title',
        text='Post text',
        author=author,
        category=category,
        town=town
    )
    return post

@pytest.fixture
def comment(post, author):
    comment = Comment.objects.create(
        text='Comment text',
        post=post,
        author=author,
    )
    return comment

@pytest.fixture
def advice(country, author):
    advice = Advice.objects.create(
        text='Advice text',
        country=country,
        author=author,
    )
    return advice

@pytest.fixture
def id_for_post(post):
    return post.id,

@pytest.fixture
def id_for_comment(comment):
    return comment.id,

@pytest.fixture
def id_for_advice(advice):
    return advice.id,


@pytest.fixture
def slug_for_category(category):
    return category.slug,

@pytest.fixture
def slug_for_town(town):
    return town.slug,

@pytest.fixture
def slug_for_country(country):
    return country.slug,

# @pytest.fixture
# def id_for_post_comment(post, comment):
#     return (post.id, comment.id)

@pytest.fixture
def id_for_post_comment(id_for_post, id_for_comment):
    return (*id_for_post, *id_for_comment)

@pytest.fixture
def args_for_advice(slug_for_country, id_for_advice):
    return (*slug_for_country, *id_for_advice)

@pytest.fixture
def post_form_data(category, town):
    return {
        'title': 'New post title',
        'text': 'New post text',
        'category': category.id,
        'town': town.id
    }

@pytest.fixture
def comment_form_data(post):
    return {
        'text': 'New comment text',
        'post': post.id,
    }

@pytest.fixture
def advice_form_data(country):
    return {
        'text': 'New advice text',
        'country': country.slug,
    }
