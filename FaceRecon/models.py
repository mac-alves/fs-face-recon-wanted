from django.contrib.auth.models import Permission, User
from django.db import models
#from django.urls import reverse


class Usuario(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=1)
    nome = models.CharField(max_length=250)
    idade = models.IntegerField()
    genre = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    telefone = models.CharField(max_length=50)    
    foto = models.FileField()
    treina = models.BinaryField(max_length=None, default=False)
    proc = models.BooleanField(default=False)

    def __str__(self):
        return self.nome + ' - ' + self.email


class Procurados(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nome = models.CharField(max_length=250)
    idade = models.IntegerField()
    genre = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    telefone = models.CharField(max_length=50)
    treina = models.BinaryField(max_length=None, default=False)

    def __str__(self):
        return self.nome