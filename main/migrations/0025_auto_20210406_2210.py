# Generated by Django 3.1.7 on 2021-04-06 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_auto_20210406_0039'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bill',
            old_name='charge_date',
            new_name='add_date',
        ),
    ]
