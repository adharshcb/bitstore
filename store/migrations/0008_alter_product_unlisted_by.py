# Generated by Django 4.0.5 on 2022-07-02 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_product_unlisted_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='unlisted_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
