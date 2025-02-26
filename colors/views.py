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

            # Update color fields
            colors.very_happy = data.get("very_happy", colors.very_happy)
            colors.very_relaxed = data.get("very_relaxed", colors.very_relaxed)
            colors.relaxed = data.get("relaxed", colors.relaxed)
            colors.neutral = data.get("neutral", colors.neutral)
            colors.sad = data.get("sad", colors.sad)
            colors.very_sad = data.get("very_sad", colors.very_sad)
            colors.is_breathing = data.get("is_breathing", colors.is_breathing)

            # Update threshold fields
            colors.very_happy_threshold = int(
                data.get("very_happy_threshold", colors.very_happy_threshold)
            )
            colors.very_relaxed_threshold = int(
                data.get("very_relaxed_threshold", colors.very_relaxed_threshold)
            )
            colors.relaxed_threshold = int(
                data.get("relaxed_threshold", colors.relaxed_threshold)
            )
            colors.neutral_threshold = int(
                data.get("neutral_threshold", colors.neutral_threshold)
            )
            colors.sad_threshold = int(data.get("sad_threshold", colors.sad_threshold))
            colors.very_sad_threshold = int(
                data.get("very_sad_threshold", colors.very_sad_threshold)
            )

            # Save changes to the database
            colors.save()

            return JsonResponse(
                {"status": "success", "message": "Colors and SDNN thresholds saved!"}
            )

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=405
    )


@csrf_exempt
def get_colors(request):
    """
    Returns saved colors, SDNN thresholds, and breathing state.
    """
    try:
        colors = EmotionColor.objects.first()
        if colors:
            return JsonResponse(
                colors.to_dict()
            )  # Uses the `to_dict()` method from your model
        else:
            return JsonResponse(
                {
                    "very_happy": "#FFD700",
                    "very_relaxed": "#FFFF00",
                    "relaxed": "#FFFF00",
                    "neutral": "#C0C0C0",
                    "sad": "#87CEEB",
                    "very_sad": "#1E90FF",
                    "is_breathing": False,
                    "very_happy_threshold": 70,
                    "very_relaxed_threshold": 60,
                    "relaxed_threshold": 50,
                    "neutral_threshold": 40,
                    "sad_threshold": 30,
                    "very_sad_threshold": 20,
                }
            )
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

            return JsonResponse(
                {
                    "status": "success",
                    "is_breathing": colors.is_breathing,
                    "message": "Breathing mode updated!",
                }
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=405
    )
