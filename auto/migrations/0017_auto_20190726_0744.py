# Generated by Django 2.2.1 on 2019-07-26 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0016_auto_20190726_0743'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='created_at',
            new_name='transaction_time',
        ),
    ]
