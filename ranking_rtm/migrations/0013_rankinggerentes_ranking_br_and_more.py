# Generated by Django 4.2.13 on 2024-07-01 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking_rtm', '0012_rename_base_de_varejos_rankingvendedores_base_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rankinggerentes',
            name='ranking_br',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='rankinggerentes',
            name='ranking_bu',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='rankinggerentes',
            name='ranking_tv',
            field=models.IntegerField(default=0),
        ),
    ]
