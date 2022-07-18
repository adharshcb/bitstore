# Generated by Django 4.0.5 on 2022-06-29 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_carousel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='images',
        ),
        migrations.AddField(
            model_name='images',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.product'),
            preserve_default=False,
        ),
    ]
