from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def colors_view(request):
    return render(request, 'colors.html')