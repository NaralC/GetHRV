from django.urls import path
from . import views

urlpatterns = [
    path('', views.post, name='index'),
    path('api/endpoint/', views.my_api_endpoint, name='my_api_endpoint'),
    path('api/sdnn-only/', views.get_sdnn_only, name='sdnn_only'),
    path('measures/', views.Measures, name='Measures'),
]
