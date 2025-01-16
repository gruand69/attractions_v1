from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import real_age


class MyUser(AbstractUser):
    date_of_birth = models.DateField(
        'Дата рождения', blank=True, null=True, validators=(real_age,))
    image = models.ImageField('Фото', upload_to='users_images', blank=True)
image = models.ImageField('Фото', upload_to='users_images', blank=True)