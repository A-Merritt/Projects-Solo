# Generated by Django 3.2.7 on 2021-10-05 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VetsConnect', '0002_comment_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Branch_of_Service',
            field=models.CharField(choices=[('Army', 'ARMY'), ('Navy', 'NAVY'), ('Marines', 'MARINES'), ('Air Force', 'AIR FORCE'), ('Coast Guard', 'COAST GUARD'), ('Space Force', 'SPACE FORCE')], default='Please Select your Branch', max_length=30),
        ),
    ]
