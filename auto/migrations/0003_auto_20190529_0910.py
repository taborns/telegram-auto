# Generated by Django 2.2.1 on 2019-05-29 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0002_auto_20190529_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskpackage',
            name='entity_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='packages', to='auto.Entity'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='entity_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='auto.Entity'),
        ),
    ]
