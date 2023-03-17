from .models import CarMake, CarModel

def populate_db(cars_list):

    for car in cars_list:
        car_make = CarMake.objects.filter(name=car["car_make_name"]).values("id").first()
        car_model = CarModel.objects.filter(name=car["name"], dealer_id=car["dealer_id"]).values("id").first()
        if not car_make and not car_model:
            new_car_make = CarMake(name=car["car_make_name"])
            new_car_make.save()
            new_car_model = CarModel(name=car["name"], dealer_id=car["dealer_id"], car_year=car["car_year"])
            new_car_model.car_make = new_car_make
            new_car_model.save()
        elif car_make and not car_model:
            existing_car_make = CarMake.objects.get(id=car_make["id"])
            new_car_model = CarModel(name=car["name"], dealer_id=car["dealer_id"], car_year=car["car_year"])
            new_car_model.car_make = existing_car_make
            new_car_model.save()
