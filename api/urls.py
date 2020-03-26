from django.contrib import admin
from django.urls import path,include
from api import views
from rest_framework import routers
from .views import complainListView


urlpatterns = [
# path('/user', , name = "userConsumptionN"),

    path('liststatedata',complainListView.as_view() , name = "Event"),
    path('feeddata',views.feed , name = "login"),
    path('edit',views.edit , name = "login"),
   
]
