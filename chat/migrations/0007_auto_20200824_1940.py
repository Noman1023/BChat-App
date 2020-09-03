# Generated by Django 3.0.5 on 2020-08-24 14:40

import chat.models
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_auto_20200824_0832'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='handle',
        ),
        migrations.RemoveField(
            model_name='message',
            name='room',
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='thread',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.Thread'),
        ),
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='user.jpg', storage=django.core.files.storage.FileSystemStorage(base_url='/media//my_sell', location='C:\\Users\\Nouman\\PycharmProjects\\chitchat\\media/my_sell'), upload_to=chat.models.image_directory_path),
        ),
    ]