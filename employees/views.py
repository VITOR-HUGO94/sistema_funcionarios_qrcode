from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging

from employees.utils import extract_date_from_pdf
from .models import Certificate, Employee, SiteUser
from .forms import EmployeeForm, SiteLoginForm, CertificateForm  # Adicione CertificateForm aqui
from django.forms import modelformset_factory

# Remova a linha do CertificateFormSet daqui

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

def public_employee_detail(request, pk):
    """
    View pública para acesso via QR code - não requer autenticação
    MOSTRA APENAS CERTIFICADOS QUE SÃO IMAGENS
    """
    employee = get_object_or_404(Employee, pk=pk)
    
    # Envia todos os certificados (imagens + pdfs). Se quiser só imagens:
    # certificates = [ cert for cert in employee.certificates.all() if cert.is_image ]
    certificates = employee.certificates.all()
    
    return render(request, 'employees/public_employee_detail.html', {
        'employee': employee,
        'certificates': certificates
    })

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})

@login_required
def employee_create(request):
    CertificateFormSet = modelformset_factory(Certificate, form=CertificateForm, extra=1, can_delete=True)
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        formset = CertificateFormSet(request.POST, request.FILES, queryset=Certificate.objects.none())
        if form.is_valid() and formset.is_valid():
            employee = form.save()
            for form in formset:
                if form.cleaned_data.get('file'):
                    certificate = form.save(commit=False)
                    certificate.employee = employee
                    certificate.save()
            messages.success(request, 'Funcionário cadastrado com sucesso!')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
        formset = CertificateFormSet(queryset=Certificate.objects.none())
    return render(request, 'employees/employee_form.html', {'form': form, 'formset': formset})

@login_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    CertificateFormSet = modelformset_factory(Certificate, form=CertificateForm, extra=1, can_delete=True)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        formset = CertificateFormSet(request.POST, request.FILES, queryset=Certificate.objects.filter(employee=employee))
        if form.is_valid() and formset.is_valid():
            form.save()
            certificates = formset.save(commit=False)
            for certificate in certificates:
                certificate.employee = employee
                certificate.save()
            for form in formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()
            messages.success(request, 'Funcionário atualizado com sucesso!')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
        formset = CertificateFormSet(queryset=Certificate.objects.filter(employee=employee))
    return render(request, 'employees/employee_form.html', {'form': form, 'formset': formset})

@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Funcionário excluído com sucesso!')
        return redirect('employee_list')
    return render(request, 'employees/employee_delete.html', {'employee': employee})

@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    certificates = employee.certificates.all()
    certificate_form = CertificateForm()
    return render(request, 'employees/employee_detail.html', {
        'employee': employee,
        'certificates': certificates,
        'certificate_form': certificate_form
    })
logger = logging.getLogger(__name__)

@login_required
def add_certificate(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method != 'POST':
        messages.error(request, 'Método inválido.')
        return redirect('employee_detail', pk=employee.pk)

    # LOG SEGURO: não imprima objetos grandes
    try:
        files_info = []
        for name, uploaded in request.FILES.items():
            # uploaded é UploadedFile — não lemos conteúdo
            size_kb = round(uploaded.size / 1024, 2) if hasattr(uploaded, 'size') else 'unknown'
            files_info.append({'field': name, 'filename': getattr(uploaded, 'name', 'unknown'), 'size_kb': size_kb})
        logger.debug("add_certificate: request.FILES summary = %s", files_info)
    except Exception as e:
        logger.exception("Erro ao inspecionar request.FILES: %s", e)

    form = CertificateForm(request.POST, request.FILES)

    if not request.FILES:
        messages.error(request, 'Nenhum arquivo enviado. Verifique enctype e limites do servidor (nginx, Django).')
        return redirect('employee_detail', pk=employee.pk)

    if form.is_valid():
        certificate = form.save(commit=False)
        certificate.employee = employee
        certificate.save()
        logger.info("Certificado salvo (id=%s) file=%s size=%s", certificate.pk, certificate.file.name,
                    getattr(certificate.file, 'size', 'unknown'))

        # Extração opcional (PDF) — abra o file-like mas não leia tudo ao log
        if certificate.file.name.lower().endswith('.pdf'):
            try:
                certificate.file.open('rb')
                data = extract_date_from_pdf(certificate.file)
                if data:
                    certificate.extracted_date = data
                    certificate.save()
                    messages.info(request, f'Data de emissão detectada: {data}')
            except Exception as e:
                logger.exception("Erro ao extrair data do PDF: %s", e)
                messages.warning(request, 'Não foi possível extrair data do PDF. Veja logs do servidor.')
            finally:
                try:
                    certificate.file.close()
                except:
                    pass

        messages.success(request, 'Certificado adicionado com sucesso!')
        return redirect('employee_detail', pk=employee.pk)

    else:
        logger.warning("Form inválido ao adicionar certificado: %s", form.errors.as_json())
        messages.error(request, 'Formulário inválido. Erros: %s' % form.errors.as_text())
        return redirect('employee_detail', pk=employee.pk)
    
@login_required
def delete_certificate(request, pk):
    """Remove um certificado"""
    certificate = get_object_or_404(Certificate, pk=pk)
    employee_pk = certificate.employee.pk
    
    if request.method == 'POST':
        certificate.delete()
        messages.success(request, 'Certificado removido com sucesso!')
    
    return redirect('employee_detail', pk=employee_pk)