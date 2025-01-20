from django.contrib.auth.decorators import login_required


@login_required
def dashboard_view(request):
    pass
