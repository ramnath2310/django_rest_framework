from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from employees.models import Employees
from .serializers import EmployeesSerializer1
from rest_framework import generics

router = DefaultRouter()
router.register('employeesets', views.EmployeeViewSet,basename='employees')


urlpatterns =[
    path('students/',views.students_api),
    path('students/<int:pk>',views.studentDetailsView),
    path('employee/',views.Employeesclass.as_view()),
    path('employees/employeemixin/',views.EmployeeMixin.as_view()),
    path('employees/employeeDetails/<int:pk>/',views.EmployeeDetails.as_view()),
    # path('employees/<int:pk>/',views.EmployeesDetails.as_view()),
    path('employees1/',views.EmployeeGeneric.as_view()),
    path('employeeDetails/<int:pk>',views.EmployeeDetailsGenric.as_view()),

    path('CumstomEmployees/',views.CustomEmployee.as_view()),


    # viewset
    path('',include(router.urls)),

    path('blogs/',views.Blog.as_view()),
    path('comments/',views.Comment.as_view()),

    # path('/blogs/<int:pk>/',views.BlogDetails.as_view()),
    # path('/comments/<int:pk>/',views.CommentDetails.as_view()),
    path('users/', generics.ListCreateAPIView.as_view(queryset=Employees.objects.all(), serializer_class=EmployeesSerializer1), name='user-list')
    
]