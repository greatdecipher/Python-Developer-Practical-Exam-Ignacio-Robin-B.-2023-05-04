from django.db.models import Max
from backend.models import UserCars


def get_max_order(user) -> int:
    existing_cars = UserCars.objects.filter(user=user)
    if not existing_cars.exists():
        return 1
    else:
        current_max = existing_cars.aggregate(max_order=Max('order'))['max_order']
        return current_max + 1

def reorder(user):
    existing_cars = UserCars.objects.filter(user=user)
    if not existing_cars.exists():
        return
    number_of_cars = existing_cars.count()
    new_ordering = range(1, number_of_cars+1)
    
    for order, user_car in zip(new_ordering, existing_cars):
        user_car.order = order
        user_car.save()