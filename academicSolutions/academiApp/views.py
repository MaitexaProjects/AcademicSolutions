from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as log
from datetime import datetime
from django.contrib import messages
from datetime import date
from .forms import PortfolioForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from decimal import Decimal, InvalidOperation



# Create your views here.


def home(request):
    return render(request,'home.html')


def studentSignup(request):
    if request.method == 'POST':
        username=request.POST.get('Username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        number=request.POST.get('number')
        course=request.POST.get('course')
        district=request.POST.get('district')
        place=request.POST.get('place')
        pin=request.POST.get('pin')
        print(email)
        
       
        try:
            user=User.objects.create_user(username=username,email=email,password=password)
            AcademiApp.objects.create(user=user,role='student',number=number,course=course,district=district,place=place,pin=pin)
            print(user)   
            # login(request, user)

            return redirect('login')  
            
        except Exception as e:
            print(e)
            return render(request, 'studentSignup.html', {'error': 'User not created. Please try again.'})
        
    return render(request,'studentSignup.html')



def staffSignup(request):
    if request.method == 'POST':
        username=request.POST.get('Username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        number=request.POST.get('number')
        district=request.POST.get('district')
        place=request.POST.get('place')
        pin=request.POST.get('pin')

        print(password)

        try:
            user=User.objects.create_user(username=username,email=email,password=password)
            AcademiApp.objects.create(user=user,role='staff',number=number,district=district,place=place,pin=pin)
            print(f"User created: {user}")
            # login(request, user)
            return redirect('login')  
            
        except Exception as e:
            print(e)
            return render(request, 'staffSignup.html', {'error': 'User not created. Please try again.'})
        
    return render(request,'staffSignup.html')





def login(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            log(request,user)
            
            try:
                user_profile = AcademiApp.objects.get(user=user) 
                role = user_profile.role 
                
                if role == 'student':
                    return redirect('studentDashboard') 
                elif role == 'staff':
                    return redirect('staffDashboard') 
                else:
                    return redirect('adminDashboard') 
                    
            except AcademiApp.DoesNotExist:
                return render(request, 'login.html', {'error': 'User profile not found.'})
            
        else:
           
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    
    return render(request, 'login.html')




def studentDashboard(request):

    
    
    return render(request,'studentDashboard.html')
       
     
def adminDashboard(request):
    return render(request,'adminDashboard.html')

def staffDashboard(request):
    return render(request,'staffDashboard.html')

def adminlogin(request):
    if request.method=='POST':
        username = request.POST.get('Username')
        password = request.POST.get('password')
        try:
            if username=='admin' and password=='adminacademic':
                return redirect('adminDashboard')
        except:
            return redirect('adminlogin',{'error':"username password incorrect"})

    return render(request,'adminlogin.html')


def addCourse(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        duration = request.POST.get('duration')

        if not course_name or not description or not start_date or not end_date :
            messages.error(request, "All fields are required.")
            return redirect('addCourse')

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()



            Course.objects.create(
                course_name=course_name,
                description=description,
                start_date=start_date,
                end_date=end_date,
                duration=duration,
                )
            
            messages.success(request, "Course added successfully!")
            return redirect('courselist')
        
        except Exception as e:
            messages.error(request, f"Error adding course: {str(e)}")
            return redirect('addCourse')  
            
    return render(request,'addCourse.html')



def courselist(request):
    courses = Course.objects.all()

    return render(request,'courselist.html',{'courses': courses})


def studentList(request):
    students = AcademiApp.objects.filter(role='student')
    total_students = students.count()  
    
    context = {
        'students': students,
        'total_students': total_students,
    }
    
    return render(request, 'studentlist.html', context)



def markattendance(request):
    if request.method == 'POST':
     
        student_id = request.POST.get('student_id')
        attendance_status = request.POST.get('attendance_status')

        try:
          
            student = AcademiApp.objects.get(id=student_id, role='student')

          
            if attendance_status not in ['present', 'absent']:
                messages.error(request, "Please select a valid attendance status.")
                return redirect('attendance_page')  

         
            today = date.today()
            attendance_record, created = Attendance.objects.get_or_create(student=student, date=today)

           
            if attendance_status == 'present':
                attendance_record.is_present = True
            else:
                attendance_record.is_present = False

         
            attendance_record.save()

           
            messages.success(request, f"Attendance for {student.user.username} has been marked as {attendance_status}.")
            
            return redirect('studentList')  

        except AcademiApp.DoesNotExist:
            messages.error(request, "Student not found.")
            return redirect('studentlist')  
        
    else:
        students = AcademiApp.objects.filter(role='student')  
        return render(request,' studentList')
    






def attendance_report(request):
    student_name_filter = request.GET.get('student_name', '')  

   
    attendance_records = Attendance.objects.all()

   
    if student_name_filter:
        attendance_records = attendance_records.filter(student__user__username__icontains=student_name_filter)

    students = AcademiApp.objects.filter(role='student')

    return render(request, 'attendanceReport.html', {
        'attendance_records': attendance_records,
        'students': students, 
        'student_name_filter': student_name_filter,  
    })





@login_required 
def add_portfolio(request):
 
    try:
        student_profile = AcademiApp.objects.get(user=request.user, role='student')
    except AcademiApp.DoesNotExist:
        messages.error(request, "You are not authorized to add a portfolio.")
        return redirect('home') 

    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user
            portfolio.save()
            messages.success(request, "Portfolio added successfully!")
            return redirect('portfoliolist') 
        else:
            messages.error(request, "There was an error in your submission.")

    else:
        form = PortfolioForm()

    return render(request, 'addPortfolio.html', {'form': form})

def portfoliolist(request):
    portfolios = Portfolio.objects.all()
    return render(request,'portfoliolist.html', {'portfolios': portfolios})


@login_required
def stdportfolio(request):
    portfolios = Portfolio.objects.filter(user=request.user) 
    return render(request, 'stdportfolio.html', {'portfolios': portfolios})



def adminstudentlist(request):
    
    students = AcademiApp.objects.filter(role='student')
    
    return render(request, 'adminstudentlist.html', {'students': students})



def adminstafflist(request):

    staff = AcademiApp.objects.filter(role='staff')
    
    return render(request, 'adminstafflist.html', {'staff': staff})



@login_required
def student_attendance_report(request):
    """Display all attendance records for the logged-in student."""
    student = request.user 
    attendance_records = Attendance.objects.filter(student__user=student).order_by('-date')

    return render(request, 'attendance_report.html', {
        'student': student,
        'attendance_records': attendance_records
    })



















