# Generated by Django 5.0.6 on 2024-06-17 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_api', '0002_alter_appuser_username_alter_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
    ]
