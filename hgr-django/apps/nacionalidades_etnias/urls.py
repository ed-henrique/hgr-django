from django.urls import path
from . import views

urlpatterns = [
    path('', views.nacionalidades_etnias_view, name='nacionalidades_etnias'),
]
