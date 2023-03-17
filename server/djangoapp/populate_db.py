from .models import CarMake, CarDealer

def populate_db(car_make_set, car_model_list):

    for element in set_list:
        car_make = CarMake.objects.filter(name=element).values("id").first()
        if not car_make:
            CarMake.objects.create(name=element)
            

