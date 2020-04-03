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
from scrapyd_api import ScrapydAPI
# Create your views here.
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import covidscrap

# scrapyd = ScrapydAPI('http://localhost:6800')


def edit(request):
    st = request.GET.get('state')
    conf = request.GET.get('confirmedindians')
    conf1 = request.GET.get('confirmedinternational')
    hospital = request.GET.get('inhospital')
    death = request.GET.get('death')
    cure = request.GET.get('recovered')
    

    s = state.objects.get(name=st)
    
    if conf is not None:
        s.confirmedIndians = int(conf)
    
    if conf1 is not None:
        s.confirmedInternationals = int(conf1)
    
    if cure is not None:
        s.cured = int(cure)

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

def crawl(request):

    process = CrawlerProcess('covidscrap.settings')
    process.crawl(gocovid)
    process.start()

    # task = scrapyd.schedule('default', 'covidscrap')

    return JsonResponse({'result':1})
