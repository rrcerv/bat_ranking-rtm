from django.contrib import admin
from .models import RankingGerentes, RankingVendedores, RankingRegionais

# Register your models here.
admin.site.register(RankingVendedores)
admin.site.register(RankingGerentes)
admin.site.register(RankingRegionais)