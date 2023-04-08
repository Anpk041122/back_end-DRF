from django.contrib import admin
from .models import Category, User, Medicine
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.html import mark_safe
from django.contrib.auth.models import Permission

# Register your models here.
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Medicine)
admin.site.register(Permission)