from django import forms
from django.contrib.auth.models import User

from .models import Usuario, Procurados


class PerfilForm(forms.ModelForm):
    nome = forms.CharField(max_length=250, 
                           widget=forms.TextInput(attrs={'class':'form-control',
                                                             'placeholder':'Nome do Perfil'}))
    idade = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control',
                                                              'placeholder':'Idade'}))
    genre = forms.CharField(max_length=10, 
                             widget=forms.TextInput(attrs={'class':'form-control',
                                                             'placeholder':'Genero'}))
    email = forms.EmailField(max_length=100, 
                              widget=forms.EmailInput(attrs={'class':'form-control',
                                                             'placeholder':'Email de Contato'}))
    telefone = forms.CharField(max_length=50, 
                                widget=forms.TextInput(attrs={'class':'form-control',
                                                             'placeholder':'Telefone de Contato'}))
    foto = forms.FileField(widget=forms.ClearableFileInput(attrs={'style':'position:absolute;z-index:2;top:0;left:0;filter: alpha(opacity=0);-ms-filter:"progid:DXImageTransform.Microsoft.Alpha(Opacity=0)";opacity:0;background-color:transparent;color:transparent;',
                                                                  'onchange':'$("#upload-file-info").html($(this).val());'}))

    class Meta:
        model = Usuario
        fields = ['nome', 'idade', 'genre', 'email', 'telefone', 'foto']

class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, 
                               widget=forms.TextInput(attrs={'class':'form-control',
                                                             'placeholder':'Nome de Usuario'}))
    email = forms.CharField(max_length=100, 
                               widget=forms.EmailInput(attrs={'class':'form-control',
                                                             'placeholder':'Email'}))
    password = forms.CharField(max_length=100, 
                               widget=forms.PasswordInput(attrs={'class':'form-control',
                                                             'placeholder':'Senha'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
