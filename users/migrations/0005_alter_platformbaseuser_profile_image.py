# Generated by Django 5.0.4 on 2024-05-09 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_socialmedia_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platformbaseuser',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
