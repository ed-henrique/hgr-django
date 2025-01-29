"""
URL configuration for hgr_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("autenticacao/", include("apps.autenticacao.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
    path("gestao/nacionalidades-etnias/",
         include("apps.nacionalidades_etnias.urls")),
    path("gestao/medidas-de-precaucao/",
         include("apps.medidas_de_precaucao.urls")),
    path("gestao/portas-de-entrada/", include("apps.portas_de_entrada.urls")),
    path("gestao/tipos-de-cirurgia/", include("apps.tipos_de_cirurgia.urls")),
    path("gestao/tipos-de-vacuo/", include("apps.tipos_de_vacuo.urls")),
    path("gestao/tipos-de-o2/", include("apps.tipos_de_o2.urls")),
    path("gestao/tipos-de-leito/", include("apps.tipos_de_leito.urls")),
    path("gestao/status-de-leito/", include("apps.status_de_leito.urls")),
    path("gestao/status-de-paciente/", include("apps.status_de_paciente.urls")),
    path("gestao/tipos-de-saida/", include("apps.tipos_de_saida.urls")),
    path("gestao/especialidades/", include("apps.especialidades.urls")),
    path("gestao/unidades-de-saude/", include("apps.unidades_de_saude.urls")),
    path("gestao/setores/", include("apps.setores.urls")),
    path("gestao/leitos/", include("apps.leitos.urls")),
    path("gestao/usuarios/", include("apps.usuarios.urls")),
    path("gestao/pacientes/", include("apps.pacientes.urls")),
    path("gestao/entradas/", include("apps.entradas.urls")),
    path("gestao/cirurgias/", include("apps.cirurgias.urls")),
    path("configuracoes/", include("apps.configuracoes.urls")),
]

urlpatterns += debug_toolbar_urls()
