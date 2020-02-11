"""SiteFRec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('perfis/', views.perfis, name='perfis'),
    path('register/', views.register, name='register'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
	path('<int:perfil_id>/', views.detail, name='detail'),
    path('<int:perfil_id>/treinamento', views.treinamento, name='treinamento'),
    path('create_peril/', views.create_peril, name='create_peril'),
    path('<int:perfil_id>/delete_perfil/', views.delete_perfil, name='delete_perfil'),
    path('<int:perfil_id>/aciona_procura/', views.aciona_procura, name='aciona_procura'),
    path('<int:perfil_id>/procurado/', views.procurado, name='procurado'),
    path('list_proc/', views.list_proc, name='list_proc'),
    
    #path('admin/', admin.site.urls),
]
