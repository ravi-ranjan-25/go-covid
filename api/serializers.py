from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import state,Product,order

class complainSerializer(serializers.ModelSerializer):
    # username = serializers.SerializerMethodField('Complain')
    
    class Meta:
        model = state
        fields = '__all__'

class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    


class ProductSerializer(serializers.Serializer):
    productName = serializers.CharField()
    productid = serializers.CharField()
    productDescription = serializers.CharField()
    stock = serializers.IntegerField()
    active = serializers.BooleanField()
    display = serializers.CharField()
    costPrice = serializers.FloatField()
    sellingPrice = serializers.FloatField()
    discount = serializers.FloatField()
    

class orderSerializer(serializers.Serializer):
    user = UserSerializer()
    product = ProductSerializer()
    amount = serializers.FloatField()
    orderid = serializers.CharField()
    accept = serializers.IntegerField()
