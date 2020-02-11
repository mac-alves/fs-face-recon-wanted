from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import PerfilForm, UserForm
from .models import Usuario, Procurados
from django.conf import settings

#treinamento facereconhecimento
import face_recognition
import pickle
import pymysql.cursors
import numpy as np
import os

# Create your views here.

# função pra leitura do arquivo .dat pro treinamento
def read_file(filename):
    with open(filename, 'rb') as f:
        encodings = f.read()
    return encodings
#---------------------------------------------------
#funão para apagar arquivo de treinamento do diretorio
def apagatreina(diretorio):
    for raiz, diretorios, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            if arquivo.endswith('.dat'):
                os.remove(os.path.join(raiz, arquivo))
#------------------------------------------------------

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'act':'active'})
    else:
        perfil = request.user

        return render(request, 'index.html', {'perfil': perfil, 'act':'active'})

def perfis(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'act':'active'})
    else:
        perfils = Usuario.objects.filter(user=request.user)
        query = request.GET.get("q")
        if query:
            perfils = perfils.filter(
                Q(nome__icontains=query) |
                Q(email__icontains=query)
            ).distinct()
            return render(request, 'perfis.html', {
                'perfils': perfils,
                'act':'active',
            })
        else:
            return render(request, 'perfis.html', {'perfils': perfils, 'act':'active'})

def create_peril(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'act':'active'})
    else:
        form = PerfilForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.user = request.user
            perfil.foto = request.FILES['foto']
            file_type = perfil.foto.url.split('.')[-1]
            file_type = file_type.lower()
            nada = perfil.foto.url
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'perfil': perfil,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                    'act':'active',

                }
                return render(request, 'create_perfil.html', context)
            perfil.save()
            return render(request, 'treinamento.html', {'perfil': perfil, 'nada':nada, 'act':'active'})
        context = {
            "form": form,
            'act':'active',
        }
        return render(request, 'create_perfil.html', context)

def treinamento(request, perfil_id):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'act':'active'})
    else:
        all_face_encodings = {}

        user = str(request.user)
        perfil = get_object_or_404(Usuario, pk=perfil_id)
        fotourl = str(perfil.foto)
        ident = perfil.nome + '-' + user + '-' + str(perfil.id)
        #treinamento
        img2 = face_recognition.load_image_file(settings.MEDIA_ROOT + '/' + fotourl)
        all_face_encodings[ident] = face_recognition.face_encodings(img2)[0]
        
        with open(settings.MEDIA_ROOT + '/' + ident + '.dat', 'wb') as f:
            pickle.dump(all_face_encodings, f)
        # ......
        perfil.treina = read_file(settings.MEDIA_ROOT + '/' + ident + '.dat')
        
        perfil.save()
        apagatreina(settings.MEDIA_ROOT + '/')

        context = {
            'perfil': perfil,
            'user': user,
            'act':'active'
        }
        return render(request, 'detail.html', context) 

def aciona_procura(request, perfil_id):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'act':'active'})
    else:
        user = request.user
        perfil = get_object_or_404(Usuario, pk=perfil_id)
        notif_procur = True
        context = {
            'perfil': perfil,
            'user': user,
            'notif_procur': notif_procur,
            'act':'active'
        }
        return render(request, 'detail.html', context)

def procurado(request, perfil_id):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'act':'active'})
    else:
        user = request.user
        perfil = get_object_or_404(Usuario, pk=perfil_id)
        if perfil.proc:
            context = {
                'perfil': perfil,
                'user': user,
                'msgProc':"Perfil ja consta na lista de procurados",
            }
        else:
            procurado = Procurados(user=perfil,
                                   nome=perfil.nome,
                                   idade=perfil.idade,
                                   genre=perfil.genre,
                                   email=perfil.email,
                                   telefone=perfil.telefone,
                                   treina=perfil.treina)
            procurado.save()
            perfil.proc = True
            perfil.save()

            context = {
                'perfil': perfil,
                'user': user,
                'act':'active'
            }
        return render(request, 'detail.html', context)

def list_proc(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'act':'active'})
    else:
        proc_perf = Procurados.objects.all()
        context = {
            'proc_perf':proc_perf,
            'act':'active',
        }
        return render(request, 'list_proc.html', context)


def delete_perfil(request, perfil_id):
    perfil = Usuario.objects.get(pk=perfil_id)
    perfil.delete()
    perfils = Usuario.objects.filter(user=request.user)
    return render(request, 'perfis.html', {'perfils': perfils, 'act':'active'})


def detail(request, perfil_id):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'act':'active'})
    else:
        user = request.user
        perfil = get_object_or_404(Usuario, pk=perfil_id)
        return render(request, 'detail.html', {'perfil': perfil, 'user': user, 'act':'active'})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        'act':'active',
        "form": form,
    }
    return render(request, 'login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                perfil = user
                return render(request, 'index.html', {'perfil': perfil, 'act':'active'})
            else:
                return render(request, 'login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login', 'act':'active'})
    return render(request, 'login.html', {'act':'active',})


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                perfil = user
                return render(request, 'index.html', {'perfil': perfil, 'act':'active'})
    context = {
        "act":"active",
        "form": form,
    }
    return render(request, 'register.html', context)