from .models import Category, Medicine
from rest_framework import serializers

class MedicineSerializer(serializers.Serializer):
    
    
    class Meta:
        model = Medicine
        fields = '__all__'
        exclude = ['category']

