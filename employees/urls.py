from django.urls import path
from . import views



urlpatterns = [
    # Página inicial (login)
    path('', views.home_view, name='home'),
    
    # URLs públicas (acesso via QR code)
    path('public/employee/<int:pk>/', views.public_employee_detail, name='public_employee_detail'),

    # Logout
    path('login/', views.site_login, name='site_login'),
    path('logout/', views.site_logout, name='site_logout'),
    # CRUD protegido
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/new/', views.employee_create, name='employee_create'),
    path('employees/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employees/<int:pk>/edit/', views.employee_update, name='employee_update'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
]