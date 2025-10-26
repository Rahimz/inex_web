from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Project


class ProjectsListView(ListView):
    
    queryset = Project.objects.all()
    context_object_name = 'projects'
    template_name = 'projects/projects_list.html'


class ProjectDetailsView(DetailView):
    
    queryset = Project.objects.all()
    slug_field = 'slug' 
    slug_url_kwarg = 'slug' 
    
    template_name = 'projects/project_details.html'
    

