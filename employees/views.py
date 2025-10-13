from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Employee, SiteUser
from .forms import EmployeeForm, SiteLoginForm

def site_login(request):
    """Login específico para o sistema do site"""
    if request.user.is_authenticated:
        return redirect('employee_list')
    
    if request.method == 'POST':
        form = SiteLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo ao sistema, {user.username}!')
                return redirect('employee_list')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = SiteLoginForm()
    
    return render(request, 'site_login.html', {'form': form})

def site_logout(request):
    """Logout do sistema do site"""
    logout(request)
    messages.info(request, 'Você foi desconectado do sistema.')
    return redirect('site_login')

def home_view(request):
    """Página inicial que redireciona para o login apropriado"""
    return render(request, 'home.html')

# ✅ NOVA VIEW PÚBLICA PARA QR CODE
def public_employee_detail(request, pk):
    """
    View pública para acesso via QR code - não requer autenticação
    """
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/public_employee_detail.html', {
        'employee': employee
    })

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})

@login_required
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário cadastrado com sucesso!')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form})

@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})

@login_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário atualizado com sucesso!')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form})

@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Funcionário excluído com sucesso!')
        return redirect('employee_list')
    return render(request, 'employees/employee_delete.html', {'employee': employee})
