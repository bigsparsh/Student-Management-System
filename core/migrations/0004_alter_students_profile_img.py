# Generated by Django 4.2.7 on 2023-12-01 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_teachers_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='profile_img',
            field=models.ImageField(default='blank_profile_picture.jpg', null=True, upload_to='profile_images'),
        ),
    ]