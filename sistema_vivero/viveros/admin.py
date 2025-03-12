from django.contrib import admin
from .models import (
    Productor, Finca, Vivero, Labor,
    ProductoControlHongo, ProductoControlPlaga, ProductoControlFertilizante
)

@admin.register(Productor)
class ProductorAdmin(admin.ModelAdmin):
    list_display = ('documento_identidad', 'nombre', 'apellido', 'telefono', 'correo')
    search_fields = ('documento_identidad', 'nombre', 'apellido')

@admin.register(Finca)
class FincaAdmin(admin.ModelAdmin):
    list_display = ('numero_catastro', 'municipio', 'productor')
    list_filter = ('municipio',)
    search_fields = ('numero_catastro', 'municipio')

@admin.register(Vivero)
class ViveroAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'tipo_cultivo', 'get_finca', 'get_productor')
    list_filter = ('tipo_cultivo', 'finca__municipio')
    search_fields = ('codigo', 'tipo_cultivo')
    
    def get_finca(self, obj):
        return obj.finca.numero_catastro
    get_finca.short_description = 'Finca'
    
    def get_productor(self, obj):
        return f"{obj.finca.productor.nombre} {obj.finca.productor.apellido}"
    get_productor.short_description = 'Productor'

@admin.register(Labor)
class LaborAdmin(admin.ModelAdmin):
    list_display = ('vivero', 'fecha', 'descripcion')
    list_filter = ('fecha', 'vivero__tipo_cultivo')
    date_hierarchy = 'fecha'

@admin.register(ProductoControlHongo)
class ProductoControlHongoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'registro_ica', 'frecuencia_aplicacion', 'valor', 'periodo_carencia', 'nombre_hongo')
    list_filter = ('nombre_hongo', 'periodo_carencia')
    search_fields = ('nombre', 'registro_ica', 'nombre_hongo')

@admin.register(ProductoControlPlaga)
class ProductoControlPlagaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'registro_ica', 'frecuencia_aplicacion', 'valor', 'periodo_carencia')
    list_filter = ('periodo_carencia',)
    search_fields = ('nombre', 'registro_ica')

@admin.register(ProductoControlFertilizante)
class ProductoControlFertilizanteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'registro_ica', 'frecuencia_aplicacion', 'valor', 'fecha_ultima_aplicacion')
    list_filter = ('fecha_ultima_aplicacion',)
    search_fields = ('nombre', 'registro_ica')
    date_hierarchy = 'fecha_ultima_aplicacion'