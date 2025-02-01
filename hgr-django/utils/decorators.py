from django.contrib.auth.decorators import user_passes_test


def is_admin(user):
    return user.is_authenticated and user.tipo_de_usuario.nome == "Administrador"


is_admin_required = user_passes_test(
    is_admin, login_url='/autenticacao/entrar/')


def is_superadmin(user):
    return user.is_authenticated and user.tipo_de_usuario.nome == "Super Administrador"


is_superadmin_required = user_passes_test(
    is_superadmin, login_url='/autenticacao/entrar/')


def is_admin_or_higher(user):
    print(user.tipo_de_usuario.nome)
    return user.is_authenticated and (user.tipo_de_usuario.nome == "Super Administrador" or user.tipo_de_usuario.nome == "Administrador")


is_admin_or_higher_required = user_passes_test(
    is_admin_or_higher, login_url='/autenticacao/entrar/')
