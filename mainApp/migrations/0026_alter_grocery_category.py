# Generated by Django 5.0.4 on 2024-04-13 06:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0025_grocery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grocery',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mainApp.grocerycategory'),
        ),
    ]
