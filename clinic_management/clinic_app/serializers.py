from .models import (
    Category, User, Medicine, Employee, 
    Patient, Order, OrderDetail, Position,
    Appointment, Schedule, ScheduleDetail, MedicalHistory

)
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.models import Group

class AdminUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        """
        Create a new admin user from validated data.

        Parameters:
        -----------
        validated_data: dict
            The validated data to create the admin user from.

        Returns:
        --------
        u: User
            The newly created admin user.
        """
        data = validated_data.copy()
        u = User(**data)    
        u.password = make_password(u.password)
        u.save()
        if u.is_doctor:
            g = Group.objects.get(name = "Doctor")
        else:
            g = Group.objects.get(name = "Nurse")
            
        u.groups.add(g) 
        return u
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_doctor', 'is_nurse', 'is_staff']
        # fields = '__all__'
        extra_kwargs = {
            'avatar': {'write_only': True},
            'password': {'write_only': True}
        }

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        """
        Create a new regular user from validated data.

        Parameters:
        -----------
        validated_data: dict
            The validated data to create the regular user from.

        Returns:
        --------
        u: User
            The newly created regular user.
        """
        data = validated_data.copy()
        u = User(**data)
        u.password = make_password(u.password)
        u.save()
        
        
        g = Group.objects.get(name = "Patient")
        u.groups.add(g) 
        return u

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'avatar','is_doctor', 'is_nurse', 'is_staff']
        extra_kwargs = {
            'avatar': {'write_only': True},
            'password': {'write_only': True}
        }

# - PositionSerializer: Serializer for Position Model
class PositionSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Position
        fields = '__all__'

# - EmployeeSerializer: Serializer for Employee Model
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        
# - PatientSerializer: Serializer for Patient Model
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

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
        fields = '__all__'

# - OrderDetailSerializer : Serializer for OrderDetail Model
class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'

# - AppointmentSerializer : Serializer for Appointment Model
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
# - ScheduleSerializer : Serializer for Schedule Model
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'
# - ScheduleDetailSerializer : Serializer for ScheduleDetail Model
class ScheduleDetailSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ScheduleDetail
        fields = '__all__'
# - MedicationSerializer : Serializer for Medication Model
class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = ['symptoms', 'diagnosis', 'appointment', 'patient', 'doctor']