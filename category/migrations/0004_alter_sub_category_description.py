# Generated by Django 4.0.5 on 2022-07-03 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_alter_sub_category_sub_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sub_category',
            name='description',
            field=models.TextField(),
        ),
    ]
