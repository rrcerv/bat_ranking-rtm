# Generated by Django 4.2.13 on 2024-06-27 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0009_user_territorio'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ranking_br',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='ranking_bu',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='ranking_tv',
            field=models.IntegerField(default=0),
        ),
    ]