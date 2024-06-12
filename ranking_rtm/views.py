from django.shortcuts import render
from django.http import JsonResponse
from .models import RankingGerentes, RankingVendedores, RankingRegionais, User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import datetime
from django.utils import timezone

# Create your views here.

def generate_ranking():
    json = {}

    random_object = RankingRegionais.objects.get(id=1)
    choices_regionais = random_object._meta.get_field('regional').choices

    for regional in choices_regionais:
        json[regional[0]] = 0

    usuarios = User.objects.all()

    for usuario in usuarios:


        if usuario.role == 'Gerente':
            regional = usuario.regional
            ranking_model = RankingGerentes.objects.get(usuario=usuario)
            for field in ranking_model._meta.fields:
                if field.name == 'usuario':
                    pass
                elif field.name == 'id':
                    pass
                else:
                    points = getattr(ranking_model, field.name)
                    json[regional] += points
                

        elif usuario.role == 'Vendedor':
            regional=usuario.regional
            ranking_model = RankingVendedores.objects.get(usuario=usuario)
            for field in ranking_model._meta.fields:
                if field.name == 'usuario':
                    pass
                elif field.name == 'id':
                    pass
                else:
                    points = getattr(ranking_model, field.name)
                    json[regional] += points

    print(json)
    current_time = timezone.now()

    for key, value in json.items():
        model_object = RankingRegionais.objects.get(regional=key)
        setattr(model_object, 'value', value)
        setattr(model_object, 'updatedAt', current_time)
        model_object.save()

def retrieve_ranking_regionais():
    ranking_regional_object = RankingRegionais.objects.all()[:1]
    day_plus_1 = ranking_regional_object[0].updatedAt + timezone.timedelta(days=1)

    generate_ranking()

    if (timezone.now() > day_plus_1):
        generate_ranking()
    else:
        pass

    ranking_regionais = RankingRegionais.objects.all().order_by('value')[3:]

    return ranking_regionais

@login_required
def index(request):
    
    usuario = request.user

    ranking_regionais = retrieve_ranking_regionais()

    if usuario.role == 'Vendedor':
        role = 'Vendedor'
        ranking = RankingVendedores.objects.get(usuario=usuario)

        json = {}
        total_points = 0
        max_points = 1800

        for field in ranking._meta.fields:
            if field.name == 'usuario':
                json['nome'] = usuario.name
            elif field.name == 'id':
                json['id'] = usuario.id
            else:
                json[f'{field.name}'] = getattr(ranking, field.name)
                total_points+= getattr(ranking, field.name)

        percentage = int((total_points/max_points)*100)


        return render(request, 'ranking_vendedores.html', {
            'ranking': json,
            'percentage': percentage,
            'ranking_regionais': ranking_regionais,
            'usuario': usuario
        })


    elif usuario.role == 'Gerente':
        role = 'Gerente'
        ranking = RankingGerentes.objects.get(usuario=usuario)


        json = {}
        total_points = 0
        max_points = 2400

        for field in ranking._meta.fields:
            if field.name == 'usuario':
                json['nome'] = usuario.name
            elif field.name == 'id':
                json['id'] = usuario.id
            else:
                json[f'{field.name}'] = getattr(ranking, field.name)
                total_points += getattr(ranking, field.name)

        percentage = int((total_points/max_points)*100)

        print(json)
        print(percentage)

        return render(request, 'ranking_gerentes.html', {
            'ranking': json,
            'percentage': percentage,
            'ranking_regionais': ranking_regionais,
            'usuario': usuario
        })
