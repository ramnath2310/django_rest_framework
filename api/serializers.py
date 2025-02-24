from rest_framework import serializers
from students.models import Student
from employees.models import Employee,Employees


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Student
        fields = '__all__'
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

# Custom serializers
class EmployeesSerializer1(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    is_high_earner = serializers.SerializerMethodField()
    

    class Meta:
        model = Employees
        fields = ['emp_id', 'first_name','last_name','full_name','emp_deg','emp_salary','is_high_earner','is_active']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"    
    
    def validate_emp_salary(self, value):
        if value < 0:
            raise serializers.ValidationError("Salary must be a positive number")
        return value
    
    def get_is_high_earner(self, obj):
        return obj.emp_salary > 100000

  
