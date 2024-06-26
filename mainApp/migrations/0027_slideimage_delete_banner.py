# Generated by Django 5.0.4 on 2024-04-13 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0026_alter_grocery_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='SlideImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='slides/')),
                ('alt_text', models.CharField(max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='Banner',
        ),
    ]
