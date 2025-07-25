from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """Класс тегов достопримечательностей"""
    tag = models.CharField('Тег',
                           max_length=20
                           )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('tag',)

    def __str__(self):
        return self.tag


class Category(models.Model):
    title = models.CharField(
        max_length=256, verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        max_length=40,
        verbose_name='Идентификатор',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Недопустимый символ!'
        )
        ],
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы,'
            + ' цифры, дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Country(models.Model):
    title = models.CharField(
        max_length=256, verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        max_length=40,
        verbose_name='Идентификатор',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Недопустимый символ!'
        )
        ],
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы,'
            + ' цифры, дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Town(models.Model):
    title = models.CharField(
        max_length=256, verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        max_length=40,
        verbose_name='Идентификатор',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Недопустимый символ!'
        )
        ],
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы,'
            + ' цифры, дефис и подчёркивание.')
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        related_name='towns',
        verbose_name='Страна'
    )

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ('title',)

    def __str__(self):
        return self.title


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
        related_name='posts',
        verbose_name='Автор публикации'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='Категория'
    )
    image = models.ImageField(
        'Фотография', upload_to='posts_images', blank=True)

    town = models.ForeignKey(
        Town,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='Город'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        blank=True,
        help_text='Удерживайте Ctrl для выбора нескольких вариантов'
    )

    def comment_count(self):
        return self.comments.count()

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created_at',)


class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favoriting',
        verbose_name='Пользователь'
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='favoriting',
        verbose_name='Достопримечательность'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ('id',)
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'post'),
                name='unique_favorite_post'
            ),
        )

    def __str__(self):
        return f'У {self.user} {self.post} входит в избранное'


class Advice(models.Model):
    text = models.TextField('Текст комментария')
    image = models.ImageField(
        'Фото совета', upload_to='advices_images', blank=True)

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='advices'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='advices')

    class Meta:
        verbose_name = 'Совет'
        verbose_name_plural = 'Советы'
        ordering = ('-created_at',)
