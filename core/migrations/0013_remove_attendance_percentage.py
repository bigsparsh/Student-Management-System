# Generated by Django 4.2.7 on 2023-12-04 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_attendance_class_taken_attendance_total_class_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='percentage',
        ),
    ]
