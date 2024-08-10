from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Category(models.Model):
    title = models.CharField(
        max_length=256, verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        max_length=64, unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы,'
            + ' цифры, дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(models.Model):
    town = models.CharField(
        max_length=256,
        verbose_name='Название города'
    )
    country = models.CharField(
        max_length=256,
        verbose_name='Название страны'
    )
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.town


class Post(models.Model):
    title = models.CharField(
        max_length=256, verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата и время публикации',
        # help_text=('Если установить дату и время в будущем'
        #            + ' — можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='post',
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name='post',
        null=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='post',
        verbose_name='Категория'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.')
    image = models.CharField(
        max_length=256,
        null=True,
        default=None,
        verbose_name='Фотография'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title
