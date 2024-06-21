from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.http import JsonResponse
from .models import User
import json

# Create your views here.

def login(request):
        usuario = request.user.is_anonymous
        
        if request.user.is_anonymous:

            if request.method == 'POST':

                body = request.POST

                matricula = str(body.get('matricula', '0'))
                senha = body.get('Senha', '0')

                usuario = authenticate(matricula=matricula, password=senha)

                if usuario is not None:
                    auth_login(request, usuario)
                    return redirect('index')
                else:
                    return render(request, 'login.html', {
                        'status': '20'
                    })
                
            else:
                return render(request, 'login.html', {
                    'status': '0'
                })
        else:
             return redirect('index')

def logout_view(request):
    logout(request)
    return redirect('login')