# Generated by Django 3.1.7 on 2021-03-14 12:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210314_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockitem',
            name='add_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
