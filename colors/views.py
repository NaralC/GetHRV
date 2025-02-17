from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import EmotionColor
import json


def colors_view(request):
    return render(request, "colors.html")


@csrf_exempt
def save_colors(request):
    if request.method == "POST":
        try:
            # Parse JSON data from the request
            data = json.loads(request.body)

            # Get the first instance or create a new one
            colors, _ = EmotionColor.objects.get_or_create(id=1)

            # Update the colors
            colors.very_happy = data.get("very_happy", colors.very_happy)
            colors.happy = data.get("happy", colors.happy)
            colors.neutral = data.get("neutral", colors.neutral)
            colors.sad = data.get("sad", colors.sad)
            colors.very_sad = data.get("very_sad", colors.very_sad)
            colors.is_breathing = data.get("is_breathing", colors.is_breathing)
            colors.save()

            return JsonResponse({"status": "success", "message": "Colors saved!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=405
    )


@csrf_exempt
def get_colors(request):
    """
    Returns saved colors and breathing state.
    """
    try:
        colors = EmotionColor.objects.first()
        if colors:
            return JsonResponse(colors.to_dict())
        else:
            return JsonResponse({
                "very_happy": "#FFD700",
                "happy": "#FFFF00",
                "neutral": "#C0C0C0",
                "sad": "#87CEEB",
                "very_sad": "#1E90FF",
                "is_breathing": False,
            })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


@csrf_exempt
def toggle_breathing(request):
    """
    Toggles the `is_breathing` state in the database.
    """
    if request.method == "POST":
        try:
            colors, _ = EmotionColor.objects.get_or_create(id=1)
            colors.is_breathing = not colors.is_breathing  # Toggle state
            colors.save()

            return JsonResponse({
                "status": "success",
                "is_breathing": colors.is_breathing,
                "message": "Breathing mode updated!"
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=405
    )
