# Generated by Django 4.2.13 on 2024-05-14 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_advertiserproduct_id_remove_portfolio_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertiserproduct',
            old_name='temp_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='portfolio',
            old_name='temp_id',
            new_name='id',
        ),
    ]
