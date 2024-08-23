from django.urls import path
from . import views 

app_name = 'generals'

urlpatterns = [
    path('', views.HomeView, name="home"),
]
