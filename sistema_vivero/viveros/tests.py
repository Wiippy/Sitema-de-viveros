from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from .models import (
    Productor, Finca, Vivero, Labor,
    ProductoControlHongo, ProductoControlPlaga, ProductoControlFertilizante
)

class ProductorTests(TestCase):
    def setUp(self):
        self.productor = Productor.objects.create(
            documento_identidad="1234567890",
            nombre="Juan",
            apellido="Pérez",
            telefono="+573001234567",
            correo="juan.perez@example.com"
        )
    
    def test_creacion_productor(self):
        """Prueba la creación correcta de un productor"""
        self.assertEqual(self.productor.nombre, "Juan")
        self.assertEqual(self.productor.apellido, "Pérez")
        self.assertEqual(self.productor.documento_identidad, "1234567890")
    
    def test_documento_identidad_unico(self):
        """Prueba que no se pueden crear dos productores con el mismo documento de identidad"""
        with self.assertRaises(IntegrityError):
            Productor.objects.create(
                documento_identidad="1234567890",  # Mismo documento que el de setUp
                nombre="Pedro",
                apellido="Gómez",
                telefono="+573009876543",
                correo="pedro.gomez@example.com"
            )
    
    def test_email_invalido(self):
        """Prueba que no se puede crear un productor con un email inválido"""
        productor_invalido = Productor(
            documento_identidad="9876543210",
            nombre="María",
            apellido="López",
            telefono="+573001234567",
            correo="correo_invalido"  # Email inválido
        )
        with self.assertRaises(ValidationError):
            productor_invalido.full_clean()

class FincaTests(TestCase):
    def setUp(self):
        self.productor = Productor.objects.create(
            documento_identidad="1234567890",
            nombre="Juan",
            apellido="Pérez",
            telefono="+573001234567",
            correo="juan.perez@example.com"
        )
        self.finca = Finca.objects.create(
            productor=self.productor,
            numero_catastro="CAT-12345",
            municipio="Medellín"
        )
    
    def test_creacion_finca(self):
        """Prueba la creación correcta de una finca"""
        self.assertEqual(self.finca.numero_catastro, "CAT-12345")
        self.assertEqual(self.finca.municipio, "Medellín")
        self.assertEqual(self.finca.productor, self.productor)
    
    def test_numero_catastro_unico(self):
        """Prueba que no se pueden crear dos fincas con el mismo número de catastro"""
        with self.assertRaises(IntegrityError):
            Finca.objects.create(
                productor=self.productor,
                numero_catastro="CAT-12345",  # Mismo número de catastro
                municipio="Bogotá"
            )
    
    def test_relacion_productor_finca(self):
        """Prueba la relación entre productor y finca"""
        # Verificar que la finca está relacionada correctamente con el productor
        self.assertEqual(self.productor.fincas.count(), 1)
        self.assertEqual(self.productor.fincas.first(), self.finca)

class ViveroTests(TestCase):
    def setUp(self):
        self.productor = Productor.objects.create(
            documento_identidad="1234567890",
            nombre="Juan",
            apellido="Pérez",
            telefono="+573001234567",
            correo="juan.perez@example.com"
        )
        self.finca = Finca.objects.create(
            productor=self.productor,
            numero_catastro="CAT-12345",
            municipio="Medellín"
        )
        self.vivero = Vivero.objects.create(
            finca=self.finca,
            codigo="VIV-001",
            tipo_cultivo="Café"
        )
    
    def test_creacion_vivero(self):
        """Prueba la creación correcta de un vivero"""
        self.assertEqual(self.vivero.codigo, "VIV-001")
        self.assertEqual(self.vivero.tipo_cultivo, "Café")
        self.assertEqual(self.vivero.finca, self.finca)
    
    def test_codigo_unico_por_finca(self):
        """Prueba que no se pueden crear dos viveros con el mismo código en la misma finca"""
        with self.assertRaises(IntegrityError):
            Vivero.objects.create(
                finca=self.finca,
                codigo="VIV-001",  # Mismo código en la misma finca
                tipo_cultivo="Cacao"
            )
    
    def test_multiples_viveros_por_finca(self):
        """Prueba que una finca puede tener múltiples viveros"""
        Vivero.objects.create(
            finca=self.finca,
            codigo="VIV-002",
            tipo_cultivo="Cacao"
        )
        self.assertEqual(self.finca.viveros.count(), 2)

class LaborTests(TestCase):
    def setUp(self):
        self.productor = Productor.objects.create(
            documento_identidad="1234567890",
            nombre="Juan",
            apellido="Pérez",
            telefono="+573001234567",
            correo="juan.perez@example.com"
        )
        self.finca = Finca.objects.create(
            productor=self.productor,
            numero_catastro="CAT-12345",
            municipio="Medellín"
        )
        self.vivero = Vivero.objects.create(
            finca=self.finca,
            codigo="VIV-001",
            tipo_cultivo="Café"
        )
        self.labor = Labor.objects.create(
            vivero=self.vivero,
            fecha=date.today(),
            descripcion="Fertilización general"
        )
    
    def test_creacion_labor(self):
        """Prueba la creación correcta de una labor"""
        self.assertEqual(self.labor.vivero, self.vivero)
        self.assertEqual(self.labor.fecha, date.today())
        self.assertEqual(self.labor.descripcion, "Fertilización general")
    
    def test_relacion_vivero_labor(self):
        """Prueba la relación entre vivero y labor"""
        self.assertEqual(self.vivero.labores.count(), 1)
        self.assertEqual(self.vivero.labores.first(), self.labor)
    
    def test_multiples_labores_por_vivero(self):
        """Prueba que un vivero puede tener múltiples labores"""
        Labor.objects.create(
            vivero=self.vivero,
            fecha=date.today() - timedelta(days=7),
            descripcion="Fumigación preventiva"
        )
        self.assertEqual(self.vivero.labores.count(), 2)

class ProductoControlTests(TestCase):
    def setUp(self):
        self.productor = Productor.objects.create(
            documento_identidad="1234567890",
            nombre="Juan",
            apellido="Pérez",
            telefono="+573001234567",
            correo="juan.perez@example.com"
        )
        self.finca = Finca.objects.create(
            productor=self.productor,
            numero_catastro="CAT-12345",
            municipio="Medellín"
        )
        self.vivero = Vivero.objects.create(
            finca=self.finca,
            codigo="VIV-001",
            tipo_cultivo="Café"
        )
        self.labor = Labor.objects.create(
            vivero=self.vivero,
            fecha=date.today(),
            descripcion="Aplicación de productos"
        )
        
        # Crear productos de control
        self.producto_hongo = ProductoControlHongo.objects.create(
            registro_ica="ICA-H-12345",
            nombre="Fungicida XYZ",
            frecuencia_aplicacion=15,
            valor=75000.00,
            periodo_carencia=10,
            nombre_hongo="Roya",
            labor=self.labor
        )
        
        self.producto_plaga = ProductoControlPlaga.objects.create(
            registro_ica="ICA-P-54321",
            nombre="Insecticida ABC",
            frecuencia_aplicacion=30,
            valor=85000.00,
            periodo_carencia=15,
            labor=self.labor
        )
        
        self.producto_fertilizante = ProductoControlFertilizante.objects.create(
            registro_ica="ICA-F-98765",
            nombre="Fertilizante NPK",
            frecuencia_aplicacion=60,
            valor=120000.00,
            fecha_ultima_aplicacion=date.today() - timedelta(days=30),
            labor=self.labor
        )
    
    def test_creacion_producto_hongo(self):
        """Prueba la creación correcta de un producto de control de hongos"""
        self.assertEqual(self.producto_hongo.nombre, "Fungicida XYZ")
        self.assertEqual(self.producto_hongo.registro_ica, "ICA-H-12345")
        self.assertEqual(self.producto_hongo.nombre_hongo, "Roya")
        self.assertEqual(self.producto_hongo.periodo_carencia, 10)
    
    def test_creacion_producto_plaga(self):
        """Prueba la creación correcta de un producto de control de plagas"""
        self.assertEqual(self.producto_plaga.nombre, "Insecticida ABC")
        self.assertEqual(self.producto_plaga.registro_ica, "ICA-P-54321")
        self.assertEqual(self.producto_plaga.periodo_carencia, 15)
    
    def test_creacion_producto_fertilizante(self):
        """Prueba la creación correcta de un producto de control de fertilizantes"""
        self.assertEqual(self.producto_fertilizante.nombre, "Fertilizante NPK")
        self.assertEqual(self.producto_fertilizante.registro_ica, "ICA-F-98765")
        self.assertEqual(self.producto_fertilizante.fecha_ultima_aplicacion, date.today() - timedelta(days=30))
    
    def test_relacion_labor_productos(self):
        """Prueba la relación entre labor y productos de control"""
        self.assertEqual(self.labor.productos_control_hongo.count(), 1)
        self.assertEqual(self.labor.productos_control_plaga.count(), 1)
        self.assertEqual(self.labor.productos_control_fertilizante.count(), 1)
        
        self.assertEqual(self.labor.productos_control_hongo.first(), self.producto_hongo)
        self.assertEqual(self.labor.productos_control_plaga.first(), self.producto_plaga)
        self.assertEqual(self.labor.productos_control_fertilizante.first(), self.producto_fertilizante)