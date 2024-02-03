from django.urls import path
from apps.services.api.api import services_api_view

urlpatterns = [
    path('services/', services_api_view, name = 'services_api')
]
