from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Project, Category, Client, Image

class ImageInline(admin.StackedInline):
    model = Image
    raw_field_id = 'project'
    extra = 3


@admin.register(Project)
class ProjectAdmin(TranslatableAdmin):
    list_display = ['name', 'category', 'client', ]
    
    inlines = [ImageInline]
    # NOTE: I do not want to translate slug automatically
    # def get_prepopulated_fields(self, request, obj=None):
    #     # can't use `prepopulated_fields = ..` because it breaks the admin validation
    #     # for translated fields. This is the official django-parler workaround.
    #     return { 'slug': ('name',) }
    # prepopulated_fields = {'slug': ('name',)}

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name']
    
    # def get_prepopulated_fields(self, request, obj=None):
    #     return { 'slug': ('name',) }
    # prepopulated_fields = {'slug': ('name',)}

@admin.register(Client)
class ClientAdmin(TranslatableAdmin):
    list_display = ['name']
    
    # def get_prepopulated_fields(self, request, obj=None):
    #     return { 'slug': ('name',) }
    # prepopulated_fields = {'slug': ('name',)}

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['project']
    