# Generated by Django 3.2.9 on 2021-12-15 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_auto_20211208_1505'),
    ]

    operations = [
        migrations.RunSQL("ALTER TABLE activities_activity ALTER time_spent TYPE INTEGER USING EXTRACT(epoch FROM time_spent)")
    ]