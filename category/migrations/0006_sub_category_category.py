# Generated by Django 4.0.5 on 2022-07-24 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0005_remove_sub_category_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sub_category',
            name='category',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='category.category'),
            preserve_default=False,
        ),
    ]