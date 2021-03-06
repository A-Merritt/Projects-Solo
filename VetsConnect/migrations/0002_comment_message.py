# Generated by Django 3.2.7 on 2021-10-05 02:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('VetsConnect', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='VetsConnect.user')),
                ('users_who_liked', models.ManyToManyField(related_name='messages_user_liked', to='VetsConnect.User')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='VetsConnect.user')),
                ('message', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='VetsConnect.message')),
                ('users_who_liked', models.ManyToManyField(related_name='comments_user_liked', to='VetsConnect.User')),
            ],
        ),
    ]
