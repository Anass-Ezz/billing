# Generated by Django 3.1.7 on 2021-03-16 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20210316_1421'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BillItems',
            new_name='BillItem',
        ),
        migrations.RenameModel(
            old_name='customers',
            new_name='Customer',
        ),
        migrations.AddField(
            model_name='bill',
            name='charge_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
