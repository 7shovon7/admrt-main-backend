# Generated by Django 4.2.13 on 2024-06-19 14:26

import core.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_user_options_user_user_email_ci_uniqueness'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=core.models.LowercaseEmailField(max_length=254, unique=True),
        ),
    ]
