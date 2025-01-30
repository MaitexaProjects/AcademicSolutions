from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.


class AcademiApp(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    role= models.CharField(max_length=100 ,choices=[('student', 'Student'), ('staff', 'Staff'), ('admin', 'Admin')], default='student')
    course=models.CharField(max_length=100,null=True,blank=True)
    number=models.IntegerField(null=True,blank=True)
    place=models.CharField(max_length=100,null=True,blank=True)
    district=models.CharField(max_length=100,null=True,blank=True)
    pin=models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.user.username


# class Faculty(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField()
    
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    course_name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.IntegerField( blank=True)
    # faculty_in_charge = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    def __str__(self):
        return self.course_name
    


class Attendance(models.Model):
    student = models.ForeignKey(AcademiApp, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    date = models.DateField()
    is_present = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'date'], name='unique_student_date')
        ]

    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {'Present' if self.is_present else 'Absent'}"
    

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    title = models.CharField(max_length=200)
    description = models.TextField()
    document = models.FileField(upload_to='documents/', blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Marks(models.Model):
    student = models.ForeignKey(AcademiApp, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField()
    total_marks = models.IntegerField()
    exam_date = models.DateField()

    def __str__(self):
        return f"{self.student.user.username} - {self.course.course_name} - {self.exam_date}"
    



    




