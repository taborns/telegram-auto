# Generated by Django 2.2.1 on 2019-07-25 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0011_auto_20190725_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='runningtask',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
