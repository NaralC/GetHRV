from django.urls import path
from .views import save_colors, get_colors, toggle_breathing

urlpatterns = [
    path("save-colors", save_colors),
    path("get-colors", get_colors),
    path("toggle-breathing", toggle_breathing),
]
