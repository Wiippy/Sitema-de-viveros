from django.db import models
from django.core.validators import MinValueValidator, EmailValidator, RegexValidator

class Productor(models.Model):
    documento_identidad = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El número de teléfono debe estar en formato: '+999999999'. Hasta 15 dígitos permitidos.")]
    )
    correo = models.EmailField(validators=[EmailValidator(message="Ingrese un correo electrónico válido.")])

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.documento_identidad})"

    class Meta:
        verbose_name_plural = "Productores"

class Finca(models.Model):
    productor = models.ForeignKey(Productor, on_delete=models.CASCADE, related_name='fincas')
    numero_catastro = models.CharField(max_length=50, unique=True)
    municipio = models.CharField(max_length=100)

    def __str__(self):
        return f"Finca {self.numero_catastro} - {self.municipio}"

class Vivero(models.Model):
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE, related_name='viveros')
    codigo = models.CharField(max_length=50)
    tipo_cultivo = models.CharField(max_length=100)

    def __str__(self):
        return f"Vivero {self.codigo} - {self.tipo_cultivo}"

    class Meta:
        unique_together = ['finca', 'codigo']

class Labor(models.Model):
    vivero = models.ForeignKey(Vivero, on_delete=models.CASCADE, related_name='labores')
    fecha = models.DateField()
    descripcion = models.TextField()
    
    def __str__(self):
        return f"Labor en {self.vivero} - {self.fecha}"

class ProductoControl(models.Model):
    registro_ica = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    frecuencia_aplicacion = models.PositiveIntegerField(help_text="Frecuencia en días")
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    class Meta:
        abstract = True
        
    def __str__(self):
        return f"{self.nombre} (ICA: {self.registro_ica})"

class ProductoControlHongo(ProductoControl):
    periodo_carencia = models.PositiveIntegerField(help_text="Período de carencia en días")
    nombre_hongo = models.CharField(max_length=100)
    labor = models.ForeignKey(Labor, on_delete=models.CASCADE, related_name='productos_control_hongo')

    def __str__(self):
        return f"{super().__str__()} - Control de Hongo: {self.nombre_hongo}"

class ProductoControlPlaga(ProductoControl):
    periodo_carencia = models.PositiveIntegerField(help_text="Período de carencia en días")
    labor = models.ForeignKey(Labor, on_delete=models.CASCADE, related_name='productos_control_plaga')

    def __str__(self):
        return f"{super().__str__()} - Control de Plaga"

class ProductoControlFertilizante(ProductoControl):
    fecha_ultima_aplicacion = models.DateField()
    labor = models.ForeignKey(Labor, on_delete=models.CASCADE, related_name='productos_control_fertilizante')

    def __str__(self):
        return f"{super().__str__()} - Fertilizante (Última aplicación: {self.fecha_ultima_aplicacion})"