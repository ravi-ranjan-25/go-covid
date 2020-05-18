from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class state(models.Model):
    name = models.CharField(unique = False,max_length=256)
    confirmedIndians = models.IntegerField(unique = False,max_length=256,default=0)
    active = models.IntegerField(unique = False,max_length=256,default=0)
    inHospital = models.IntegerField(unique = False,max_length=256,default=0)
    deaths = models.IntegerField(unique = False,max_length=256,default=0)
    cured = models.IntegerField(unique = False,max_length=256,default=0)
    
    # def __init__(self,Name,confirmedIndians1,confirmedInternationals1,deaths1,cured1):
      
    #     a = state.objects.filter(name=Name)
        
    #     if(a>0):
    #         p=a[0]
    #         p.confirmedIndians =  confirmedIndians1
    #         p.confirmedInternationals =  confirmedInternationals1
    #         p.deaths =  confirmeddeaths1
    #         p.cured =  confirmedcured1
    #         p.save()
    #     else:
    #         self.name= Name
    #         self.confirmedIndians = confirmedIndians1    
    #         self.confirmedInternationals = confirmedInternationals1    
    #         self.deaths = deaths1
    #         self.cured = cured1

    def __str__(self):
        return self.name     

class userdetails(models.Model):
     
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    mobile = models.CharField(unique = True,max_length=256)
    admin = models.BooleanField(default=False)
    objectname = models.CharField(unique = False,default="NA",max_length=256)
    # resturants = models.BooleanField(default=False)
    # airport = models.CharField(unique = False,default="NA",max_length=256)
    category = models.CharField(unique = False,default="NA",max_length=256)
    time = models.DateTimeField(default = timezone.now())

    def __str__(self):
        return self.user.username

# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    productName = models.CharField(unique = False,default="NA",max_length=256)
    productid = models.CharField(unique = True,default="NA",max_length=256)
    productDescription = models.CharField(unique = False,default="NA",max_length=256)
    stock = models.IntegerField(default=-1,max_length=256)
    active = models.BooleanField(default=True)
    display = models.CharField(unique=False,default="https://www.vikasanvesh.in/wp-content/themes/vaf/images/no-image-found-360x260.png",max_length=256)
    costPrice = models.FloatField(default=0.00,max_length=256)
    sellingPrice = models.FloatField(default=0.00,max_length=256)
    discount = models.FloatField(default=0.00,max_length=256)
    
    

    def __str__(self):
        return self.productName

class wallet(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    amount = models.FloatField(default=0.00,max_length=256)

    def __str__(self):
        return self.user.username

class order(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    amount = models.FloatField(default=0.00,max_length=256)
    orderid=models.CharField(unique = True,default="NA",max_length=256)
    accept = models.IntegerField(unique=False,default=-1,max_length=256)
    time = models.DateTimeField(default = timezone.now())
    
    def __str__(self):
        return self.product.productName

class storerestro(models.Model):
    Order = models.ForeignKey(order,on_delete = models.CASCADE)
    preparing_packaging = models.BooleanField(default=False)
    dispatched = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    Rating = models.FloatField(default=0.00,max_length=256)
    time = models.DateTimeField(default = timezone.now())
    
    def __str__(self):
        return self.Order.orderid
