from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_setores_view, name='dashboard_setores'),
]
