# Generated by Django 3.1.2 on 2020-11-02 20:19

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('poem', '0008_like'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('owner', 'poem_n')},
        ),
    ]