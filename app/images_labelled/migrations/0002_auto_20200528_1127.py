# Generated by Django 2.2.6 on 2020-05-28 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images_labelled', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagelabelled',
            name='image',
            field=models.ImageField(upload_to='labelled', verbose_name='uploaded image'),
        ),
    ]