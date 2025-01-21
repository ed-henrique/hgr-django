from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('entrar/', views.CustomLoginView.as_view(authentication_form=views.UserLoginForm), name='entrar'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('esqueci-minha-senha/', auth_views.PasswordResetView.as_view(),
         name='esqueci_minha_senha'),
    path('esqueci-minha-senha/sucesso', auth_views.PasswordResetDoneView.as_view(),
         name='esqueci_minha_senha_sucesso'),
    path('alterar-senha/', auth_views.PasswordResetConfirmView.as_view(),
         name='alterar_senha'),
    path('alterar-senha/sucesso', auth_views.PasswordResetCompleteView.as_view(),
         name='alterar_senha_sucesso'),
    path('sair/', auth_views.LogoutView.as_view(), name='sair'),
]
