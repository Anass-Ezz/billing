# Generated by Django 3.1.7 on 2021-03-26 23:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20210318_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='billitem',
            name='add_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]