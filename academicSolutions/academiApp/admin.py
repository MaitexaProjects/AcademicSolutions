from django.contrib import admin
from .models import *
# Register your models here.

class MarksAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'marks_obtained', 'total_marks', 'exam_date', 'percentage')


admin.site.register(AcademiApp)
admin.site.register(Attendance)
admin.site.register(Course)
admin.site.register(Portfolio)
admin.site.register(AcademicPerformance)



