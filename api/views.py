from django.shortcuts import render,get_object_or_404
# from django.http import JsonResponse,HttpResponse
from students.models import Student
from rest_framework.response import Response
from .serializers import StudentSerializer,EmployeeSerializer,EmployeesSerializer1
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from employees.models import Employee,Employees
from django.http import Http404
from rest_framework import mixins,generics,viewsets
from blogs.models import Blog,Comment
from blogs.serializers import BlogSerializer,CommentSerializer
from .pagination import CustomPagination
from employees.filters import EmployeeFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

# Create your views here.
@api_view(['GET','POST'])
def students_api(request):
    if request.method == 'GET':
        # get all the data from the student table
        student=Student.objects.all()
        serializer=StudentSerializer(student,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Manual serialization
    # student_list=list(student.values())


# GET method using Primary key
@api_view(["GET","PUT","DELETE"])
def studentDetailsView(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'GET':
            serializer = StudentSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
         serializer = StudentSerializer(student, data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_200_OK)
         else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
         student.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)     

class Employeesclass(APIView):
     def get(self, request):
          employees = Employee.objects.all()
          serializer = EmployeeSerializer(employees, many=True)
          return Response(serializer.data)
     def post(self,request):
          serializer = EmployeeSerializer(data=request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
# class EmployeesDetails(APIView):
#      def get_object(self, pk):
#           try:
#                return Employee.objects.get(pk=pk)
#           except Employee.DoesNotExist:
#                raise Http404
#      def get(self,requset,pk):
#           employee = self.get_object(pk)
#           serializer = EmployeeSerializer(employee)
#           return Response(serializer.data,status=status.HTTP_200_OK)
#      def put(self,requset,pk):
#           employee = self.get_object(pk)
#           serializer = EmployeeSerializer(employee,data=requset.data)
#           if serializer.is_valid():
#                serializer.save()
#                return Response(serializer.data,status=status.HTTP_200_OK)
#           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#      def delete(self , request , pk):
#           employee = self.get_object(pk)
#           employee.delete()
#           return Response(status=status.HTTP_204_NO_CONTENT)
class EmployeeMixin(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
     queryset = Employee.objects.all()
     serializer_class = EmployeeSerializer

     def get(self,request):
          return self.list(request)
     def post(self,request):
          return self.create(request)
     
class EmployeeDetails(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
     queryset = Employee.objects.all()
     serializer_class = EmployeeSerializer

     def get(self,request,pk):
          return self.retrieve(request,pk)
     def put(self,request,pk):
          return self.update(request,pk)
     def delete(self,request,pk):
          return self.destroy(request,pk)
     
# Generic APIView Example
class EmployeeGeneric(generics.ListAPIView,generics.CreateAPIView):
     queryset = Employee.objects.all()
     serializer_class = EmployeeSerializer 


class EmployeeDetailsGenric(generics.RetrieveUpdateDestroyAPIView):
     queryset = Employee.objects.all()
     serializer_class = EmployeeSerializer
     lookup_field = 'pk'  # this is for primary key


# # Viewsets
# class EmployeeViewSet(viewsets.ViewSet):
   
#      def list(self, request):
#             queryset = Employee.objects.all()
#             serializer = EmployeeSerializer(queryset,many=True)
#             return Response(serializer.data)
#      def create(self, request):
#           serializer = EmployeeSerializer(data=request.data)
#           if serializer.is_valid():
#               serializer.save()
#               return Response(serializer.data, status=status.HTTP_201_CREATED)
#           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#      def retrieve(self,request,pk=None):
#           employee = get_object_or_404(Employee,pk=pk)
#           serializer = EmployeeSerializer(employee)
#           return Response(serializer.data,status=status.HTTP_200_OK)

#      def update(self,request,pk=None):
#         employee = get_object_or_404(Employee, pk=pk)
#         serializer = EmployeeSerializer(employee, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
#      def destroy(self, request, pk=None):
#           employee = get_object_or_404(Employee, pk=pk)
#           employee.delete()
#           return Response(status=status.HTTP_204_NO_CONTENT)      


# ModelViewSets
class EmployeeViewSet(viewsets.ModelViewSet):
     queryset = Employee.objects.all()
     serializer_class = EmployeeSerializer
     pagination_class = CustomPagination 
     # global filtering
     # filterset_fields = ['emp_designation']

     # custom filtering
     filterset_class = EmployeeFilter
     filter_backends = [DjangoFilterBackend,SearchFilter]
     search_fields = ['emp_name']

     @action(detail =False,methods = ['GET'],name='Get all active employees')
     def active(self, request):
        active_employees = Employees.objects.filter(is_active=True)
        serializer =EmployeesSerializer1(active_employees, many=True)
        return Response(serializer.data)



class Blog(generics.ListCreateAPIView):
     queryset = Blog.objects.all()
     serializer_class = BlogSerializer
     filter_backends = [SearchFilter,OrderingFilter]
     search_fields = ['blog_title','blog_body']
     ordering_fields = ['id']

class Comment(generics.ListCreateAPIView):
     queryset = Comment.objects.all()
     serializer_class = CommentSerializer


# class BlogDetails(generics.RetrieveUpdateDestroyAPIView):
#      queryset = Blog.objects.all()
#      serializer_class = BlogSerializer
#      lookup_field = 'pk'  # this is for primary key


# class CommentDetails(generics.RetrieveUpdateDestroyAPIView):
#      queryset = Comment.objects.all()
#      serializer_class = CommentSerializer
#      lookup_field = 'pk'  # this is for primary key
    
class CustomEmployee(APIView):
     
     def get(self , request):
          employees = Employees.objects.all()
          serializer = EmployeesSerializer1(employees,many = True)
          return Response(serializer.data)
     def post(self , request):
          serializer = EmployeesSerializer1(data = request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status = status.HTTP_201_CREATED)
          return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
class ListCreateAPIView(generics.ListCreateAPIView):
     def list(self, request):
          # queryset = self.get_queryset()
          # serializer = EmployeesSerializer1(queryset, many=True)
          return Response(data)
     def create(self, request):
          serializer = EmployeesSerializer1(data=request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)