# Generated by Django 4.0.5 on 2022-07-13 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_account_is_mail_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to='photos/profile_images/'),
        ),
    ]
