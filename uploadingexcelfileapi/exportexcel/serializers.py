from rest_framework import serializers
from exportexcel import models

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Item
        fields="__all__"


    


