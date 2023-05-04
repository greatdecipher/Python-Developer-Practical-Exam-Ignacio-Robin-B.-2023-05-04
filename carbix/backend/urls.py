from django.urls import path
from backend import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("cars/", views.CarList.as_view(), name='car-list'),
]

htmx_urlpatterns = [
    path('check_username/', views.check_username, name='check-username'),
    path('add-car/', views.add_car, name='add-car'),
    path('delete-car/<int:pk>/', views.delete_car, name='delete-car'),
    path('search-car/', views.search_car, name='search-car'),
    path('clear/', views.clear, name='clear'),
    path('sort/', views.sort, name='sort'),
]

urlpatterns += htmx_urlpatterns