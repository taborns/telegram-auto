# Generated by Django 2.2.1 on 2019-07-24 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0008_auto_20190724_0937'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='target_member_count',
            field=models.IntegerField(default=20000),
            preserve_default=False,
        ),
    ]
