from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('home/',views.home,name='home'),
    path('studentSignup/',views.studentSignup,name='studentSignup'),
    path('staffSignup/',views.staffSignup,name='staffSignup'),
    # path('studentSignup/',views.studentSignup,name='studentSignup'),
    path('login/',views.login,name='login'),
    path('studentDashboard/',views.studentDashboard,name='studentDashboard'),
    path('staffDashboard/',views.staffDashboard,name='staffDashboard'),
    path('adminDashboard/',views.adminDashboard,name='adminDashboard'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('addCourse/',views.addCourse,name='addCourse'),  
    path('courselist/',views.courselist,name='courselist'),  
    path('studentList/',views.studentList,name='studentList'),
    path('markattendance/',views.markattendance,name='markattendance'),
    path('attendance_report/',views.attendance_report,name='attendance_report'),
    path('add_portfolio/',views.add_portfolio,name='add_portfolio'),
    path('portfoliolist/',views.portfoliolist,name='portfoliolist'),
    path('stdportfolio/',views.stdportfolio,name='stdportfolio'),
    path('adminstudentlist/',views.adminstudentlist,name='adminstudentlist'),
    path('adminstafflist/',views.adminstafflist,name='adminstafflist'),
    path('addmark/',views.addmark,name='addmark')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)