from django.shortcuts import redirect
from django.urls import reverse, resolve

class AuthRedirectMiddleware:
    """
    Middleware to handle unauthenticated and authenticated user redirects.
    - Redirects unauthenticated users to '/entrar' unless accessing public routes or admin.
    - Redirects authenticated users to '/dashboard' on 404 pages.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define paths or view names accessible without authentication
        public_paths = [
            reverse('entrar'),
            reverse('cadastro'),
            reverse('esqueci_minha_senha'),
            reverse('esqueci_minha_senha_sucesso'),
            reverse('alterar_senha'),
            reverse('alterar_senha_sucesso'),
        ]
        admin_paths = ['/admin/', '/admin/login/']

        # Handle unauthenticated users
        if not request.user.is_authenticated:
            if not any(request.path.startswith(path) for path in public_paths + admin_paths):
                return redirect(reverse('entrar'))

        # Process the response
        response = self.get_response(request)

        # Redirect authenticated users to '/dashboard' on 404 pages
        if request.user.is_authenticated and response.status_code == 404:
            return redirect(reverse('dashboard'))

        return response
