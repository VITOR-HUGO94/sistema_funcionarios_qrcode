from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Employee,Certificate
import os

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['file']  # Apenas o campo file
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Valida o tamanho do arquivo (10MB máximo)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("O arquivo não pode ser maior que 10MB.")
            
            # Valida as extensões permitidas
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.webp']
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError("Apenas imagens (JPG, PNG, GIF, WEBP) e PDFs são permitidos.")
        
        return file

class SiteLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuário ou E-mail'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Senha'
        })
    )

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'department', 'hire_date']
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
        }
