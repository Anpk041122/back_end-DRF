from .models import (
    Category, User, Medicine, Employee, 
    Patient, Order, OrderDetail, Position,
    Appointment, Schedule, ScheduleDetail

)
from rest_framework import serializers

# - UserSerializer: Serializer cho User Model
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

# - PositionSerializer: Serializer cho Position Model
class PositionSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Position
        field = '__all__'

# - EmployeeSerializer: Serializer cho Employee Model
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        field = '__all__'
        exclude = ['user']
        
# - PatientSerializer: Serializer cho Patient Model
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        field = '__all__'

# - CategorySerializer: Serializer cho Category Model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# - MedicineSerializer: Serializer cho Medicine Model   
class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'
        
# - OrderSerializer: Serializer cho Order Model
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        field = '__all__'

# - OrderDetailSerializer : Serializer cho OrderDetail Model
class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        field = '__all__'

# - AppointmentSerializer : Serializer cho Appointment Model
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        field = '__all__'
# - ScheduleSerializer : Serializer cho Schedule Model
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        field = '__all__'
# - ScheduleDetailSerializer : Serializer cho ScheduleDetail Model
class ScheduleDetailSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ScheduleDetail
        field = '__all__'