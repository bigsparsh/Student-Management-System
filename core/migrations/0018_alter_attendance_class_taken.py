# Generated by Django 4.2.7 on 2023-12-04 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_attendance_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='class_taken',
            field=models.IntegerField(default=0),
        ),
    ]
