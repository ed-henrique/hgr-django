from django.urls import path
from . import views

urlpatterns = [
    path('', views.especialidades_view, name='especialidades'),
]
