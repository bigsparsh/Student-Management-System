# Generated by Django 4.2.7 on 2023-12-04 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_remove_attendance_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='percentage',
            field=models.IntegerField(default=0),
        ),
    ]