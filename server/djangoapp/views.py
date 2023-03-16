from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel, CarDealer
from .restapis import (get_dealers_from_cf, get_dealer_reviews_from_cf, post_request)
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    current_endpoint = request.path
    context = {'current_endpoint': current_endpoint}
    if request.method == "GET":
        return render(request, "djangoapp/about.html", context)


# Create a `contact` view to return a static contact page
def contact(request):
    current_endpoint = request.path
    context = {'current_endpoint': current_endpoint}
    if request.method == "GET":
        return render(request, "djangoapp/contact.html", context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["psw"]
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect("django:index")
        else:
            context["message"] = "Invalid username or password."
            return render(request, "djangoapp/index.html", context)
            

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect("djangoapp:index")

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/registration.html", context)
    elif request.method == "POST":
        # Check if user exists
        username = request.POST["username"]
        password = request.POST["psw"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        user_exist = False
        try:
            User.objects.get(username = username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username = username, first_name = first_name, 
                                            last_name = last_name, password = password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context["message"] = "User already exists."
            return render(request, "djangoapp/registration.html", context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):

    if request.method == "GET":

        st = request.GET.get("st")
        dealerId = request.GET.get("dealerId")
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/52ac0e20-0ea8-4898-97d4-6706d5dd228d/dealership-package/get-dealership.json"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)

        if st:
            dealerships = get_dealers_from_cf(url, st=st)
        elif dealerId:
            dealerId = int(dealerId)
            dealerships = get_dealers_from_cf(url, dealerId=dealerId)

        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.full_name for dealer in dealerships])
        # Return a list of dealer full name
        return HttpResponse(dealer_names)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):

    if request.method == "GET":

        dealer_id = int(dealer_id)

        url = "https://us-south.functions.appdomain.cloud/api/v1/web/52ac0e20-0ea8-4898-97d4-6706d5dd228d/dealership-package/get-review.json"

        # Get reviews from the URL
        reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
        # Concat all review's content
        reviews_content = ' '.join([f"{review.review} - {review.sentiment}" for review in reviews])
        # Return a list of reviews content
        return HttpResponse(reviews_content)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):

    #if request.method == "POST":

        if request.user.is_authenticated:

            url = "https://us-south.functions.appdomain.cloud/api/v1/web/52ac0e20-0ea8-4898-97d4-6706d5dd228d/dealership-package/post-review.json"

            review = dict()
            review["id"] = 51
            review["time"] = datetime.utcnow().isoformat()
            review["name"] = "Gonzalo Raymond"
            review["dealership"] = int(dealer_id)
            review["review"] = "The electric mobility is the future"
            review["purchase"] = True
            review["purchase_date"] = "03/16/2023"
            review["car_make"] = "BYD"
            review["car_model"] = "HAN"
            review["car_year"] = 2023

            json_payload = dict()
            json_payload["review"] = review

            response = post_request(url, json_payload, dealerId = dealer_id)
            print(response)
            return HttpResponse(response)

        else:
            return redirect("djangoapp:index")
        
