# Generated by Django 3.1.7 on 2021-04-05 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_auto_20210329_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='bill_total',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='bill',
            name='items',
            field=models.ManyToManyField(blank=True, null=True, to='main.BillItem'),
        ),
        migrations.AlterField(
            model_name='varient',
            name='quantity',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]