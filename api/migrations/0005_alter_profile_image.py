# Generated by Django 5.0 on 2024-01-29 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_profile_bio_alter_profile_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='user_images'),
        ),
    ]
