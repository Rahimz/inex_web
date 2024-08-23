from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from projects.models import Project, Client

def HomeView(request):
    projects = Project.objects.all().select_related('client', 'category')

    clients = Client.objects.order_by('?')[:5]
    context = dict(
        page_title=_("Home"),
        projects=projects,
        clients=clients,
    )
    return render(
        request,
        'index.html',
        context
    )
