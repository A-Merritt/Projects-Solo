# Generated by Django 3.2.7 on 2021-10-08 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VetsConnect', '0004_auto_20211005_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
