import sys
from django.utils.timezone import now
from django.db import models
from django.conf import settings
import uuid



# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):

    name = models.CharField(null=False, max_length=30, default="Car Maker")
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(default=0)
    name = models.CharField(max_length=200, default="Model")

    SEDAN = "sedan"
    SUV = "suv"
    WAGON = "wagon"
    COUPE = "coupe"

    TYPE_CHOICES = [
        (SEDAN, "Sedan"),
        (SUV, "Suv"),
        (WAGON, "Wagon"),
        (COUPE, "Coupe")
    ]

    car_type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default=SEDAN
    )

    car_year = models.DateField(null=True)

    def __str__(self):
        return self.name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, state, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer state
        self.state = state
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, purchase, review, id, purchase_date=None, car_make=None, car_model=None, car_year=None, sentiment=None):
        # Review Dealership
        self.dealership = dealership
        # User Name
        self.name = name
        # Purchase Status
        self.purchase = purchase
        # User Review
        self.review = review
        # Purchase Date
        self.purchase_date = purchase_date
        # Car Make
        self.car_make = car_make
        # Car Model
        self.car_model = car_model
        # Car Year
        self.car_year = car_year
        # User Sentiment
        self.sentiment = sentiment
        # Review Id
        self.id = id

        def __str__(self):
            return "Review: " + self.review
