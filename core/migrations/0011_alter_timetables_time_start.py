# Generated by Django 4.2.7 on 2023-12-04 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_timetables_time_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetables',
            name='time_start',
            field=models.TimeField(),
        ),
    ]
