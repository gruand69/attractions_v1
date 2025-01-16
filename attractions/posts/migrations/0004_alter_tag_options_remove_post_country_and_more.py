# Generated by Django 5.0.6 on 2025-01-07 18:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_country_tag_town_remove_post_location_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ('tag',), 'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
        migrations.RemoveField(
            model_name='post',
            name='country',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='name',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='slug',
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, help_text='Удерживайте Ctrl для выбора нескольких вариаетов', to='posts.tag', verbose_name='Теги'),
        ),
        migrations.AddField(
            model_name='tag',
            name='tag',
            field=models.CharField(default=None, max_length=20, verbose_name='Тег'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='town',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='towns', to='posts.country', verbose_name='Страна'),
        ),
    ]
