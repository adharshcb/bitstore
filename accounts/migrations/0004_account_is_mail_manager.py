# Generated by Django 4.0.5 on 2022-07-11 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_account_is_banned'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_mail_manager',
            field=models.BooleanField(default=False),
        ),
    ]
