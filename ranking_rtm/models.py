from django.db import models
from usuarios.models import User

# Create your models here.
class RankingGerentes(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ranking_gerente')

    pts_ytd_direto = models.IntegerField(null=False, default=0)
    efetividade = models.IntegerField(null=False, default=0)
    faturamento = models.IntegerField(null=False, default=0)
    positivacao = models.IntegerField(null=False, default=0)
    cobertura_vol_prime = models.IntegerField(null=False, default=0)
    adimplencia_prime = models.IntegerField(null=False, default=0)
    id_ulp = models.IntegerField(null=False, default=0)
    base = models.IntegerField(null=False, default=0)
    pts_share_ka_cnv = models.IntegerField(null=False, default=0)
    pts_divers_portfolio = models.IntegerField(null=False, default=0)
    boost = models.IntegerField(null=False, default=0)

    pontos_acumulados = models.IntegerField(null=False, blank=False, default=0)

    date = models.DateField(default='2021-01-01')





class RankingVendedores(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ranking_vendedor')
    efetividade = models.IntegerField(null=False, default=0)
    positivao_parcial = models.IntegerField(null=False, default=0)
    adimplencia_prime = models.IntegerField(null=False, default=0)
    id_ulp = models.IntegerField(null=False, default=0)
    faturamento_parc = models.IntegerField(null=False, default=0)
    digital = models.IntegerField(null=False, default=0)
    base_de_varejos = models.IntegerField(null=False, default=0)
    vol_prime = models.IntegerField(null=False, default=0)
    boost = models.IntegerField(null=False, default=0)

    pontos_acumulados = models.IntegerField(null=False, blank=False, default=0)

    ranking_tv = models.IntegerField(null=False, blank=False, default=0)
    ranking_bu = models.IntegerField(null=False, blank=False, default=0)
    ranking_br = models.IntegerField(null=False, blank=False, default=0)

    date = models.DateField(default='2021-01-01')


class RankingRegionais(models.Model):
    SUL = 'SUL'
    SPR = 'SPR'
    SPC = 'SPC'
    RIO = 'RIO'
    CTO = 'CTO'
    NNE = 'NNE'

    REGIONAIS_CHOICES = (
        (SUL, 'SUL'),
        (SPR, 'SPR'),
        (SPC, 'SPC'),
        (RIO, 'RIO'),
        (CTO, 'CTO'),
        (NNE, 'NNE')
    )

    regional = models.CharField(max_length=5, choices=REGIONAIS_CHOICES, default=SUL)
    value = models.IntegerField(null=False, blank=False, default=0)
    updatedAt = models.DateTimeField(null=False,blank=False)

    date = models.DateField(default='2021-01-01')


class RankingTerritorioRegional(models.Model):
    SUL = 'SUL'
    SPR = 'SPR'
    SPC = 'SPC'
    RIO = 'RIO'
    CTO = 'CTO'
    NNE = 'NNE'

    REGIONAIS_CHOICES = (
        (SUL, 'SUL'),
        (SPR, 'SPR'),
        (SPC, 'SPC'),
        (RIO, 'RIO'),
        (CTO, 'CTO'),
        (NNE, 'NNE')
    )

    regional = models.CharField(max_length=5, choices=REGIONAIS_CHOICES, default=SUL)

    territorio = models.CharField(max_length=100, default='-')

    points = models.IntegerField(null=False, blank=False, default=0)

    date = models.DateField(default='2021-01-01')
