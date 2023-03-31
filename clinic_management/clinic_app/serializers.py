<<<<<<< Updated upstream
from .models import Category, Medicine
from rest_framework import serializers

class MedicineSerializer(serializers.Serializer):
    
    
    class Meta:
        model = Medicine
        fields = '__all__'
        exclude = ['category']
=======
from .models import (
    Category, Medicine , 
    User
)
from rest_framework import serializers

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['id', 'medicine_name', 'manufacturer', 'descrip', 'unit_price', 'image', 'category_id']
        # exclude = ['category_id']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']

class UserSerializer(serializers.ModelSerializer):

    # def create(self, validated_data):
    #     data = validated_data.copy()

    #     u = User(**data)
    #     u.role = "paitent"
    #     u.set_password(u.password)
    #     u.save()

    #     return u

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'user_name', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }
>>>>>>> Stashed changes

