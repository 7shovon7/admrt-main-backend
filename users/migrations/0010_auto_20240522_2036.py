# Generated by Django 4.2.13 on 2024-05-22 20:36

from django.db import migrations, models
import uuid


def populate_uuid_field(apps, schema_editor):
    AdSpaceForSpaceHost = apps.get_model('users', 'AdSpaceForSpaceHost')
    for ad_space in AdSpaceForSpaceHost.objects.all():
        ad_space.temp_id = uuid.uuid4()
        ad_space.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_adspaceforspacehost_temp_id'),
    ]

    operations = [
        migrations.RunPython(populate_uuid_field)
    ]
