# Generated by Django 3.1.2 on 2020-11-01 13:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('poem', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poem',
            name='writer',
        ),
        migrations.AddField(
            model_name='poem',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
