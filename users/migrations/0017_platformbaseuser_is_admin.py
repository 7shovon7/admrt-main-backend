# Generated by Django 4.2.13 on 2024-05-26 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_adspaceforspacehost_space_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='platformbaseuser',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
