from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Attendance)
admin.site.register(Students)
admin.site.register(Teachers)
admin.site.register(Courses)
admin.site.register(Subjects)
admin.site.register(Notifications)
admin.site.register(TimeTables)
