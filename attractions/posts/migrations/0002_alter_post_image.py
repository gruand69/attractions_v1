# Generated by Django 5.0.6 on 2024-08-08 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.CharField(default=None, max_length=256, null=True, verbose_name='Фотография'),
        ),
    ]
