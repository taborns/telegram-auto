# Generated by Django 2.2.1 on 2019-07-26 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0013_auto_20190725_1905'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='expected_price',
            field=models.FloatField(default=20),
            preserve_default=False,
        ),
    ]
