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


def post(request):
    global ppg_data, ppg, sampling_rate, measures_instance
    global measures
    global num

    # print("Check if the request method is POST")
    if request.method == "POST":  # 当提交表单时
        # 判断是否传参
        num += 1
        #  print(num)
        data = json.loads(request.body)
        # print(data["total_event"])

        android_id = data.get("android_id", None)
        # print(f"Received Android ID: {android_id}")
        if android_id is not None:
            #  print("Valid Android ID received: ", android_id)
            #  print("Received data: ", data)

            measures_instance = Measures()
            measures_instance.android_id = android_id
            # if 'timeStamp' in data:
            measures_instance.timeStamp = data["time"]
            if num >= 1 and len(data):
                ppg_data = enqueue(ppg_data, data)  # Add new data to the buffer
                if len(ppg_data) >= 60:  # Ensure buffer is sufficient
                    sampling_rate, ppg, ppg_data = get_ppg(ppg_data, 60)
                    #  working_data, measures = hrv_generator(measures, ppg, sampling_rate)
                    try:
                        working_data, measures = hrv_generator(
                            measures, ppg, sampling_rate
                        )
                    except BadSignalWarning as e:
                        print("Bad signal warning:", e)
                        print("Skipping this segment of data.")

                    if (
                        "sdnn" in measures and measures["sdnn"]
                    ):  # Check if 'sdnn' exists
                        print("Current SDNN: ", measures["sdnn"])
                #  else:
                #      print("SDNN not available yet, waiting for more data...")
                else:
                    print(
                        f"Insufficient buffer size for HRV processing, currently at {len(ppg_data)}. Waiting for more data..."
                    )

                # 将processed data 存入数据库 （这一步之前在models.py 中创建class）

                if len(measures):
                    # is not empty,saving the data to the database using the 'Measures' model.

                    for key, value in measures.items():
                        if value is None:
                            value = -1
                        setattr(measures_instance, key, value)

                for field in Measures._meta.fields:
                    if (
                        field.name != "id"
                        and getattr(measures_instance, field.name) is None
                    ):
                        setattr(measures_instance, field.name, -1)

                #  print(f"{field.name}: {getattr(measures_instance, field.name)}")

                measures_instance.save()

    # return render(request, "measures.html", {"measures": measures})
    template = loader.get_template("measures.html")
    context = {"measures": measures}
    return HttpResponse(template.render(context, request))


def my_api_endpoint(request):
    """
    Returns the color associated with the latest SDNN value.
    Uses user-customized colors if available, otherwise defaults.
    """
    # Retrieve the latest measure entry
    measure = Measures.objects.order_by("timeStamp").last()

    if not measure or "sdnn" not in model_to_dict(measure):
        return JsonResponse({"error": "No valid SDNN data found"}, status=400)
    
    # Fetch the user's saved colors (or default colors)
    emotion_colors = get_user_colors()

    # Get the SDNN value and map it to the correct color
    sdnn_value = model_to_dict(measure)["sdnn"]
    print(sdnn_value)
    mapped_color = map_sdnn_to_color(sdnn_value, emotion_colors)

    return JsonResponse({"color": mapped_color})


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
        return "#616161" # Pulsing gray for no data
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
        return "#FF69B4" # Hot-pink stand-in for rainbow


def get_user_colors() -> dict:
    """
    Retrieves user-customized emotion colors from the database or defaults.

    Returns:
        dict: A dictionary mapping emotions to their respective colors.
    """
    colors = EmotionColor.objects.first()  # Get the first saved color settings

    if colors:
        return {
            "very_happy": colors.very_happy,
            "happy": colors.happy,
            "neutral": colors.neutral,
            "sad": colors.sad,
            "very_sad": colors.very_sad,
        }
    else:
        # Default colors if none exist in the database
        return {
            "very_happy": "#FFD700",  # Gold
            "happy": "#FFFF00",  # Yellow
            "neutral": "#C0C0C0",  # Gray
            "sad": "#87CEEB",  # Light Blue
            "very_sad": "#1E90FF",  # Blue
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
