from django.urls import path
from .views import save_colors, get_colors

urlpatterns = [
    path("save-colors", save_colors),
    path("get-colors", get_colors),
]
