from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _

from .models import Project


class ProjectsListView(ListView):
    
    queryset = Project.objects.all()
    context_object_name = 'projects'
    template_name = 'projects/projects_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Projects")
        return context
        


class ProjectDetailsView(DetailView):
    
    queryset = Project.objects.all()
    slug_field = 'slug' 
    slug_url_kwarg = 'slug' 
    
    template_name = 'projects/project_details.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Project") + f" {self.get_object().name}"
        return context

