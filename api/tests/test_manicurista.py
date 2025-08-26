from django.test import TestCase
from api.roles.models import Rol
from api.manicuristas.models import Manicurista


class ManicuristaTest(TestCase):

    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.rol = Rol.objects.create(
            nombre="Manicurista",
            estado="activo"
        )

    def test_creacion_manicurista(self):
        """Test para crear una manicurista básica"""
        manicurista = Manicurista.objects.create(
            nombre="Ana María Pérez",
            tipo_documento="CC",
            numero_documento="123456789",
            especialidad="Manicure Clásica",
            celular="12345678901",
            correo="ana@gmail.com",
            estado="activo"
        )
        self.assertEqual(manicurista.nombre, "Ana María Pérez")
        self.assertEqual(manicurista.especialidad, "Manicure Clásica")
        self.assertEqual(manicurista.estado, "activo")
        self.assertTrue(manicurista.disponible)

    def test_propiedades_nombres_apellidos(self):
        """Test para verificar las propiedades de nombres y apellidos"""
        manicurista = Manicurista.objects.create(
            nombre="Ana María Pérez",
            tipo_documento="CC",
            numero_documento="111222333",
            celular="3001112222",
            correo="test@gmail.com"
        )
        self.assertEqual(manicurista.nombres, "Ana")
        self.assertEqual(manicurista.apellidos, "María Pérez")

        manicurista.nombre = "Ana"
        manicurista.save()
        self.assertEqual(manicurista.nombres, "Ana")
        self.assertEqual(manicurista.apellidos, "")

    def test_contraseña_temporal_y_cambio(self):
        """Test para generar y cambiar contraseña temporal"""
        manicurista = Manicurista.objects.create(
            nombre="Carlos López",
            tipo_documento="CC",
            numero_documento="444555666",
            celular="3004445555",
            correo="carlos@gmail.com"
        )
        contraseña_temp = manicurista.generar_contraseña_temporal()
        self.assertTrue(manicurista.debe_cambiar_contraseña)
        self.assertTrue(manicurista.verificar_contraseña_temporal(contraseña_temp))
        self.assertFalse(manicurista.verificar_contraseña_temporal("clave_incorrecta"))

        manicurista.cambiar_contraseña("nueva_clave123")
        self.assertFalse(manicurista.debe_cambiar_contraseña)
        self.assertTrue(manicurista.verificar_contraseña_temporal("nueva_clave123"))
