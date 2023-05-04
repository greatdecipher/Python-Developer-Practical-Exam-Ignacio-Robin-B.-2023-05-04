from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from backend.forms import RegisterForm
from backend.models import Car, UserCars
from backend.utils import get_max_order, reorder
from django.views.generic.list import ListView

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'
    
class Login(LoginView):
    template_name = 'registration/login.html'

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)


class CarList(LoginRequiredMixin, ListView):
    template_name = 'cars.html'
    model = Car
    context_object_name = 'cars'

    def get_queryset(self):
        return UserCars.objects.filter(user=self.request.user)


def check_username(request):
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse("<div id='username-error' class='error'>This username already exists</div>")
    else:
        return HttpResponse("<div id='username-error' class='success'>This username is available</div>")

@login_required
def add_car(request):
    name = request.POST.get('carname')
    
    # add car
    car = Car.objects.get_or_create(name=name)[0]
    
    # add the car to the user's list
    if not UserCars.objects.filter(car=car, user=request.user).exists():
        UserCars.objects.create(
            car=car, 
            user=request.user, 
            order=get_max_order(request.user)
        )

    # return template fragment with all the user's cars
    cars = UserCars.objects.filter(user=request.user)
    messages.success(request, f"Added {name} to list of cars")
    return render(request, 'partials/car-list.html', {'cars': cars})

@require_http_methods(['DELETE'])
@login_required
def delete_car(request, pk):
    ...
    # remove the car from the user's list
    UserCars.objects.get(pk=pk).delete()

    reorder(request.user)

    # return template fragment with all the user's cars
    cars = UserCars.objects.filter(user=request.user)
    return render(request, 'partials/car-list.html', {'cars': cars})

@login_required
def search_car(request):
    search_text = request.POST.get('search')

    # look up all cars that contain the text
    # exclude user cars
    usercars = UserCars.objects.filter(user=request.user)
    results = Car.objects.filter(name__icontains=search_text).exclude(
        name__in=usercars.values_list('car__name', flat=True)
    )
    context = {"results": results}
    return render(request, 'partials/search-results.html', context)

def clear(request):
    return HttpResponse("")

def sort(request):
    car_pks_order = request.POST.getlist('car_order')
    cars = []
    for idx, car_pk in enumerate(car_pks_order, start=1):
        usercar = UserCars.objects.get(pk=car_pk)
        usercar.order = idx
        usercar.save()
        cars.append(usercar)

    return render(request, 'partials/car-list.html', {'cars': cars})