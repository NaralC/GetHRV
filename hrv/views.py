from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from collections import deque
from django.template import loader

from colors.models import EmotionColor
from .data_processing import enqueue, hrv_generator, get_ppg
from .models import Measures
from django.forms.models import model_to_dict
from heartpy.exceptions import BadSignalWarning
from django.utils.timezone import now

ppg_data = deque()
ppg = []
measures = {}
num = 0

# Create your views here.


def index(request):
    # global ppg, ppg_data, measures
    # sampling_rate, ppg, ppg_data = get_ppg(100, ppg_data)
    # working_data, measures = hrv_generator(measures, ppg, sampling_rate)
    return HttpResponse("hello HRV")


# 接口函数


import json
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Measures
from django.db.utils import IntegrityError


def post(request):
    global ppg_data, ppg, sampling_rate, measures_instance
    global measures
    global num

    bad_signal = False

    try:
        if request.method == "POST":
            num += 1
            data = json.loads(request.body)

            android_id = data.get("android_id", None)
            if android_id is not None:
                measures_instance = Measures()
                measures_instance.android_id = android_id
                measures_instance.timeStamp = data["time"]

                if num >= 1 and len(data):
                    ppg_data = enqueue(ppg_data, data)  # Add new data to the buffer
                    if len(ppg_data) >= 60:  # Ensure buffer is sufficient
                        sampling_rate, ppg, ppg_data = get_ppg(ppg_data, 60)
                        try:
                            working_data, measures = hrv_generator(
                                measures, ppg, sampling_rate
                            )
                        except BadSignalWarning as e:
                            print("Bad signal warning:", e)
                            print("Skipping this segment of data.")
                            bad_signal = True

                        if "sdnn" in measures and measures["sdnn"]:
                            print("Current SDNN: ", measures["sdnn"])
                    else:
                        print(
                            f"Insufficient buffer size for HRV processing, currently at {len(ppg_data)}. Waiting for more data..."
                        )

                    if len(measures):
                        for key, value in measures.items():
                            setattr(
                                measures_instance,
                                key,
                                value if value is not None else -1,
                            )

                    for field in Measures._meta.fields:
                        if (
                            field.name != "id"
                            and getattr(measures_instance, field.name) is None
                        ):
                            setattr(measures_instance, field.name, -1)

                    if bad_signal:
                        measures_instance.sdnn = -500

                    print("Saving SDNN:", measures_instance.sdnn)
                    measures_instance.save()

    except Exception as e:
        print("❌ An error occurred:", str(e))

        # Ensure an instance is saved with SDNN = -500 on failure
        try:
            error_instance = Measures(
                android_id=android_id if "android_id" in locals() else "unknown",
                timeStamp=(
                    data["time"] if "data" in locals() and "time" in data else None
                ),
                sdnn=-500,  # Mark error condition
            )
            error_instance.save()
            print("⚠ Error recorded with SDNN = -500")
        except IntegrityError as db_error:
            print("⚠ Failed to save error instance:", db_error)

    template = loader.get_template("measures.html")
    context = {"measures": measures}
    return HttpResponse(template.render(context, request))


def my_api_endpoint(request):
    """
    Returns the color associated with the latest SDNN value.
    Uses user-customized colors and thresholds if available, otherwise defaults.
    """

    # Check if the breathing tutorial is active
    emotion_color = EmotionColor.objects.last()
    is_breathing = emotion_color.is_breathing if emotion_color else False

    if is_breathing:
        return JsonResponse({"color": "is_breathing"}, status=200)

    # Retrieve the latest measure entry
    measure = Measures.objects.order_by("timeStamp").last()

    # If no measure data found — HRV is still being processed
    if not measure or "sdnn" not in model_to_dict(measure):
        return JsonResponse({"color": "loading"}, status=200)

    print(f"Latest TimeStamp: {measure.timeStamp}")

    # Check if the latest timeStamp is recent
    if not is_recent(measure.timeStamp):
        return JsonResponse({"color": "loading"}, status=200)

    # If the data contains a bad signal
    sdnn_value = model_to_dict(measure)["sdnn"]
    if sdnn_value == -500:
        return JsonResponse({"color": "bad_signal"}, status=200)

    # Fetch user-customized colors and SDNN thresholds
    emotion_data = get_user_colors()

    # Extract thresholds
    thresholds = {
        "very_happy": emotion_data["very_happy_threshold"],
        "very_relaxed": emotion_data["very_relaxed_threshold"],
        "relaxed": emotion_data["relaxed_threshold"],
        "neutral": emotion_data["neutral_threshold"],
        "sad": emotion_data["sad_threshold"],
        "very_sad": emotion_data["very_sad_threshold"],
    }
    print(thresholds)

    # Determine the color based on SDNN value
    if sdnn_value >= thresholds["very_happy"]:
        mapped_color = "#FF69B4"  # Fixed Rainbow for Very Happy
    elif sdnn_value >= thresholds["very_relaxed"]:
        mapped_color = emotion_data["very_relaxed"]
    elif sdnn_value >= thresholds["relaxed"]:
        mapped_color = emotion_data["relaxed"]
    elif sdnn_value >= thresholds["neutral"]:
        mapped_color = emotion_data["neutral"]
    elif sdnn_value >= thresholds["sad"]:
        mapped_color = emotion_data["sad"]
    else:
        mapped_color = emotion_data["very_sad"]

    return JsonResponse({"color": mapped_color})


def is_recent(timestamp):
    """
    Checks if a timestamp is recent within a given threshold.

    Args:
        timestamp (datetime): The timestamp to check.

    Returns:
        bool: True if recent, False otherwise.
    """
    # Get current time
    current_time = now()

    # Calculate the time difference
    time_difference = (current_time - timestamp).total_seconds()

    return time_difference <= 90  # 90 seconds


def map_sdnn_to_color(sdnn: float, emotion_colors) -> str:
    """
    Maps an SDNN value to a predefined color based on arbitrary ranges.

    Args:
        sdnn (float): The SDNN value to map.

    Returns:
        str: The hex color code corresponding to the SDNN value.
    """

    # Map sdnn to a color based on ranges (arbitrary example ranges)
    if sdnn <= 0:
        return "loading"  # Pulsing gray for no data
    elif sdnn < 20:
        return emotion_colors["very_sad"]
    elif 20 <= sdnn < 30:
        return emotion_colors["sad"]
    elif 30 <= sdnn < 40:
        return emotion_colors["neutral"]
    elif 40 <= sdnn < 50:
        return emotion_colors["happy"]
    elif 50 <= sdnn < 70:
        return emotion_colors["very_happy"]
    else:
        return "#FF69B4"  # Hot-pink stand-in for rainbow


def get_user_colors() -> dict:
    """
    Retrieves user-customized emotion colors and SDNN thresholds from the database, or defaults.

    Returns:
        dict: A dictionary mapping emotions to their respective colors and thresholds.
    """
    colors = EmotionColor.objects.first()  # Get the first saved color settings

    if colors:
        return {
            "very_happy": colors.very_happy,
            "very_relaxed": colors.very_relaxed,
            "relaxed": colors.relaxed,
            "neutral": colors.neutral,
            "sad": colors.sad,
            "very_sad": colors.very_sad,
            "is_breathing": colors.is_breathing,
            "very_happy_threshold": colors.very_happy_threshold,
            "very_relaxed_threshold": colors.very_relaxed_threshold,
            "relaxed_threshold": colors.relaxed_threshold,
            "neutral_threshold": colors.neutral_threshold,
            "sad_threshold": colors.sad_threshold,
            "very_sad_threshold": colors.very_sad_threshold,
        }
    else:
        # Default colors and thresholds if none exist in the database
        return {
            "very_happy": "#FF69B4",  # Fixed Rainbow for Very Happy 🌈
            "very_relaxed": "#FFD700",  # Gold
            "relaxed": "#FFFF00",  # Yellow
            "neutral": "#C0C0C0",  # Gray
            "sad": "#87CEEB",  # Light Blue
            "very_sad": "#1E90FF",  # Blue
            "is_breathing": False,
            "very_happy_threshold": 70,
            "very_relaxed_threshold": 60,
            "relaxed_threshold": 50,
            "neutral_threshold": 40,
            "sad_threshold": 30,
            "very_sad_threshold": 20,
        }


# Add a new view to retrieve data for a specific watch using its Android ID
def get_watch_data(request, android_id):
    try:
        # Assuming you have a field named "android_id" in your Measures model
        watch_data = (
            Measures.objects.filter(android_id=android_id).order_by("timeStamp").last()
        )
        measure_dict = model_to_dict(watch_data)
        return JsonResponse(measure_dict, safe=False)
    except Measures.DoesNotExist:
        return JsonResponse(
            {"error": "Watch data not found for the given Android ID."}, status=404
        )


def get_sdnn_only(request):
    """
    Only returns the SDNN value for the latest measure entry.
    """
    # Retrieve the latest measure entry
    measure = Measures.objects.order_by("timeStamp").last()

    # If data not found — it's still working out the HRV
    if not measure or "sdnn" not in model_to_dict(measure):
        return JsonResponse({"sdnn": "loading"})

    print(f"Latest TimeStamp: {measure.timeStamp}")

    # Check if the latest timeStamp is recent
    if not is_recent(measure.timeStamp):
        return JsonResponse({"sdnn": "loading"}, status=200)

    # If the data contains bad signal
    if model_to_dict(measure)["sdnn"] == -500:
        return JsonResponse({"sdnn": "bad_signal"}, status=200)

    return JsonResponse({"sdnn": measure.sdnn})
