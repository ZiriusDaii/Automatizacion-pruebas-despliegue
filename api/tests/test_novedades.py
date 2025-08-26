from datetime import date, timedelta, time
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from api.manicuristas.models import Manicurista
from api.novedades.models import Novedad


class NovedadTest(TestCase):

    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.manicurista = Manicurista.objects.create(
            nombre="Ana Pérez",
            tipo_documento="CC",
            numero_documento="123456789",
            celular="3001234567",
            correo="ana@gmail.com"
        )
        self.hoy = timezone.now().date()
        self.manana = self.hoy + timedelta(days=1)

    def test_creacion_novedad_valida(self):
        """Test para crear una novedad válida"""
        novedad = Novedad.objects.create(
            manicurista=self.manicurista,
            fecha=self.manana,
            estado='ausente',
            tipo_ausencia='completa'
        )
        self.assertEqual(novedad.estado, 'ausente')
        self.assertEqual(novedad.tipo_ausencia, 'completa')
        self.assertEqual(novedad.fecha, self.manana)
        self.assertIsNone(novedad.hora_entrada)
        self.assertIsNone(novedad.hora_inicio_ausencia)
        self.assertIsNone(novedad.hora_fin_ausencia)
