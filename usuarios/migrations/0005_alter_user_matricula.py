# Generated by Django 4.2.13 on 2024-06-12 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_user_regional'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='matricula',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
