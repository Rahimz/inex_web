from projects.models import Category


def categories_context(request):
    language = request.LANGUAGE_CODE
    
    categories = Category.objects.filter(
        translations__language_code=language
        ).values('translations__name', 'slug')  # Assuming you have a Project model
    return {
        'categories_context': categories,
    }