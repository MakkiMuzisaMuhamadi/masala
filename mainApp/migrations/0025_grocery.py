# Generated by Django 5.0.4 on 2024-04-13 06:51

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0024_grocerycategory_delete_grocery'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grocery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=0, max_digits=50)),
                ('image_main', models.ImageField(upload_to='grocery_item_images/')),
                ('image_1', models.ImageField(blank=True, upload_to='grocery_item_images/')),
                ('image_2', models.ImageField(blank=True, upload_to='grocery_item_images/')),
                ('image_3', models.ImageField(blank=True, upload_to='grocery_item_images/')),
                ('product_type', models.CharField(default='Grocery', editable=False, max_length=10)),
                ('category', models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='mainApp.grocerycategory')),
            ],
        ),
    ]
