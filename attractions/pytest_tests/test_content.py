from django.urls import reverse
import pytest

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

