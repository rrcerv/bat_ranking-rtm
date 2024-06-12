# Generated by Django 4.2.13 on 2024-06-11 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking_rtm', '0004_delete_rankingregionais'),
    ]

    operations = [
        migrations.CreateModel(
            name='RankingRegionais',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regional', models.CharField(choices=[('SUL', 'SUL'), ('SPR', 'SPR'), ('SPC', 'SPC'), ('RIO', 'RIO'), ('CTO', 'CTO'), ('NNE', 'NNE')], default='SUL', max_length=5)),
                ('value', models.IntegerField(default=0)),
                ('updatedAt', models.DateTimeField()),
            ],
        ),
    ]
