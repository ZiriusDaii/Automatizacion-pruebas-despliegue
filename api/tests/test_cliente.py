from django.test import TestCase
from api.roles.models import Rol
from api.clientes.models import Cliente


class ClienteTest(TestCase):

    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.rol = Rol.objects.create(
            nombre="Cliente",
            estado="activo"
        )

    def test_creacion_cliente(self):
        """Test para crear un cliente básico"""
        cliente = Cliente.objects.create(
            tipo_documento="CC",
            documento="123456789",
            nombre="Juan Pérez",
            celular="3160526457",
            correo_electronico="juan@gmail.com",
            direccion="Calle Falsa 123",
            estado=True,
            genero="M"
        )
        self.assertEqual(cliente.nombre, "Juan Pérez")
        self.assertEqual(cliente.documento, "123456789")
        self.assertEqual(cliente.genero, "M")
        self.assertTrue(cliente.estado)

    def test_generar_verificar_contraseña_temporal(self):
        """Test para generar y verificar contraseña temporal"""
        cliente = Cliente.objects.create(
            nombre="Adriana López",
            tipo_documento="CC",
            documento="987654321",
            celular="3001234567",
            correo_electronico="adriana@gmail.com"
        )
        contraseña_temp = cliente.generar_contraseña_temporal()
        self.assertTrue(cliente.debe_cambiar_contraseña)
        self.assertTrue(cliente.verificar_contraseña_temporal(contraseña_temp))
        self.assertFalse(cliente.verificar_contraseña_temporal("contraseña_incorrecta"))

    def test_cambiar_contraseña(self):
        """Test para cambiar contraseña"""
        cliente = Cliente.objects.create(
            nombre="Luis Gómez",
            tipo_documento="CC",
            documento="555666777",
            celular="3009876543",
            correo_electronico="luis@gmail.com"
        )
        cliente.generar_contraseña_temporal()
        cliente.cambiar_contraseña("nueva_clave456")
        self.assertFalse(cliente.debe_cambiar_contraseña)
        self.assertTrue(cliente.verificar_contraseña_temporal("nueva_clave456"))
