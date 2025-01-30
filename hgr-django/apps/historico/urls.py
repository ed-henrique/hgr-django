from django.urls import path
from . import views

urlpatterns = [
    path('', views.historico_view, name='historico'),
]
