from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True
        ordering = ['-id']

class User(BaseModel):
    user_name = models.CharField(max_length=30, unique=True)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=10)
    is_admin = models.BooleanField(default=False)
    
class Position(models.Model):
    position_name = models.CharField(max_length=100)
    description = models.TextField()

class Employee(BaseModel):
    employee_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    avatar = models.ImageField(upload_to='static/%S', null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    specialization = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Patient(BaseModel):
    patient_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    avatar = models.ImageField(upload_to='static/patient', null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    medical_history = RichTextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
class Medicine(BaseModel):
    medicine_name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='static/%S', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Order(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    medicines = models.ManyToManyField(Medicine, through='OrderDetail')



class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()
    payment_method = models.CharField(max_length=100, default='')
    total_money = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    class Meta:
        indexes = [
            models.Index(fields=['order'])
        ]

class Appointment(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    shift = models.CharField(max_length=100)
    state = models.CharField(max_length=100)


class Schedule(BaseModel):
    weekday = models.CharField(max_length=100)
    date = models.DateField()
    employees = models.ManyToManyField(Employee, through='ScheduleDetail')

class ScheduleDetail(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
