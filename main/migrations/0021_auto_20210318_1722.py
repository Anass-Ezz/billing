# Generated by Django 3.1.7 on 2021-03-18 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20210318_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='after_discount',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='bill',
            name='bill_total',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='bill',
            name='discount',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='billitem',
            name='item_price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='billitem',
            name='item_total',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stockitem',
            name='stock_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
