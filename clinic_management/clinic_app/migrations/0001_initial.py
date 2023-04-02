# Generated by Django 4.1.7 on 2023-04-02 05:39

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('descrip', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('employee_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=200)),
                ('avatar', models.ImageField(null=True, upload_to='static/%S')),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('specialization', models.CharField(max_length=100)),
                ('experience', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('medicine_name', models.CharField(max_length=100)),
                ('manufacturer', models.CharField(max_length=100)),
                ('description', ckeditor.fields.RichTextField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('image', models.ImageField(null=True, upload_to='static/%S')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_app.category')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_app.employee')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('dosage', models.CharField(max_length=100)),
                ('instructions', models.TextField()),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_app.medicine')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_app.order')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('weekday', models.CharField(max_length=100)),
                ('date', models.DateField()),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user_name', models.CharField(max_length=30, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('password', models.CharField(max_length=20)),
                ('role', models.CharField(max_length=10)),
                ('is_admin', models.BooleanField(default=False)),
                ('first_name', models.CharField(default='', max_length=100)),
                ('last_name', models.CharField(default='', max_length=100)),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScheduleDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_app.employee')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_app.schedule')),
            ],
        ),
        migrations.AddField(
            model_name='schedule',
            name='employees',
            field=models.ManyToManyField(through='clinic_app.ScheduleDetail', to='clinic_app.employee'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(max_length=100)),
                ('total_money', models.DecimalField(decimal_places=2, max_digits=7)),
                ('order_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_app.orderdetail')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('patient_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=200)),
                ('avatar', models.ImageField(null=True, upload_to='static/patient')),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('medical_history', ckeditor.fields.RichTextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_app.user')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='order',
            name='medicines',
            field=models.ManyToManyField(through='clinic_app.OrderDetail', to='clinic_app.medicine'),
        ),
        migrations.AddField(
            model_name='order',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_app.patient'),
        ),
        migrations.AddField(
            model_name='employee',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_app.position'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_app.user'),
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('shift', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_app.employee')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_app.patient')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='orderdetail',
            index=models.Index(fields=['order'], name='clinic_app__order_i_c76d1f_idx'),
        ),
    ]
