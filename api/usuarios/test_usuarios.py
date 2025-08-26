from django.test import TestCase
from api.usuarios.models import Usuario
from api.roles.models import Rol


class UsuarioModelTest(TestCase):
    """Tests para el modelo Usuario"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        # Crear un rol de prueba
        self.rol = Rol.objects.create(
            nombre='Cliente',
            estado='activo'
        )
        
        # Datos de usuario de prueba
        self.usuario_data = {
            'nombre': 'Juan Pérez',
            'tipo_documento': 'CC',
            'documento': '12345678',
            'celular': '3001234567',
            'correo_electronico': 'juan@example.com',
            'rol': self.rol,
            'is_active': True
        }
    
    def test_crear_usuario_basico(self):
        """Test para crear un usuario básico"""
        usuario = Usuario.objects.create_user(
            correo_electronico=self.usuario_data['correo_electronico'],
            password='testpass123',
            **{k: v for k, v in self.usuario_data.items() if k != 'correo_electronico'}
        )
        
        self.assertEqual(usuario.nombre, 'Juan Pérez')
        self.assertEqual(usuario.correo_electronico, 'juan@example.com')
        self.assertEqual(usuario.tipo_documento, 'CC')
        self.assertEqual(usuario.documento, '12345678')
        self.assertTrue(usuario.is_active)
        self.assertFalse(usuario.is_staff)
        self.assertFalse(usuario.is_superuser)
    
    def test_crear_superusuario(self):
        """Test para crear un superusuario"""
        superuser = Usuario.objects.create_superuser(
            correo_electronico='admin@example.com',
            password='adminpass123',
            **{k: v for k, v in self.usuario_data.items() if k != 'correo_electronico'}
        )
        
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)



