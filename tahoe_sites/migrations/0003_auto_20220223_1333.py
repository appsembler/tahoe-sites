# Generated by Django 2.2.12 on 2022-02-23 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tahoe_sites', '0002_auto_20220117_0354'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userorganizationmapping',
            unique_together=set(),
        ),
    ]
