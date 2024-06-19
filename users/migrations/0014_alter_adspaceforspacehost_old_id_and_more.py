# Generated by Django 4.2.13 on 2024-05-22 22:22

from django.db import migrations, models
import users.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20240522_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adspaceforspacehost',
            name='old_id',
            field=models.CharField(default=users.models.generate_random_uuid, editable=False),
        ),
        migrations.AlterField(
            model_name='adspaceforspacehost',
            name='temp_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
