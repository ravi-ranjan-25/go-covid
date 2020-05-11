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
from scrapy.crawler import CrawlerRunner,CrawlerProcess
from scrapy.utils.project import get_project_settings
from covidscrap.spiders import gocovid
# scrapyd = ScrapydAPI('http://localhost:6800')
from bs4 import BeautifulSoup
import requests

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
    url = "https://www.mohfw.gov.in/"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    
# print(soup.prettify())

    
    trs = soup.find_all('tr')

    item= []
    
    for tr in trs[1:-5]:
        list = {}
        tds = tr.find_all("td")
        print(tds)
        list['name']=str(tds[1].get_text())
        list['confirmed'] = str(tds[2].get_text())
        list['deaths'] = str(tds[4].get_text())
        list['cured'] = str(tds[3].get_text())
        list['active'] = int(list['confirmed']) - int(list['deaths']) - int(list['cured']) 
        z = state.objects.filter(name=list['name'])

        if z == 0:
            o = state(name=list['name'],confirmedIndians=list['confirmed'],active=list['active'],deaths=list['deaths'],cured=list['cured'])
            o.save()
        else:
            z[0].name=list['name']
            z[0].confirmedIndians=list['confirmed']
            z[0].active=list['active']
            z[0].deaths=list['deaths']
            z[0].cured=list['cured']
            z[0].save()

        item.append(list)    

    # process = CrawlerRunner(get_project_settings())
    
    # process.crawl(gocovid.covidspider)
    # # process.start()

    # task = scrapyd.schedule('default', 'covidscrap')

    return JsonResponse({'result':item})

def currentprices(request): 
    html_resp = urlopen("https://www.mohfw.gov.in/") 
    response = scrapy.http.HtmlResponse(html_resp) 
    
    for p in response.xpath('//*[@id="state-data"]/div/div/div/div/table/tbody/tr')[:-3]:
            print(p)
            item = stateItem()
            item['confirmedInternationals'] = 0
            item['name']=p.css('td::text')[1]
            item['confirmedIndians'] = p.css('td::text')[2]
            item['deaths'] = p.css('td::text')[4]
            item['cured'] = p.css('td::text')[3]
            print(item)
            yield item
    