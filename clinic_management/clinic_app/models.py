from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser 

# Create your models here.

class BaseModel(models.Model):
    """
    A base model class that includes common fields for all models in the application.
    
    Fields:
        - created_at: A DateTimeField that represents the date and time the object was created.
        - updated_at: A DateTimeField that represents the date and time the object was last updated.
        - is_active: A BooleanField that indicates whether the object is currently active or not.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True
        ordering = ['-id']

class User(AbstractUser):
    """
    A model class that represents a user of the application.

    Fields:
        - avatar: An ImageField that stores the user's avatar image.
        - is_staff: A BooleanField that indicates whether the user is a staff member or not.
        - is_superuser: A BooleanField that indicates whether the user is a superuser or not.
        - is_doctor: A BooleanField that indicates whether the user is a doctor or not.
        - is_nurse: A BooleanField that indicates whether the user is a nurse or not.
    """
    avatar = models.ImageField(upload_to='users/%Y/%m/', null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_nurse = models.BooleanField(default=False)

class Position(models.Model):
    """
    A model class that represents a position of an employee.

    Fields:
        - position_name: A CharField that represents the name of the position.
        - description: A TextField that represents the description of the position.
    """
    position_name = models.CharField(max_length=100)
    description = models.TextField()

class Employee(BaseModel):
    """
    A model class that represents an employee of the hospital.

    Fields:
        - employee_name: A CharField that represents the name of the employee.
        - email: An EmailField that represents the email of the employee.
        - phone_number: A CharField that represents the phone number of the employee.
        - address: A CharField that represents the address of the employee.
        - date_of_birth: A DateField that represents the date of birth of the employee.
        - gender: A CharField that represents the gender of the employee.
        - specialization: A CharField that represents the specialization of the employee.
        - experience: A CharField that represents the experience of the employee.
        - position: A ForeignKey that represents the position of the employee.
        - user: A ForeignKey that represents the user associated with the employee.
    """
    employee_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    # avatar = models.ImageField(upload_to='static/employee/%S', null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    specialization = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Patient(BaseModel):
    """
    Represents a patient in the system.

    Fields:
        patient_name (str): The name of the patient.
        email (str): The email address of the patient.
        phone_number (str): The phone number of the patient.
        address (str): The address of the patient.
        date_of_birth (datetime.date): The date of birth of the patient.
        gender (str): The gender of the patient.
        medical_history (str): The medical history of the patient.
        user (User): The user associated with the patient.
    """
    patient_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    # avatar = models.ImageField(upload_to='static/patient', null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    medical_history = RichTextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Category(models.Model):
    """
    Category model represents the categories of the medicines.
    Fields:
        category_name (str): The name of the category.
        description (str, optional): The description of the category.
    """
    category_name = models.CharField(max_length=100)
    
class Medicine(BaseModel):
    """
    Medicine model represents the medicines available in the clinic.

    Fields:
        medicine_name (str): The name of the medicine.
        manufacturer (str): The name of the manufacturer.
        description (str): The description of the medicine.
        unit_price (float): The unit price of the medicine.
        image (str, optional): The image of the medicine.
        category (Category): The category of the medicine.
    """
    medicine_name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='static/medicine/', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Appointment(BaseModel):
    """
    Appointment model for medical appointments.

    Fields:
        patient (Patient): The patient who made the appointment.
        employee (Employee): The employee who will attend the appointment.
        date (datetime.date): The date of the appointment.
        time (datetime.time): The time of the appointment.
        shift (str): The shift of the appointment.
        state (str): The state of the appointment.
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    shift = models.CharField(max_length=100)
    state = models.CharField(max_length=100)


class MedicalHistory(BaseModel):
    """
    MedicalHistory model for patients' medical histories.

    Fields:
        patient (User): The patient who has the medical history.
        doctor (Employee): The doctor who performed the medical examination.
        appointment (Appointment): The appointment where the medical examination was performed.
        symptoms (str): The symptoms of the patient.
        diagnosis (str): The diagnosis of the patient.
        order (Order): The order related to the medical examination.
    """
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_histories')
    doctor = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='medical_histories')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='medical_histories')
    symptoms = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)

class Order(BaseModel):
    """
    Order model represents the order made by patients.

    Fields:
        patient (Patient): The patient who made the order.
        employee (Employee): The employee who processed the order.
        medicines (Medicine): The medicines in the order.
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    medicines = models.ManyToManyField(Medicine, through='OrderDetail')
    medical_history = models.ForeignKey(MedicalHistory, on_delete=models.CASCADE)


class OrderDetail(models.Model):
    """
    OrderDetail model represents the details of the order made by patients.

    Fields:
        order (Order): The order this detail is associated with.
        medicine (Medicine): The medicine in this detail.
        quantity (int): The quantity of the medicine.
        dosage (str): The dosage of the medicine.
        instructions (str): The instructions of the medicine.
        payment_method (str, optional): The payment method of the order.
        total_money (float, optional): The total money of the order.
    """
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

class Schedule(BaseModel):
    """
    Schedule model for medical employees' schedules.

    Fields:
        weekday (str): The weekday of the schedule.
        date (datetime.date): The date of the schedule.
        employees (Employee): The employees on the schedule.
    """
    weekday = models.CharField(max_length=100)
    date = models.DateField()
    employees = models.ManyToManyField(Employee, through='ScheduleDetail')

class ScheduleDetail(models.Model):
    """
    ScheduleDetail model for schedule details of medical employees.

    Fields:
        schedule (Schedule): The schedule of the employee.
        employee (Employee): The employee on the schedule.
        start_time (datetime.time): The start time of the schedule.
        end_time (datetime.time): The end time of the schedule.
    """
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()