from django.contrib import admin
from .models import Inmate, Staff

# Register your models here.
admin.site.register(Inmate)
admin.site.register(Staff)