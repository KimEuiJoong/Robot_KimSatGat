# Generated by Django 3.1.2 on 2020-11-11 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poem', '0012_auto_20201111_0421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expoet',
            name='name',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
