from django.db import models
# from django.utils.text import slugify
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _
from tools.utils.make_thumbnail import make_thumbnail
from django.urls import reverse

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
        location = models.CharField(
            max_length=250,
            blank=True,
            null=True,
            verbose_name=_("Location")
        ),
        completed_date = models.CharField(
            _("Completed date"),
            null=True,
            blank=True
        )
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
    area = models.CharField(
        blank=True,
        null=True,
        verbose_name=_("Area")
    )
    
    
    
    cover_image = models.ImageField(
        upload_to='products/'        
    )
    thumbnail = models.ImageField(
        upload_to='products/thumbnails/',
        null=True,
        blank=True
    )
    rank = models.PositiveSmallIntegerField(
        _("Rank"),
        default=1
    )
    
    class Meta:
        ordering = ('rank',)
    
    def get_absolute_url(self):
        # We use 'self.slug' which will be the slug from the current active language
        # thanks to django-parler's magic.
        return reverse('projects:project_details', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # make thumbnail from file
        try:
            if self.cover_image and not self.thumbnail:
                self.thumbnail = make_thumbnail(self.cover_image.file, size=(500,500))
        except Exception as e:
            print(f"Error generating thumbnail: {e}")
            
        return super().save(*args, **kwargs)


class Image(models.Model):
    project = models.ForeignKey(
        Project,
        related_name='images',
        on_delete=models.CASCADE,
    )
    file = models.ImageField(
        upload_to='projects/images/'
    )
    thumbnail = models.ImageField(
        upload_to='products/images/thumbnails/',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"image {self.id}"
    
    
    def save(self, *args, **kwargs):
        # make thumbnail from file
        try:
            if self.file and not self.thumbnail:
                self.thumbnail = make_thumbnail(self.file.file, size=(500,500))
        except Exception as e:
            print(f"Error generating thumbnail: {e}")
            
        return super().save(*args, **kwargs)
    