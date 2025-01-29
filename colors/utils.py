from django.http import JsonResponse
from colors.models import EmotionColor


def map_sdnn_to_color(sdnn: float) -> str:
    """
    Maps an SDNN value to a predefined color based on arbitrary ranges.

    Args:
        sdnn (float): The SDNN value to map.

    Returns:
        str: The hex color code corresponding to the SDNN value.
    """
    # Define the ranges and their associated colors
    emotion_colors = {
        "very_happy": "#FFD700",  # Gold
        "happy": "#FFFF00",  # Yellow
        "neutral": "#C0C0C0",  # Gray
        "sad": "#87CEEB",  # Light Blue
        "very_sad": "#1E90FF",  # Blue
    }

    # Map sdnn to a color based on ranges (arbitrary example ranges)
    if sdnn < 20:
        return emotion_colors["very_sad"]
    elif 20 <= sdnn < 40:
        return emotion_colors["sad"]
    elif 40 <= sdnn < 60:
        return emotion_colors["neutral"]
    elif 60 <= sdnn < 80:
        return emotion_colors["happy"]
    else:
        return emotion_colors["very_happy"]



def get_colors(request):
    """
    API endpoint to fetch custom emotion colors.
    """
    # Fetch the first row or create it with defaults
    emotion_colors, _ = EmotionColor.objects.get_or_create(id=1)

    # Return the colors as a JSON response
    return JsonResponse(emotion_colors.to_dict())