# Generated by Django 5.0.4 on 2024-05-10 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_advertiserproduct_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertiserproduct',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
