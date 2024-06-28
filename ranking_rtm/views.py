from django.shortcuts import render
from django.http import JsonResponse
from .models import RankingGerentes, RankingVendedores, RankingRegionais, User, RankingTerritorioRegional, User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q
import datetime
from django.utils import timezone
import os
import glob

import re
import json
import base64
from PIL import Image # PRECISA INSTALAR NO SERVIDOR
from io import BytesIO
import random
import pandas as pd

# CRIPTOGRAFIA -- PRECISA INSTALAR NO SERVIDOR pycryptodome
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import environ
env = environ.Env()
environ.Env.read_env()

# VARIÁVEIS GLOBAIS
path_user_images = env('PATH_USER_IMAGES')


# FUNÇÕES 

# CRIPTOGRAFIA
def encrypt(message):

    chave_separadora = env('cripto_chave_separadora')
    salt = env('cripto_salt')
    password = env('cripto_password')
    key = PBKDF2(password, salt, dkLen=32)

    cipher = AES.new(key, AES.MODE_CBC)

    cipher_data = cipher.encrypt(pad(message.encode(), AES.block_size))

    encriptado = (cipher_data)

    iv = cipher.iv

    encriptado = base64.urlsafe_b64encode(encriptado).decode('utf-8')
    
    iv = base64.urlsafe_b64encode(iv).decode('utf-8')

    return encriptado + chave_separadora + iv

def decrypt(encriptado):
    chave_separadora = env('cripto_chave_separadora')
    salt = env('cripto_salt')
    password = env('cripto_password')

    encriptado = encriptado.split(chave_separadora)
    
    
    iv = encriptado[1]
    encriptado = encriptado[0]

    encriptado = base64.urlsafe_b64decode(encriptado.encode('utf-8'))
    iv = base64.urlsafe_b64decode(iv.encode('utf-8'))
    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_CBC, iv = iv)

    decrypted_text = unpad(cipher.decrypt(encriptado), AES.block_size).decode()

    return (decrypted_text)

def encrypt_iv_fixo(message):
    salt = env('cripto_salt')
    password = env('cripto_password')
    key = PBKDF2(password, salt, dkLen=32)

    iv_fixo=b'ZJ\xc4D\x15\xc9jy\x13\xfdD\x15v\xec\x19l'

    cipher = AES.new(key, AES.MODE_CBC, iv=iv_fixo)

    cipher_data = cipher.encrypt(pad(message.encode(), AES.block_size))

    encriptado = (cipher_data)

    encriptado = base64.urlsafe_b64encode(encriptado).decode('utf-8')

    return encriptado

def decrypt_iv_fixo(encriptado):
    salt = env('cripto_salt')
    password = env('cripto_password')
    
    iv_fixo=b'ZJ\xc4D\x15\xc9jy\x13\xfdD\x15v\xec\x19l'

    encriptado = base64.urlsafe_b64decode(encriptado.encode('utf-8'))

    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_CBC, iv = iv_fixo)

    decrypted_text = unpad(cipher.decrypt(encriptado), AES.block_size).decode()

    return (decrypted_text)
# FIM CRIPTOGRAFIA 

def extract_image_data(base64_string):
    # Regex to extract the data part and the format
    pattern = re.compile(r'data:image/(?P<type>[a-zA-Z]+);base64,(?P<data>.+)')
    match = pattern.match(base64_string)
    
    if not match:
        raise ValueError("Invalid base64 image string")
    
    image_type = match.group('type')
    image_data = match.group('data')
    
    return image_type, image_data

def user_has_photo(matricula):
    global path_user_images

    enc_matricula = encrypt_iv_fixo(matricula)

    path = path_user_images + enc_matricula + '.*'

    if glob.glob(path):
        path_arquivo = (glob.glob(path)[0])
        split = path_arquivo.split('\\')
        arquivo = split[len(split)-1]
        return arquivo
    else:
        return


# RANKING REGIONAIS

def generate_ranking():
    json = {}

    random_object = RankingRegionais.objects.get(id=1)
    choices_regionais = random_object._meta.get_field('regional').choices

    for regional in choices_regionais:
        json[regional[0]] = 0

    usuarios = User.objects.all()

    for usuario in usuarios:
        regional = usuario.regional
        
        if usuario.role == 'GRM' or usuario.role == 'GTV':
            ranking_model = RankingGerentes.objects.get(usuario=usuario)
            json[regional]+=ranking_model.pontos_acumulados
         
        elif usuario.role == 'Vendedor':
            ranking_model = RankingVendedores.objects.get(usuario=usuario)
            json[regional]+=ranking_model.pontos_acumulados

        # LÓGICA DE LOOP PELAS VARIÁVEIS DE KPI PARA ACUMULAR OS PONTOS -- EM DESUSO POR JÁ TER OS PONTOS ACUMULADOS
        #if usuario.role == 'GTM' or usuario.role == 'GTV':
        #    regional = usuario.regional
        #    ranking_model = RankingGerentes.objects.get(usuario=usuario)
        #    for field in ranking_model._meta.fields:
        #        if field.name == 'usuario':
        #            pass
        #        elif field.name == 'id':
        #            pass
        #        elif field.name == 'date':
        #            pass
        #        else:
        #            points = getattr(ranking_model, field.name)
        #            json[regional] += points
        #        
#
        #elif usuario.role == 'Vendedor':
        #    regional=usuario.regional
        #    ranking_model = RankingVendedores.objects.get(usuario=usuario)
        #    for field in ranking_model._meta.fields:
        #        if field.name == 'usuario':
        #            pass
        #        elif field.name == 'id':
        #            pass
        #        elif field.name == 'date':
        #            pass
        #        else:
        #            points = getattr(ranking_model, field.name)
        #            json[regional] += points

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

    ranking_regionais = RankingRegionais.objects.all().order_by('-value')


    return ranking_regionais

# FIM RANKING REGIONAIS


# RANKING TERRITÓRIO POR REGIONAL

# ESSA FUNÇÃO GERA O RANKING
def gen_ranking_territorios_regional():
    objetos = RankingTerritorioRegional.objects.all()

    for objeto in objetos:
        objeto.delete()
    
    usuarios = User.objects.all()

    json = {} # JSON TOTAL

    for usuario in usuarios:
        print(usuario.role)
        json_usuario = {} # JSON INDIVIDUAL
        # ITERA SOBRE TODOS OS TERRITORIOS DE GERENTES E ARMAZENA NO JSON OS DADOS DO ACUMULADO
        if usuario.role == 'GRM' or usuario.role == 'GTV':
            condition1= Q(usuario=usuario)
            ranking_model = RankingGerentes.objects.get(condition1)

            regional = usuario.regional
            territorio = usuario.territorio
            total_pontos= ranking_model.pontos_acumulados
            data=ranking_model.date

            print(json)
            print(usuario.territorio)
            # SE O TERRITÓRIO JÁ EXISTE NO JSON, SOMA OS PONTOS
            if regional+territorio in json:
                print('if')
                json[regional+territorio]['pontos_acumulados'] = json[regional+territorio]['pontos_acumulados'] + total_pontos
            # CASO CONTRÁRIO, CRIA UM TERRITÓRIO NOVO
            else:
                print('else')
                json_usuario['regional'] = regional
                json_usuario['territorio'] = territorio
                json_usuario['pontos_acumulados'] = total_pontos
                json_usuario['data'] = data
                json[regional+territorio] = json_usuario
                
        # ITERA SOBRE TODOS OS TERRITÓRIOS DOS VENDEDORES E ARMAZENA NO JSON OS DADOS DO ACUMULADO 
        elif usuario.role == 'Vendedor':
            condition1 = Q(usuario=usuario)
            ranking_model = RankingVendedores.objects.get(condition1)

            regional = usuario.regional
            territorio = usuario.territorio
            total_pontos = ranking_model.pontos_acumulados
            data = ranking_model.date

            # SE O TERRITÓRIO JÁ EXISTE NO JSON, SOMA OS PONTOS
            if regional+territorio in json:
                json[regional+territorio]['pontos_acumulados'] = json[regional+territorio]['pontos_acumulados'] + total_pontos
            # CASO CONTRÁRIO, CRIA UM TERRITÓRIO NOVO
            else:
                json_usuario['regional'] = regional
                json_usuario['territorio'] = territorio
                json_usuario['pontos_acumulados'] = total_pontos
                json_usuario['data'] = data
                json[regional+territorio] = json_usuario
    
    for key, value in json.items():

        try:
            condition1 = Q(territorio=value['territorio'])
            condition2 = Q(regional = value['regional'])
            condition3 = Q(date= value['data'])
            object = RankingTerritorioRegional.objects.get(condition1 & condition2 & condition3)

            object.territorio = value['territorio']
            object.regional = value['regional']
            object.points = value['pontos_acumulados']
            object.date = value['data']
            object.save()

        except:
            object = RankingTerritorioRegional(territorio=value['territorio'], regional=value['regional'], points=value['pontos_acumulados'], date=value['data'])
            object.save()


def retrieve_ranking_territorios_regional(regional):
    objects = RankingTerritorioRegional.objects.filter(regional=regional).order_by('-points')
    
    return objects

# FIM RANKING TERRITÓRIO POR REGIONAL

def get_pontos(element):
    return element['pontos_acumulados']

def retrieve_ranking_vendedores_territorio(territorio, regional):
    condition1=Q(territorio=territorio)
    condition2=Q(regional=regional)
    usuarios_territorio = User.objects.filter(condition1, condition2)
    lista=[]
    for usuario in usuarios_territorio:
        if (usuario.role == 'Vendedor'):
            json_usuario = {}

            for field in usuario._meta.fields:
                if field.name == 'password':
                    pass
                attr = getattr(usuario, field.name)
                json_usuario[field.name] = attr

            try:
                ranking_model = RankingVendedores.objects.get(usuario=usuario)

                json_usuario['pontos_acumulados'] = ranking_model.pontos_acumulados
                json_usuario['ranking_bu'] = ranking_model.ranking_bu
                json_usuario['ranking_br'] = ranking_model.ranking_br
                json_usuario['ranking_tv'] = ranking_model.ranking_tv
            except:
                json_usuario['pontos_acumulados'] = 0
            
            lista.append(json_usuario)
        else:
            pass
        
    lista.sort(key=get_pontos, reverse=True)

    return lista

def retrieve_ranking_vendedores_bu(regional):
    condition2=Q(regional=regional)
    usuarios_territorio = User.objects.filter(condition2)
    lista=[]
    for usuario in usuarios_territorio:
        if (usuario.role == 'Vendedor'):
            json_usuario = {}

            for field in usuario._meta.fields:
                if field.name == 'password':
                    pass
                attr = getattr(usuario, field.name)
                json_usuario[field.name] = attr

            try:
                ranking_model = RankingVendedores.objects.get(usuario=usuario)

                json_usuario['pontos_acumulados'] = ranking_model.pontos_acumulados
                json_usuario['ranking_bu'] = ranking_model.ranking_bu
                json_usuario['ranking_br'] = ranking_model.ranking_br
                json_usuario['ranking_tv'] = ranking_model.ranking_tv
            except:
                json_usuario['pontos_acumulados'] = 0
            
            lista.append(json_usuario)
        else:
            pass
        
    lista.sort(key=get_pontos, reverse=True)

    return lista


# Create your views here.

@login_required
def index(request):
    usuario = request.user
    ambient = env('AMBIENT') 

    ranking_regionais = retrieve_ranking_regionais()


    gen_ranking_territorios_regional()
    ranking_t_r = retrieve_ranking_territorios_regional(regional=usuario.regional)

    if usuario.role == 'Vendedor':
        role = 'Vendedor'
        ranking = RankingVendedores.objects.get(usuario=usuario)

        if (user_has_photo(usuario.matricula)):
            arquivo_foto = user_has_photo(usuario.matricula)

            if(ambient == 'dev'):
                pass
            elif(ambient == 'prod'):
                arquivo_foto_split = arquivo_foto.split('/')
                arquivo_foto = arquivo_foto_split[len(arquivo_foto_split)-1]
        else:
            arquivo_foto = ''

        json = {}
        total_points = 0
        max_points = 1800

        for field in ranking._meta.fields:
            if field.name == 'usuario':
                json['nome'] = usuario.name
            elif field.name == 'id':
                json['id'] = usuario.id
            elif field.name == 'date':
                json['date'] = getattr(ranking, 'date')
            else:
                json[f'{field.name}'] = getattr(ranking, field.name)
                total_points+= getattr(ranking, field.name)

        percentage = int((total_points/max_points)*100)


        random_number = random.randint(1,100)

        ranking_vendedores_territorio = retrieve_ranking_vendedores_territorio(usuario.territorio, usuario.regional)

        return render(request, 'ranking_vendedores.html', {
            'ranking': json,
            'percentage': percentage,
            'ranking_regionais': ranking_regionais,
            'usuario': usuario,
            'arquivo_foto': arquivo_foto,
            'random_number': random_number,
            'ambient': ambient,
            'a': 0,
            'ranking_v_t': ranking_vendedores_territorio,
            'ranking_t_r': ranking_t_r
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
            elif field.name == 'date':
                json['date'] = getattr(ranking, 'date')
            else:
                json[f'{field.name}'] = getattr(ranking, field.name)
                total_points += getattr(ranking, field.name)

        percentage = int((total_points/max_points)*100)


        return render(request, 'ranking_gerentes.html', {
            'ranking': json,
            'percentage': percentage,
            'ranking_regionais': ranking_regionais,
            'usuario': usuario
        })

    elif usuario.role == 'GRM':
        role = 'Gerente'
        ranking = RankingGerentes.objects.get(usuario=usuario)

        ranking_v_bu = retrieve_ranking_vendedores_bu(usuario.regional)
        print(ranking_v_bu)


        json = {}
        total_points = 0
        max_points = 2400

        for field in ranking._meta.fields:
            if field.name == 'usuario':
                json['nome'] = usuario.name
            elif field.name == 'id':
                json['id'] = usuario.id
            elif field.name == 'date':
                json['date'] = getattr(ranking, 'date')
            else:
                json[f'{field.name}'] = getattr(ranking, field.name)
                total_points += getattr(ranking, field.name)

        percentage = int((total_points/max_points)*100)


        return render(request, 'ranking_grm.html', {
            'ranking': json,
            'percentage': percentage,
            'ranking_regionais': ranking_regionais,
            'usuario': usuario,
            'ranking_v_bu':ranking_v_bu,
            'ranking_t_r':ranking_t_r
        })

    elif usuario.role == 'GTV':
        role = 'Gerente'
        ranking = RankingGerentes.objects.get(usuario=usuario)

        ranking_v_t = retrieve_ranking_vendedores_territorio(usuario.territorio, usuario.regional)

        json = {}
        total_points = 0
        max_points = 2400

        for field in ranking._meta.fields:
            if field.name == 'usuario':
                json['nome'] = usuario.name
            elif field.name == 'id':
                json['id'] = usuario.id
            elif field.name == 'date':
                json['date'] = getattr(ranking, 'date')
            else:
                json[f'{field.name}'] = getattr(ranking, field.name)
                total_points += getattr(ranking, field.name)

        percentage = int((total_points/max_points)*100)


        return render(request, 'ranking_gtv.html', {
            'ranking': json,
            'percentage': percentage,
            'ranking_regionais': ranking_regionais,
            'usuario': usuario,
            'ranking_v_t': ranking_v_t,
            'ranking_t_r': ranking_t_r
        })
     

@login_required
def teste_crop_image(request):
    return render(request, 'teste_crop_image.html')

# APIS
@login_required
def upload_user_image(request):
    global path_user_images
    if request.method == 'POST':
        usuario = request.user
        arquivo_foto_usuario = user_has_photo(usuario.matricula)
        encrypted_matricula = encrypt_iv_fixo(usuario.matricula)

        data = json.loads(request.body.decode('utf-8'))

        foto_base64 = data['userImage']
        bounding_box = (data['boundingBox'])

        tipo, imagem = extract_image_data(foto_base64)
        img = Image.open(BytesIO(base64.b64decode(imagem)))
        
        img = img.crop((bounding_box['left'], bounding_box['top'], bounding_box['right'], bounding_box['bottom']))

        path_user_image = path_user_images + f'{encrypted_matricula}.{tipo}'

        ambient = env('AMBIENT')

        if(ambient == 'dev'):
            if arquivo_foto_usuario:
                os.remove(path_user_images + arquivo_foto_usuario)
        elif (ambient == 'prod'):
            if arquivo_foto_usuario:
                os.remove(path_user_image)


        img.save(path_user_image)
        
        return JsonResponse({'Response': 'Ok'})
    else:
        return JsonResponse({'Response': 'Metodo nao autorizado'}, status=418)




# API PARA FAZER UPDATE DA BASE.
# O ARQUIVO EXCEL DEVE SER UM MERGE ENTRE AS PLANILHAS DE DATA DE NASCIMENTO E RANKINGS
@login_required
def update_base(request):
    result=pd.read_excel('output.xlsx')

    for line in result.iterrows():
        line = line[1]

        # USER
        matricula = line['Matricula']
        regional = line['BU_x'].strip().upper()
        territorio = line['TV']

        if(territorio == '-'):
            continue
        else:
            pass

        if line['FUNÇÃO'] == 'VENDEDOR':
            role = line['FUNÇÃO'].title()
        else:
            role = line['FUNÇÃO'].strip().upper()

        dia = str(line['dia']).zfill(2)
        mes = str(line['mês']).zfill(2)
        ano = str(line['ano']).zfill(2)

        name=line['RECURSO']

        password= dia+mes+ano
        print(name, matricula, role, regional, territorio, password)

        try:
            object_user = User(name=name, matricula = matricula, regional=regional, territorio=territorio, role=role)
            object_user.set_password(password)
            object_user.save()
            last_user = object_user
        except:
            print('Fail')
            pass
        

        # SETANDO RANKING
        if role == 'GRM' or role == 'GTV':
            pts_ytd_direto = line['PTS YTD DIRETO']
            efetividade = line['EFETIVIDADE']
            faturamento = line['FATURAMENTO']
            positivacao = line['POSITIVAÇÃO']
            cobertura_vol_prime = line['COBERTURA DE VOLUME PRIME']
            adimplencia_prime = line['ADIMPLÊNCIA PRIME']
            id_ulp = line['ID ULP']
            base= line['BASE']
            pts_share_ka_cnv = line['PTS SHARE KA CNV']
            pts_divers_portfolio = ['PTS DIVERS. PORTFÓLIO PARCERIA']
            boost = ['BOOST']
            print(object_user, pts_ytd_direto, efetividade, faturamento, positivacao, cobertura_vol_prime, adimplencia_prime, id_ulp, base)
            object_ranking = RankingGerentes(usuario=object_user, pts_ytd_direto=pts_ytd_direto, efetividade=efetividade,
                            faturamento=faturamento, positivacao=positivacao, cobertura_vol_prime=cobertura_vol_prime,
                            adimplencia_prime=adimplencia_prime, id_ulp=id_ulp, base=base, pts_share_ka_cnv=pts_share_ka_cnv,
                            pts_divers_portfolio=pts_divers_portfolio, boost=boost)
            object_ranking.save()

        elif role=='Vendedor':
            efetividade = line['EFETIVIDADE']
            faturamento = line['FATURAMENTO']
            positivacao = line['POSITIVAÇÃO']
            cobertura_vol_prime = line['COBERTURA DE VOLUME PRIME']
            adimplencia_prime = line['ADIMPLÊNCIA PRIME']
            id_ulp = line['ID ULP']
            base= line['BASE']
            object_ranking = RankingVendedores(usuario=object_user, efetividade=efetividade, faturamento=faturamento,
                                               positivacao=positivacao, cobertura_vol_prime=cobertura_vol_prime,
                                               adimplencia_prime=adimplencia_prime, id_ulp=id_ulp, base=base)
            object_ranking.save()

    return JsonResponse({'Response': 'OK'})