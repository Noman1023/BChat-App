# Generated by Django 3.0.5 on 2020-08-25 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_auto_20200825_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image_height',
            field=models.PositiveIntegerField(blank=True, default='100', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='image_width',
            field=models.PositiveIntegerField(blank=True, default='100', null=True),
        ),
    ]
