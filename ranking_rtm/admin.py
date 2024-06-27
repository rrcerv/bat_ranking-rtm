from django.contrib import admin
from .models import RankingGerentes, RankingVendedores, RankingRegionais, RankingTerritorioRegional

# Register your models here.
admin.site.register(RankingVendedores)
admin.site.register(RankingGerentes)
admin.site.register(RankingRegionais)
admin.site.register(RankingTerritorioRegional)