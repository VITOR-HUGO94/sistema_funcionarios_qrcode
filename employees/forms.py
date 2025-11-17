from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Employee,Certificate
import os

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['file', 'description']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'accept': '.pdf,image/*'})
        }

    def clean_file(self):
        f = self.cleaned_data.get('file')
        if f and f.size > 10 * 1024 * 1024:  # 10 MB
            raise forms.ValidationError('Arquivo muito grande (máx. 10MB).')
        return f

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
