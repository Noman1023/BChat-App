# Generated by Django 3.0.5 on 2020-08-25 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0010_auto_20200825_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_online',
            field=models.BooleanField(default=False),
        ),
    ]
