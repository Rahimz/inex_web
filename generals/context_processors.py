from projects.models import Project


def projects_context(request):
    projects = Project.objects.values('name', 'slug')  # Assuming you have a Project model
    return {
        'projects_context': projects,
    }