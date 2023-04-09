from .models import (
    Category, User, Medicine, Employee, 
    Patient, Order, OrderDetail, Position,
    Appointment, Schedule, ScheduleDetail, MedicalHistory

)
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.models import Group

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        data = validated_data.copy()
        u = User(**data)
        u.password = make_password(u.password)
        u.save()
        g = Group.objects.get(name = "Patient")
        u.groups.add(g) 
        return u

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        # fields = '__all__'
        extra_kwargs = {
            'username' : {'read_only': True},
            'avatar': {'write_only': True},
            'password': {'write_only': True}
        }

# - PositionSerializer: Serializer for Position Model
class PositionSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Position
        field = '__all__'

# - EmployeeSerializer: Serializer for Employee Model
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        field = '__all__'
        exclude = ['user']
        
# - PatientSerializer: Serializer for Patient Model
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        field = '__all__'

# - CategorySerializer: Serializer for Category Model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# - MedicineSerializer: Serializer for Medicine Model   
class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'
        
# - OrderSerializer: Serializer for Order Model
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        field = '__all__'

# - OrderDetailSerializer : Serializer for OrderDetail Model
class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        field = '__all__'

# - AppointmentSerializer : Serializer for Appointment Model
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        field = '__all__'
# - ScheduleSerializer : Serializer for Schedule Model
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        field = '__all__'
# - ScheduleDetailSerializer : Serializer for ScheduleDetail Model
class ScheduleDetailSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ScheduleDetail
        field = '__all__'
# - MedicationSerializer : Serializer for Medication Model
class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        field = ['symptoms', 'diagnosis', 'appointment', 'patient', 'doctor']