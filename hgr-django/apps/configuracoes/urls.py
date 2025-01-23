from django.urls import path
from . import views

urlpatterns = [
    path('', views.configuracoes_view, name='configuracoes'),
    path('mudar_nome', views.mudar_nome_view, name='mudar_nome'),
    path('mudar_nome_de_usuario',
         views.mudar_nome_de_usuario_view, name='mudar_nome_de_usuario'),
    path('mudar_email', views.mudar_email_view, name='mudar_email'),
    path('mudar_senha', views.mudar_senha_view, name='mudar_senha'),
]
