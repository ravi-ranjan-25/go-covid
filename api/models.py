from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class state(models.Model):
    name = models.CharField(unique = True,max_length=256)
    confirmedCase = models.IntegerField(unique = False,max_length=256,default=0)
    inHospital = models.IntegerField(unique = False,max_length=256,default=0)
    deaths = models.IntegerField(unique = False,max_length=256,default=0)
    time = models.DateTimeField(unique = False,default = timezone.now())

    def __str__(self):
        return self.name     

 