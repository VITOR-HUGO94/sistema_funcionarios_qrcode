from django.contrib import admin
from .models import Employee
from django.contrib.auth.admin import UserAdmin
from .models import SiteUser

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'department', 'hire_date')
    list_filter = ('department',)
    search_fields = ('first_name', 'last_name', 'email')
@admin.register(SiteUser)
class SiteUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'employee_id', 'department', 'is_staff')
    list_filter = ('department', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Employee Information', {
            'fields': ('employee_id', 'department', 'phone_number', 'hire_date')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Employee Information', {
            'fields': ('employee_id', 'department', 'phone_number', 'hire_date', 'email')
        }),
    )
