# Generated by Django 3.1.2 on 2020-11-15 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poem', '0016_auto_20201114_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tagscore',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]