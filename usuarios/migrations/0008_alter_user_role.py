# Generated by Django 4.2.13 on 2024-06-27 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0007_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Vendedor', 'Vendedor'), ('Gerente', 'Gerente'), ('GRM', 'GRM'), ('GTV', 'GTV')], default='Vendedor', max_length=20),
        ),
    ]