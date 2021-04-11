# Generated by Django 3.1.7 on 2021-03-28 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_billitem_add_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='items',
            field=models.ManyToManyField(blank=True, to='main.BillItem'),
        ),
        migrations.AlterField(
            model_name='varient',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]