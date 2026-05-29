import json
import logging
from .models import CarMake, CarModel
from .populate import initiate
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from .restapis import get_request, analyze_review_sentiments, post_review

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

# Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state

    dealerships = get_request(endpoint)

    return JsonResponse({"status":200,"dealers":dealerships})

def get_dealer_details(request, dealer_id):
    endpoint = "/fetchDealer/" + dealer_id

    dealer = get_request(endpoint)

    return JsonResponse({"status":200, "dealer":dealer})

def get_dealer_reviews(request, dealer_id):
    endpoint = "/fetchReviews/dealer/" + dealer_id

    reviews = get_request(endpoint)

    for review_detail in reviews:
        response = analyze_review_sentiments(review_detail["review"])
        review_detail["sentiment"] = response

    return JsonResponse({"status":200, "reviews":reviews})

def add_review(request):

    if(request.user.is_anonymous == False):

        data = json.loads(request.body)

        try:
            response = post_review(data)

            print(response)

            return JsonResponse({"status":200})

        except:
            return JsonResponse({
                "status":401,
                "message":"Error in posting review"
            })

    else:
        return JsonResponse({
            "status":403,
            "message":"Unauthorized"
        })

def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})