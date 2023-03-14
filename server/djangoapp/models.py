from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length = 30)
    description = models.CharField(max_length = 200)

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
    car_make = models.ForeignKey(CarMake, on_delete = models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(max_length = 20)

    SEDAN = "sedan"
    SUV = "suv"
    WAGON = "wagon"

    TYPE_CHOICES = [
        (SEDAN, "Sedan"),
        (SUV, "Suv"),
        (WAGON, "Wagon")
    ]

    car_type = models.CharField(
        null = False,
        max_length = 20,
        choices = TYPE_CHOICES,
        default = SEDAN
    )

    car_year = models.DateField(null = True)

    def car_make_name(self):
        return self.car_make.all().first()

    def __str__(self):
        return self.name



# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
