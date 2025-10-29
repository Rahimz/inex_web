from projects.models import Project


def projects_context(request):
    language = request.LANGUAGE_CODE
    
    projects = Project.objects.filter(
        translations__language_code=language
        ).values('translations__name', 'slug')  # Assuming you have a Project model
    return {
        'projects_context': projects,
    }