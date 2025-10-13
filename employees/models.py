from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
import qrcode
from io import BytesIO
import base64
from django.core.files.base import ContentFile

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
    
    def generate_qr_code(self):
        """
        Retorna o QR Code em base64 para exibir diretamente na página
        """
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        url = self.get_absolute_url()  # URL relativa
        qr.add_data(f"https://sistema-funcionarios-qrcode.onrender.com{url}")  # pode mudar domínio em produção
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
