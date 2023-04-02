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
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')

    def is_staff(self):
        return self.is_admin
    
class Position(models.Model):
    position_name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.position_name

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

    def __str__(self):
        return f"Name {self.employee_name} Position {self.position.position_name}"

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

    def __str__(self):
        return self.patient_name

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    descrip = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.category_name

class Medicine(BaseModel):
    medicine_name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    description = RichTextField()
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='static/%S', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

class Order(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    medicines = models.ManyToManyField(Medicine, through='OrderDetail')


    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.date} - {self.time}"

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

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.date} - {self.time} - {self.shift}"

class Schedule(BaseModel):
    weekday = models.CharField(max_length=100)
    date = models.DateField()
    employees = models.ManyToManyField(Employee, through='ScheduleDetail')

    def __str__(self):
        return f"{self.weekday} - {self.date}"

class ScheduleDetail(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
