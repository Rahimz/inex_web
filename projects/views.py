from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _

from .models import Project, Category


class ProjectsListView(ListView):
    
    queryset = Project.objects.all()
    context_object_name = 'projects'
    template_name = 'projects/projects_list.html'
    
    def get_queryset(self):
        queryset =  super().get_queryset()
        category_slug = self.kwargs.get('category_slug', '')
        if category_slug:
            try:
                category = Category.objects.get(slug=category_slug)
                queryset = queryset.filter(category=category)
            except:
                pass
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Projects")
        context["category"] = self.kwargs.get('category_slug', '')
        context["categories"] = Category.objects.all()
        return context
        


class ProjectDetailsView(DetailView):
    
    queryset = Project.objects.all()
    slug_field = 'slug' 
    slug_url_kwarg = 'slug' 
    
    # template_name = 'projects/project_details.html'
    template_name = 'projects/project_details_new.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Project") + f" {self.get_object().name}"
        return context

