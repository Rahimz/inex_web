from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import translation
from django.conf import settings
from .models import Project

class StaticViewSitemap(Sitemap):
    """
    Sitemap for static pages like home, about, contact.
    """
    priority = 0.8
    changefreq = 'weekly'
    # This tells the sitemap framework to generate alternate language URLs for these pages
    i18n = True 

    def items(self):
        # Return a list of URL names for your static pages
        return ['generals:home',] # Make sure these URL names exist in your project's urls.py

    def location(self, item):
        return reverse(item)

class ProjectSitemap(Sitemap):
    """
    Sitemap for the Project model, with support for multiple languages.
    """
    changefreq = "monthly"
    priority = 0.9
    # Enable i18n support
    i18n = True

    def items(self):
        # Return all published Project objects
        return Project.objects.all()

    def lastmod(self, obj):
        # Optional: If you have a 'updated_at' field in your Project model
        # return obj.updated_at
        return None # Return None if you don't have it

    def get_alternates(self, item):
        """
        This is the key for multilingual SEO. It generates the <xhtml:link> tags
        in the sitemap.xml file.
        """
        alternates = []
        # Loop through all supported languages
        for lang_code, _ in settings.LANGUAGES:
            # Activate the language to get the correct slug
            with translation.override(lang_code):
                try:
                    # Get the translated URL for the item
                    location = item.get_absolute_url()
                    alternates.append({'location': location, 'lang_code': lang_code})
                except Exception:
                    # If a translation for a specific language doesn't exist, skip it
                    continue
        return alternates
