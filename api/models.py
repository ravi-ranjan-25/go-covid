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

 