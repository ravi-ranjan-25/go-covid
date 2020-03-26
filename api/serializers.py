from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import state

class complainSerializer(serializers.ModelSerializer):
    # username = serializers.SerializerMethodField('Complain')
    
    class Meta:
        model = state
        fields = '__all__'

