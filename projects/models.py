from django.db import models
from django.utils.text import slugify
from parler.models import TranslatableModel, TranslatedFields

# docs at https://django-parler.readthedocs.io/en/latest/compatibility.html
# ordering with translated fields
# MyModel.objects.translated('en').order_by('translations__title')

class Category(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(
            max_length=150,
            unique=True
        ),
    )
    slug = models.SlugField(
        allow_unicode=True
    )
    def __str__(self):
        #     return self.name
        return self.safe_translation_getter('name', str(self.id))
    
class  Client(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(
            max_length=150,
            unique=True
        ),
        subtitle = models.CharField(
            max_length=150,
            null=True,
            blank=True
        ),
    )
    slug = models.SlugField(
            allow_unicode=True
        )
    logo = models.ImageField(
        upload_to='clients/'
    )

    def __str__(self):
        # return self.name
        # Return the name of the category in the active language
        return self.safe_translation_getter('name', str(self.id))
    
    
class Project(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(
            max_length=150,
            unique=True
        ),
        place = models.CharField(
            max_length=150,
            null=True,
            blank=True,
        ),
        details = models.TextField(
            blank=True
        ),
    )
    slug = models.SlugField(
        allow_unicode=True
    )
    category = models.ForeignKey(
        Category,
        related_name='projects',
        on_delete=models.PROTECT,
    )
    client = models.ForeignKey(
        Client,
        related_name='projects',
        on_delete=models.PROTECT
    )
    
    cover_image = models.ImageField(
        upload_to='products/'        
    )
    
    def __str__(self):
        return self.name
    


class Image(models.Model):
    project = models.ForeignKey(
        Project,
        related_name='images',
        on_delete=models.CASCADE,
    )
    file = models.ImageField(
        upload_to='projects/images/'
    )

    def __str__(self):
        return f"image {self.id}"
    