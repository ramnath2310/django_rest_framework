from django.db import models

# Create your models here.
class Employee(models.Model):
    emp_id = models.CharField(max_length=20)
    emp_name  = models.CharField(max_length=50)
    emp_designation = models.CharField(max_length=50)

    def __str__(self):
        return self.emp_name
class Employees(models.Model):
    emp_id = models.CharField(max_length=20)
    first_name  = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    emp_deg = models.CharField(max_length=50)
    emp_salary  = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"    