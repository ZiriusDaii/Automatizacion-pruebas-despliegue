from django.test import TestCase
from api.usuarios.models import Usuario
from api.roles.models import Rol


class UsuarioTest(TestCase):

    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.rol = Rol.objects.create(
            nombre="Administrador",
            estado="activo"
        )

    def test_creacion_usuario(self):
        """Test para crear un usuario básico"""
        usuario = Usuario.objects.create_user(
            correo_electronico="ziriusdai@gmail.com",
            password="samuel123",
            nombre="samuel",
            tipo_documento="CC",
            documento="123456789",
            celular="3160526457",
            rol=self.rol
        )
        self.assertEqual(usuario.correo_electronico, "ziriusdai@gmail.com")
        self.assertTrue(usuario.check_password("samuel123"))
        self.assertEqual(usuario.nombre, "samuel")
        self.assertEqual(usuario.tipo_documento, "CC")
        self.assertEqual(usuario.documento, "123456789")
        self.assertEqual(usuario.celular, "3160526457")
