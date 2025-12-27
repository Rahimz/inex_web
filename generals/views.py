from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from projects.models import Project, Client

def HomeView(request):
    projects = Project.objects.all().select_related('client', 'category').order_by('?')

    clients = Client.objects.order_by('?')[:5]
    context = dict(
        page_title=_("Home"),
        projects=projects,
        clients=clients,
        projects_header_text=_("Our Featured Projects")
    )
    return render(
        request,
        'index.html',
        context
    )




def handler404(request, exception):
    """
    Custom 404 page view.
    """
    response = render(request, "404.html")
    response.status_code = 404
    return response

def handler500(request):
    """
    Custom 500 page view.
    """
    response = render(request, "500.html")
    response.status_code = 500
    return response