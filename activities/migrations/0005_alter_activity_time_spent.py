# Generated by Django 3.2.9 on 2022-01-22 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0004_alter_activity_time_spent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='time_spent',
            field=models.IntegerField(),
        ),
    ]
