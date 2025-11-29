from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('categories/<str:category_slug>/', views.ProjectsListView.as_view(), name="projects_list_category"),
    path('<slug:slug>/', views.ProjectDetailsView.as_view(), name="project_details"),
    path('', views.ProjectsListView.as_view(), name="projects_list"),
]
