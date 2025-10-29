from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from projects.models import Project

def SearchView(request):
    query = request.GET.get('q', '').strip()
    normal_query = query.lower()
    
    if not query:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    language = request.LANGUAGE_CODE
    projects = Project.objects.filter(
        translations__language_code=language
        ).filter(
        Q(translations__name__icontains=query) |         
        Q(translations__name__icontains=normal_query) |         
        Q(category__translations__name__icontains=query) |  # Assuming category has a 'name' field
        Q(category__translations__name__icontains=normal_query) |  # Assuming category has a 'name' field
        Q(translations__place__icontains=query) | 
        Q(translations__place__icontains=normal_query) | 
        Q(translations__details__icontains=query) |
        Q(translations__details__icontains=normal_query)
    ).distinct()
    
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
    
    