# Generated by Django 3.1.7 on 2021-03-18 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20210318_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='after_discount',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='bill',
            name='discount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='bill',
            name='bill_total',
            field=models.IntegerField(null=True),
        ),
    ]