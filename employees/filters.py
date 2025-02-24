import django_filters
from .models import Employee


class EmployeeFilter(django_filters.FilterSet):
    designation = django_filters.CharFilter(field_name='emp_designation',lookup_expr='iexact')
    Name = django_filters.CharFilter(field_name = 'emp_name',lookup_expr='icontains')
    # id = django_filters.RangeFilter(field_name = 'id')
    id_min = django_filters.CharFilter(method='filter_by_emp_id',label='From Emp Id')
    id_max = django_filters.CharFilter(method='filter_by_emp_id',label='TO EMP ID')

    class Meta:
        model = Employee
        fields = ['designation','Name','id_min','id_max']

    def filter_by_emp_id(self,queryset, name, value):
        if name == 'id_min':
            return queryset.filter(emp_id__gte=value)
        elif name == 'id_max':
            return queryset.filter(emp_id__lte=value)
        return queryset    