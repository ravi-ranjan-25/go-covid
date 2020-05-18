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
    path('crawl',views.crawl , name = "login"),
    path('predict',views.predict1 , name = "login"),
   

    #############################################################
    #############################################################
    #############################################################


    path('signup',views.signup , name = "signup"),
    path('login',views.login , name = "login"),
    path('addproduct',views.addProduct,name="add"),
    path('editproduct',views.editproduct,name="add"),
    path('viewproduct',views.viewProduct,name="add"),
    path('placeorder',views.placeOrder,name="add"),
    path('viewpendingorders',views.viewliveStoreorders,name="add"),
    path('acceptorder',views.acceptorder,name="add"),
    path('showuserorder',views.userorder,name="add"),
    
    path('processorder',views.storeorder,name="add"),



]
