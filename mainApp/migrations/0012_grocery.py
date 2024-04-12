# Generated by Django 5.0.4 on 2024-04-12 06:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0011_buynow2_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grocery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=0, max_digits=50)),
                ('image', models.ImageField(upload_to='grocery_item_images/')),
                ('rating', models.DecimalField(decimal_places=1, max_digits=3)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mainApp.category')),
            ],
        ),
    ]