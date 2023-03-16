import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key=None, **kwargs):
    #print(kwargs)
    #print("GET from {} ".format(url))
    try:

        params = kwargs

        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            params["language"] = kwargs["language"]
            # Basic authentication GET
            response = requests.get(url, params=params, headers={"Content-Type": "application/json"}, 
                            auth=HTTPBasicAuth("apikey", api_key))
        else:
            # Call get method of requests library with URL and parameters
            # no authentication GET
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'})       
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    #print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result:
        # Get the dealerships list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = ""
            if len(kwargs) > 0:
                dealer_doc = dealer
            else:
                dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result:
        # Get the reviews list in JSON as reviews
        reviews = json_result["reviews"]
        # For each review object
        review_obj = ""
        for review in reviews:
            # Create a DealerReview object with values in `review` object
            if "car_make" in review:
                review_obj = DealerReview(dealership=review["dealership"], name=review["name"], purchase=review["purchase"], 
                                          review=review["review"], id=review["id"], purchase_date=review["purchase_date"], 
                                          car_make=review["car_make"], car_model=review["car_model"], car_year=review["car_year"], 
                                          sentiment=analyze_review_sentiments(review["review"]))
            else:
                review_obj = DealerReview(dealership=review["dealership"], name=review["name"], purchase=review["purchase"], 
                                          review=review["review"], id=review["id"], sentiment=analyze_review_sentiments(review["review"]))
            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):

    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/3ed1e618-45f3-40f5-870d-8db214770298/v1/analyze"
    api_key = "RMA30zKOJfgyqhk70Uyyqo0bJcmjYvhcX6Lp1Pr3JzmD"
    json_result = get_request(url, api_key, text= dealerreview, 
                              version="2022-04-07", features=["sentiment"], 
                              return_analyzed_text=True, language="en")
    result = json_result["sentiment"]["document"]["label"]

    return result
