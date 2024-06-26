# Generated by Django 4.2.13 on 2024-06-27 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking_rtm', '0006_rankinggerentes_date_rankingregionais_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RankingTerritorioRegional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regional', models.CharField(choices=[('SUL', 'SUL'), ('SPR', 'SPR'), ('SPC', 'SPC'), ('RIO', 'RIO'), ('CTO', 'CTO'), ('NNE', 'NNE')], default='SUL', max_length=5)),
                ('territorio', models.CharField(default='-', max_length=100)),
                ('points', models.IntegerField(default=0)),
                ('date', models.DateField(default='2021-01-01')),
            ],
        ),
    ]
