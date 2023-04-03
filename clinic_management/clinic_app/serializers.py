from .models import (
    Category, User, Medicine, Employee, 
    Patient, Order, OrderDetail, Position,
    Appointment, Schedule, ScheduleDetail

)
from rest_framework import serializers

# - UserSerializer: Serializer for User Model
class UserSerializer(serializers.ModelSerializer):

    # override create of generic.CreateAPIView 
    # set default role is ` paitient `
    # use the ` set_password ` function to hash the password
    def create(self, validated_data):
        data = validated_data.copy()

        u = User(**data)
        u.role = "paitent"
        u.set_password(u.password)
        u.save()

        return u

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
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