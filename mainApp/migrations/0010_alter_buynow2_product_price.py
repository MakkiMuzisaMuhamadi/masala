# Generated by Django 5.0.4 on 2024-04-06 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0009_remove_buynow2_product_brand_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buynow2',
            name='product_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
