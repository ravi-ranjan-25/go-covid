from django.shortcuts import render
from api.models import state,Product,order,wallet,storerestro,userdetails
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
from django.http import JsonResponse
import random
from .serializers import complainSerializer,ProductSerializer,orderSerializer
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
import os
import pickle
import joblib
import json
import numpy as np 
from sklearn import preprocessing 
import pandas as pd

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

        if len(z) == 0:
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
    
def Predict(unit):
    try:
        BASE_DIRS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_dir= os.path.join(BASE_DIRS,'api/covid_pred_model1.pkl')

        mdl=joblib.load(model_dir)
        
        X=unit
        X=np.array(unit)
        # X=X.reshape(1,-1)
        print(mdl)
        y_pred=mdl.predict(X)
        
        newdf=pd.DataFrame(y_pred>0.58, columns=['RISK'])
        return y_pred
    except ValueError as e:
        return (e.args[0])


def ohevalue(df):
    BASE_DIRS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_dir= os.path.join(BASE_DIRS,'api/covid_ohe1.pkl')
    ohe_col = joblib.load(model_dir)
    print(ohe_col)
    print(11111111111111111111111111111111111111111)
    cat_columns=['Age','Body Temp','Dry Cough','Tiredness','Chest Pain','Nasal Congestion','Runny Nose','Sore Throat','Diarrhea','Difficulty in Breathing','High Blood Pressure','Heart Problems','Diabetes','Current Smoker','Contact with a person with fever or cold in last few days']
    df_processed = pd.get_dummies(df, columns=cat_columns)
    print(df_processed['Dry Cough_1'].values[0])
    
    newdict={}
    
    for i in ohe_col:
        if i in df_processed.columns:
            d = df_processed[i].values
            newdict[i]= d[0]
            print(d)
        else:
    	    newdict[i]=0
    
    newdf=pd.DataFrame(newdict,index=[0])
    print(newdf)
    
    return newdf



def predict1(request):
    myDict = (request.GET).dict()
    df=pd.DataFrame(myDict, index=[0])
    answer=Predict(ohevalue(df)).tolist()
    # a = answer[0]
    
    for i in answer:
        a = i 
    return JsonResponse({'result':i})

def signup(request):
    userName = request.GET.get('username')
    eMail = request.GET.get('email')
    firstname = request.GET.get('firstname')
    lastname = request.GET.get('lastname')
    Password = request.GET.get('password')
    Mobile = request.GET.get('mobile')
    Airport = request.GET.get('airport')
    Category1 = request.GET.get('category')
    Object_name = request.GET.get('object_name')
    
    check = User.objects.filter(username = userName)
    checkEmail = User.objects.filter(email = eMail)
    checkHouse = userdetails.objects.filter(mobile=Mobile)
   

    if len(check) > 0:
        
            return JsonResponse({'result':0,'message':'Username already exist'})
    
    elif len(checkEmail) > 0:

            return JsonResponse({'result':0,'message':'Email address already exist'})


    elif len(checkHouse) > 0:
             return JsonResponse({'result':0,'message':'Mobile already registered'}) 

    
    else:
        # if Cab == 'y':
        #     Cab = True
        # else:
        #     Cab = False
        
        # if Hotel == 'y':
        #     Hotel = True
        # else:
        #     Hotel = False

        # if Restro == 'y':
        #     Restro = True
        # else:
        #     Restro = False

        # if Store == 'y':
        #     Store = True
        # else:
        #     Store = False    

        if Category1 is not None:
            Category1 = Category1.upper()
        else:
            Category1 = 'NA'

        if Object_name is None:
            Object_name = 'NA'

        if Airport is None:
            Airport = 'NA'

        user1 = User.objects.create_user(username = userName, email=eMail, password=Password, first_name = firstname , last_name = lastname)
        userD = userdetails(user=user1,mobile=Mobile,category=Category1,objectname=Object_name)

        w = wallet(user=user1)
        w.save()
        user1.save()
        userD.save()
        return JsonResponse({'result':1,'message':'success'})

def login(request):
    userName = request.GET.get('username')
    Password = request.GET.get('password')
    

    user1 = authenticate(username=userName, password=Password)
    
    if user1 is not None:
        house = userdetails.objects.get(user = user1)
        return JsonResponse({'result':1,'username':user1.username,'email':user1.email,'firstname':user1.first_name,
                                'lastname':user1.last_name,'mobile':house.mobile,'objectName':house.objectname,'category': house.category})
    
    else:
        return JsonResponse({'result':0,'message':'Incorrect username or password'})


def addProduct(request):
    Username = request.GET.get('username')
    Name = request.GET.get('name')
    Description = request.GET.get('description')
    Stock = request.GET.get('stock')
    Active = request.GET.get('active')
    Display = request.GET.get('dp')
    cost = request.GET.get('costprice')
    sell = request.GET.get('sellprice')
    Discount= request.GET.get('discount')

    if Active == 'y':
        Active = True
    else:
        Active = False    
        

    user1 = User.objects.get(username=Username)
    # userD = userdetails.object.get(user = user1)
    proid = "PROD"+str(random.randint(9999,99999))
    add = Product(user=user1,productName=Name,productid=proid,productDescription=Description,stock=Stock,active=Active,display=Display,costPrice=cost,sellingPrice=sell,discount=Discount)
    add.save()



    return JsonResponse({'result':1,'message':'Success'})

def editproduct(request):
    Username = request.GET.get('username')
    Name = request.GET.get('Name')
    Description = request.GET.get('description')
    Stock = request.GET.get('stock')
    Active = request.GET.get('active')
    Display = request.GET.get('dp')
    cost = request.GET.get('costprice')
    sell = request.GET.get('sellprice')
    Discount= request.GET.get('discount')
    proid = request.GET.get('productid')
        
    p = Product.objects.get(productid=proid)

    if Name is not None:
        p.name = Name

    if Description is not None:
        p.productDescription = Description

    if Stock is not None:
        p.stock = int(Stock)

    if Active is not None:
        if Active == 'y':
            Active = True
        else:
            Active = False    
        p.name = Active

    if Display is not None:
        p.display = Display

    if cost is not None:
        p.costPrice = float(cost)

    if sell is not None:
        p.sell = float(sellprice)
        
    if Discount is not None:
        p.discount = float(Discount)

    p.save() 
    return JsonResponse({'result':1,'message':'Success'})

def viewProduct(request):
    proid = request.GET.get('productid')
    isALL = request.GET.get('all')
    Username = request.GET.get('username')

    list = []

    if isALL == 'y':
        p = Product.objects.all()        
        
        for a in p:
            serial = ProductSerializer(a)
            list.append({'Product':serial.data})
        return JsonResponse({'result':1,'Product':list})
    
    elif Username is not None:
        user1 = User.objects.get(username=Username)    
        p = Product.objects.filter(user=user1)        
        

        for a in p:
            serial = ProductSerializer(a)
            list.append({'Product':serial.data})
        return JsonResponse({'result':1,'Product':list})
    
    else:
        p = Product.objects.get(productid=proid)
        serial = ProductSerializer(p)

    return JsonResponse({'result':1,'Product':serial.data})
 

def placeOrder(request):
    proid = request.GET.get('productid')
    Username = request.GET.get('username')    
    
    user1 = User.objects.get(username=Username)
    p = Product.objects.get(productid=proid)
    w = wallet.objects.get(user = user1)
    w1 = wallet.objects.get(user = p.user)

    a = p.sellingPrice + p.sellingPrice*p.discount

    w.amount = w.amount - a
    w1.amount = w1.amount + a 
    proid = "OD"+str(random.randint(999999,9999999))

    o = order(user=user1,product=p,amount=a,orderid=proid)

    o.save()
    w.save()
    w1.save()
    return JsonResponse({'result':1,'message':'Success'})


def viewliveStoreorders(request):
    Username = request.GET.get('username')    
    
    user1 = User.objects.get(username=Username)
    
    o = order.objects.filter(product__user=user1,accept=-1)
    list = []

    for a in o:
        serial = orderSerializer(a)
        list.append({'order':serial.data})
        
    return JsonResponse({'result':list})
         
        
def acceptorder(request):
    proid = request.GET.get('orderid')

    o = order.objects.get(orderid=proid)

    o.accept=0
    ud = userdetails.objects.get(user = o.product.user)
    if ud.category == 'HOTEL':
        n = hotel(Order=o)
        n.save()
    else:
        n = storerestro(Order=o)
        n.save()
            
    o.save()
    

    return JsonResponse({'result':1})

def userorder(request):
    userName = request.GET.get('username')

    user1 = User.objects.get(username=userName)
    o = order.objects.filter(user=user1)

    list = []

    for a in o:
        serial = orderSerializer(a)
        list.append({'order':serial.data})
        
    return JsonResponse({'result':list})


def storeorder(request):
    odid = request.GET.get('orderid')
    prepare = request.GET.get('packaging')
    dispatched1 = request.GET.get('dispatched')
    delivered1 = request.GET.get('delivered')
    rating1 = request.GET.get('rating')
    print(odid)
    d = order.objects.get(orderid=odid)
    o = storerestro.objects.get(Order=d)

    if prepare is not None:
        o.preparing_packaging = True

    if dispatched1 is not None:
        o.dispatched = True

    if delivered1 is not None:
        o.delivered = True

    if rating1 is not None:
        o.Rating = rating1


    o.save()    
    return JsonResponse({'result':1})

