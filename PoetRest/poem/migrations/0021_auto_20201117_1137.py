# Generated by Django 3.1.2 on 2020-11-17 02:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('poem', '0020_auto_20201117_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterUniqueTogether(
            name='survey',
            unique_together={('owner', 'date')},
        ),
    ]