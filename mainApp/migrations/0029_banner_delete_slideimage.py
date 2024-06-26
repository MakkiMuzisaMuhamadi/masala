# Generated by Django 5.0.4 on 2024-04-14 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0028_bannertexts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(default='', max_length=100)),
                ('price', models.DecimalField(decimal_places=0, default=0, max_digits=50)),
                ('text', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='banner_images/')),
            ],
        ),
        migrations.DeleteModel(
            name='SlideImage',
        ),
    ]
