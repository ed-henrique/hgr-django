from django import template

register = template.Library()


@register.filter(name="is_active")
def is_active(user):
    """
    Custom filter to return if the user is active.
    Example: {{ user|is_active }}
    """
    if hasattr(user, "status_de_usuario"):
        if user.status_de_usuario.nome == "Ativo":
            return True
    return False


@register.filter(name="is_admin")
def is_admin(user):
    """
    Custom filter to return if the user is an admin.
    Example: {{ user|is_active }}
    """
    if hasattr(user, "tipo_de_usuario"):
        if user.tipo_de_usuario.nome == "Administrador":
            return True
    return False


@register.filter(name="is_superadmin")
def is_superadmin(user):
    """
    Custom filter to return if the user is an superadmin.
    Example: {{ user|is_active }}
    """
    if hasattr(user, "tipo_de_usuario"):
        if user.tipo_de_usuario.nome == "Super Administrador":
            return True
    return False


@register.filter(name="is_admin_or_higher")
def is_admin_or_higher(user):
    """
    Custom filter to return if the user is an admin or super admin.
    Example: {{ user|is_admin_or_higher }}
    """
    if hasattr(user, "tipo_de_usuario"):
        if user.tipo_de_usuario.nome in ["Administrador", "Super Administrador"]:
            return True
    return False


@register.filter(name="user_status")
def user_status(user):
    """
    Custom filter to return the user's status as a readable string.
    Example: {{ user|user_status }}
    """
    if hasattr(user, "status_de_usuario"):
        return user.status_de_usuario.nome
    return "Status not available"
