# Generated by Django 2.1.2 on 2018-12-13 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studserviceapp', '0004_auto_20181213_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='slika',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
