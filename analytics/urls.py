from django.urls import path
from . import views


app_name = 'analytics'

urlpatterns = [
    path('base/<str:base>/filter/<str:filter>/date/<str:date>/device/<str:device>/', views.AnalyticsHomeView, name='analytics_home_filter'),
    path('', views.AnalyticsHomeView, name='analytics_home'),
]
