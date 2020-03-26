from django.shortcuts import render
from api.models import state
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
from django.http import JsonResponse
import random
from .serializers import complainSerializer
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

# Create your views here.


def edit(request):
    st = request.GET.get('state')
    conf = request.GET.get('confirmed')
    hospital = request.GET.get('inhospital')
    death = request.GET.get('death')

    s = state.objects.get(name=st)
    
    if conf is not None:
        s.confirmedCase = int(conf)

    if hospital is not None:
        s.inHospital = int(hospital)

    if death is not None:
        s.deaths = int(death)

    s.save()

    return JsonResponse({'result':1})


class complainListView(ListAPIView):
    queryset = state.objects.all()
    serializer_class = complainSerializer


def feed(request):
    states = ["Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","National Capital Territory of Delhi","Puducherry"]
    # z = len(state)
    
    for i in states:
        s = state(name=i)
        print(i)
        s.save()
        # i++

    return JsonResponse({'result':1})

