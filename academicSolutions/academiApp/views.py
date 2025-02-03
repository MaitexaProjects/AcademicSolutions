from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login
from datetime import datetime
from django.contrib import messages
from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from decimal import Decimal, InvalidOperation
from .forms import FacilityForm




# Create your views here.


def home(request):
    return render(request,'home.html')




def create_user_and_profile(username, email, password, role, number, course, district, place, pin):
    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        AcademiApp.objects.create(
            user=user,
            role=role,
            number=number,
            course=course,
            district=district,
            place=place,
            pin=pin,
            status='pending'  # Default to pending approval
        )
        return user
    except Exception as e:
        print(f"Error creating user and profile: {e}")
        return None


def studentSignup(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        number = request.POST.get('number')
        course = request.POST.get('course')
        district = request.POST.get('district')
        place = request.POST.get('place')
        pin = request.POST.get('pin')

        user = create_user_and_profile(username, email, password, 'student', number, course, district, place, pin)

        if user:
            # Set status to 'pending'
            AcademiApp.objects.filter(user=user).update(status='pending')
            return redirect('login')
        else:
            return render(request, 'studentSignup.html', {'error': 'User not created. Please try again.'})

    return render(request, 'studentSignup.html')



def staffSignup(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        number = request.POST.get('number')
        district = request.POST.get('district')
        place = request.POST.get('place')
        pin = request.POST.get('pin')

        user = create_user_and_profile(username, email, password, 'staff', number, None, district, place, pin)

        if user:
            # Set status to 'pending'
            AcademiApp.objects.filter(user=user).update(status='pending')
            return redirect('login')
        else:
            return render(request, 'staffSignup.html', {'error': 'User not created. Please try again.'})

    return render(request, 'staffSignup.html')




def adminApproveRequests(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')

    pending_users = AcademiApp.objects.filter(status='pending')

    return render(request, 'adminApproveRequests.html', {'pending_users': pending_users})


def Approverequest(request,user_id):
    

    if request.method == 'POST':
        action = request.POST.get('action')

        print(f"User ID: {user_id}, Action: {action}")  # Debugging output

        try:
            user_profile = AcademiApp.objects.get(id=user_id)
            if action == 'Approve':
                user_profile.status = 'approved'
            elif action == 'Reject':
                user_profile.status = 'rejected'
            user_profile.save()
        except AcademiApp.DoesNotExist:
            pass  # Handle error if the user is not found

        return redirect('adminApproveRequests')

    return render(request, 'adminApproveRequests.html')






def login(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                user_profile = AcademiApp.objects.get(user=user)  # Get the user profile
                
                if user_profile.status != 'approved':  # Ensure the user is approved by admin
                    return render(request, 'login.html', {'error': 'Your account is pending approval by the admin.'})

                auth_login(request, user)  # Log the user in
                
                # Redirect based on role
                if user_profile.role == 'student':
                    return redirect('studentDashboard') 
                elif user_profile.role == 'staff':
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

        user=authenticate(username=username,password=password)
        if user:
            auth_login(request,user)
            return redirect('adminDashboard')
        else:
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
def studentattendance(request):
    """Display all attendance records for the logged-in student."""
    student = request.user 
    print(student)
    attendance_records = Attendance.objects.filter(student__user=student).order_by('-date')
    print(attendance_records)
    return render(request, 'stdattendance_report.html', {
        'student': student,
        'attendance_records': attendance_records
    })
    

@login_required
def add_facility(request):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to add facilities.")
        return redirect('home')

    if request.method == 'POST':
        form = FacilityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Facility added successfully!")
            return redirect('admin_dashboard')  # Redirect to admin dashboard or facility list
        else:
            messages.error(request, "There was an error adding the facility.")
    else:
        form = FacilityForm()

    return render(request, 'add_facility.html', {'form': form})

# View for Students to See Facilities
@login_required
def view_facilities(request):
    facilities = Facility.objects.all()
    return render(request, 'view_facilities.html', {'facilities': facilities})

















