import json
import logging
from .models import CarMake, CarModel
from .populate import initiate
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    data = json.loads(request.body.decode("utf-8"))

    username = data.get("userName")
    password = data.get("password")
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    email = data.get("email")

    if User.objects.filter(username=username).exists():
        return JsonResponse({
            "userName": username,
            "error": "Already Registered"
        })

    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email
    )

    login(request, user)

    return JsonResponse({
        "userName": username,
        "status": "Authenticated"
    })
def get_cars(request):
    count = CarMake.objects.filter().count()

    if(count == 0):
        initiate()

    car_models = CarModel.objects.select_related('car_make')

    cars = []

    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })

    return JsonResponse({"CarModels": cars})

def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})