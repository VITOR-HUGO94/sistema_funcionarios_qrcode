from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
import qrcode
from io import BytesIO
import base64
from django.core.files.base import ContentFile
import os
class Employee(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Nome')
    last_name = models.CharField(max_length=100, verbose_name='Sobrenome')
    email = models.EmailField(unique=True, verbose_name='E-mail')
    department = models.CharField(max_length=100, verbose_name='Departamento')
    hire_date = models.DateField(verbose_name='Data de Contratação')
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_absolute_url(self):
        return reverse('employee_detail', args=[self.pk])
    def get_public_url(self):
        """
        URL pública para acesso via QR code (sem autenticação)
        """
        return reverse('public_employee_detail', args=[self.pk])


    def generate_qr_code(self):
        """
        Retorna o QR Code em base64 para exibir diretamente na página
        """
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        public_url = self.get_public_url()
        qr.add_data(f"https://sistema-funcionarios-qrcode.onrender.com{public_url}")
  
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"

class SiteUser(AbstractUser):
    """
    Custom user model for employees
    """
    # Add custom fields here
    employee_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    hire_date = models.DateField(blank=True, null=True)
    
    # If you don't need these fields from AbstractUser, you can set them to blank/null
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    
    def __str__(self):
        return f"{self.employee_id} - {self.username}" if self.employee_id else self.username

    class Meta:
        verbose_name = 'Site User'
        verbose_name_plural = 'Site Users'

def certificate_upload_path(instance, filename):
    """Gera caminho para upload: certificates/employee_id/filename"""
    return f'certificates/employee_{instance.employee.id}/{filename}'

class Certificate(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='certificates')
    file = models.FileField(upload_to=certificate_upload_path, verbose_name='Arquivo')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Certificado {self.id} - {self.employee}"
    
    def file_extension(self):
        """Retorna a extensão do arquivo"""
        name, extension = os.path.splitext(self.file.name)
        return extension.lower()
    
    def is_image(self):
        """Verifica se o arquivo é uma imagem"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        return self.file_extension() in image_extensions
    
    def is_pdf(self):
        """Verifica se o arquivo é PDF"""
        return self.file_extension() == '.pdf'
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'