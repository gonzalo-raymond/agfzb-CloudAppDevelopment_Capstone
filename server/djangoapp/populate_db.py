
def populate_db(review_list):
 
    for review in review_list:
        if "car_make" in review:
            print(review.car_make)

