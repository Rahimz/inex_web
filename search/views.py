from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from projects.models import Project

def SearchView(request):
    query = request.GET.get('q', '').strip()
    normal_query = query.lower()
    
    if not query:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    projects = Project.objects.filter(
        Q(name__icontains=query) |         
        Q(name__icontains=normal_query) |         
        Q(category__name__icontains=query) |  # Assuming category has a 'name' field
        Q(category__name__icontains=normal_query) |  # Assuming category has a 'name' field
        Q(place__icontains=query) | 
        Q(place__icontains=normal_query) | 
        Q(details__icontains=query) |
        Q(details__icontains=normal_query)
    )
    
    context = dict(
        page_title = _("Search results"),
        projects=projects,
        query=query,
    )
    
    return render(
        request,
        'search/search.html',
        context
    )
    
    