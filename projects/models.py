from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True
    )
    slug = models.SlugField(
        allow_unicode=True
    )
    def __str__(self):
        return self.name
    
class  Client(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True
    )    
    slug = models.SlugField(
        allow_unicode=True
    )
    subtitle = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )    
    logo = models.ImageField(
        upload_to='clients/'
    )

    def __str__(self):
        return self.name
    
    
class Project(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True
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
    place = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )
    details = models.TextField(
        blank=True
    )
    cover_image = models.ImageField(
        upload_to='products/'        
    )


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
    