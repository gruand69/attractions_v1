# Generated by Django 5.0.6 on 2024-12-07 12:25

import users.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_myuser_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, validators=[users.validators.real_age], verbose_name='Дата рождения'),
        ),
    ]
