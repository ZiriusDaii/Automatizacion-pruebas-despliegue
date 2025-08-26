# WineSpa API - Backend

Backend API para el sistema de gestión de spa de uñas desarrollado con Django REST Framework.

## 📋 Descripción

Este proyecto es una API REST completa para la gestión de un spa de uñas, incluyendo funcionalidades para:
- Gestión de usuarios y autenticación
- Gestión de clientes
- Gestión de manicuristas
- Gestión de citas y servicios
- Gestión de inventario y compras
- Gestión de novedades y liquidaciones
- Sistema de roles y permisos

## 🚀 Tecnologías Utilizadas

- **Python 3.10**
- **Django 5.2**
- **Django REST Framework**
- **MySQL 8.0**
- **pytest** (para pruebas unitarias)
- **GitHub Actions** (CI/CD)

## 📦 Instalación y Configuración

### Prerrequisitos

- Python 3.10 o superior
- MySQL 8.0
- Git

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd Backend
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos

Crear una base de datos MySQL llamada `winespaapi` y configurar las variables de entorno:

```bash
# Crear archivo .env en la raíz del proyecto
DB_NAME=winespaapi
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=3306
DEBUG=True
SECRET_KEY=tu_clave_secreta
```

### 5. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar el servidor

```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

## 🧪 Configuración de Pruebas

### Instalación de pytest

El proyecto utiliza `pytest` y `pytest-django` para las pruebas unitarias. Estas dependencias ya están incluidas en `requirements.txt`.

### Configuración de pytest

El archivo `pytest.ini` contiene la configuración necesaria:

```ini
[tool:pytest]
DJANGO_SETTINGS_MODULE = winespa.settings
python_files = tests.py test_*.py *_tests.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --strict-config
    --tb=short
    --reuse-db
    --nomigrations
    --disable-warnings
    --color=yes
    -v
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    api: marks tests as API tests
testpaths = api
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
    ignore::UserWarning
```

### Ejecutar pruebas localmente

```bash
# Ejecutar todas las pruebas
python -m pytest api/tests/ -v

# Ejecutar pruebas específicas
python -m pytest api/tests/test_usuarios.py -v

# Ejecutar pruebas con marcadores específicos
python -m pytest -m "unit" -v
```

### Estructura de pruebas

Las pruebas están organizadas en la carpeta `api/tests/`:

```
api/tests/
├── __init__.py
├── test_usuarios.py      # Pruebas del modelo Usuario
├── test_cliente.py       # Pruebas del modelo Cliente
├── test_manicurista.py   # Pruebas del modelo Manicurista
├── test_roles.py         # Pruebas del modelo Rol y Permisos
└── test_novedades.py     # Pruebas del modelo Novedad
```

## 🔄 GitHub Actions - CI/CD

### Configuración Automática

El proyecto incluye un workflow de GitHub Actions que se ejecuta automáticamente en cada push y pull request a la rama `master`.

### Archivo de Workflow

El workflow está configurado en `.github/workflows/test-api.yml`:

```yaml
name: Test API (Python)

on:
  push:
    branches: [ "master" ]
  pull_request:
    branches: [ "master" ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: winespaapi
          MYSQL_USER: wine
          MYSQL_PASSWORD: tech
        ports:
          - 3306:3306
        options: --health-cmd="mysqladmin ping" --health-interval=10s --health-timeout=5s --health-retries=3

    steps:
      - name: Descargar código
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Instalar dependencias
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Verificar configuración Django
        run: |
          python -c "import django; print('Django version:', django.get_version())"
        env:
          DJANGO_SETTINGS_MODULE: winespa.settings
          PYTHONPATH: ${{ github.workspace }}
          DB_NAME: winespaapi
          DB_USER: wine
          DB_PASSWORD: tech
          DB_HOST: 127.0.0.1
          DB_PORT: 3306

      - name: Esperar MySQL
        run: |
          while ! mysqladmin ping -h"127.0.0.1" -P3306 --silent; do
            echo "Esperando MySQL..."
            sleep 2
          done
          echo "MySQL está listo!"

      - name: Configurar permisos de base de datos
        run: |
          mysql -h 127.0.0.1 -P 3306 -u root -proot -e "
          GRANT ALL PRIVILEGES ON *.* TO 'wine'@'%' WITH GRANT OPTION;
          FLUSH PRIVILEGES;
          CREATE DATABASE IF NOT EXISTS test_winespaapi;
          GRANT ALL PRIVILEGES ON test_winespaapi.* TO 'wine'@'%';
          FLUSH PRIVILEGES;"

      - name: Verificar base de datos de prueba
        run: |
          mysql -h 127.0.0.1 -P 3306 -u wine -ptech -e "SHOW DATABASES;"
          echo "Base de datos de prueba configurada correctamente"

      - name: Ejecutar pruebas
        run: |
          python -m pytest api/tests/ -v
        env:
          DJANGO_SETTINGS_MODULE: winespa.settings
          PYTHONPATH: ${{ github.workspace }}
          DEBUG: "True"
          DB_NAME: winespaapi
          DB_USER: wine
          DB_PASSWORD: tech
          DB_HOST: 127.0.0.1
          DB_PORT: 3306
```

### ¿Qué hace el workflow?

1. **Trigger**: Se ejecuta en cada push y pull request a `master`
2. **Entorno**: Ubuntu Latest con Python 3.10
3. **Base de datos**: Configura MySQL 8.0 como servicio
4. **Dependencias**: Instala todas las dependencias de `requirements.txt`
5. **Configuración**: Verifica la configuración de Django
6. **Base de datos**: Configura permisos y crea base de datos de prueba
7. **Pruebas**: Ejecuta todas las pruebas unitarias con pytest

### Verificar el estado de las pruebas

1. Ve a tu repositorio en GitHub
2. Haz clic en la pestaña "Actions"
3. Verás el workflow "Test API (Python)" ejecutándose
4. Haz clic en el workflow para ver los detalles
5. Los logs mostrarán el resultado de cada paso

### Pruebas automatizadas incluidas

El workflow ejecuta automáticamente las siguientes pruebas:

- **test_usuarios.py**: Pruebas del modelo Usuario
  - Creación de usuarios básicos
  - Creación de superusuarios

- **test_cliente.py**: Pruebas del modelo Cliente
  - Creación de clientes
  - Generación y verificación de contraseñas temporales
  - Cambio de contraseñas

- **test_manicurista.py**: Pruebas del modelo Manicurista
  - Creación de manicuristas
  - Propiedades de nombres y apellidos
  - Gestión de contraseñas temporales

- **test_roles.py**: Pruebas del modelo Rol y Permisos
  - Creación de permisos
  - Creación de roles
  - Asignación de permisos a roles

- **test_novedades.py**: Pruebas del modelo Novedad
  - Creación de novedades válidas

## 📁 Estructura del Proyecto

```
Backend/
├── api/                          # Aplicaciones Django
│   ├── usuarios/                 # Gestión de usuarios
│   ├── clientes/                 # Gestión de clientes
│   ├── manicuristas/             # Gestión de manicuristas
│   ├── roles/                    # Sistema de roles y permisos
│   ├── novedades/                # Gestión de novedades
│   ├── citas/                    # Gestión de citas
│   ├── servicios/                # Gestión de servicios
│   ├── insumos/                  # Gestión de inventario
│   ├── compras/                  # Gestión de compras
│   ├── liquidaciones/            # Gestión de liquidaciones
│   └── tests/                    # Pruebas unitarias
├── winespa/                      # Configuración principal de Django
├── .github/                      # Configuración de GitHub Actions
│   └── workflows/
│       └── test-api.yml
├── requirements.txt              # Dependencias del proyecto
├── pytest.ini                   # Configuración de pytest
├── conftest.py                  # Configuración de pytest para Django
└── manage.py                    # Script de gestión de Django
```

## 🔧 Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
DEBUG=True
SECRET_KEY=tu_clave_secreta_aqui
DB_NAME=winespaapi
DB_USER=tu_usuario_mysql
DB_PASSWORD=tu_contraseña_mysql
DB_HOST=localhost
DB_PORT=3306
```

## 📝 Comandos Útiles

```bash
# Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor de desarrollo
python manage.py runserver

# Ejecutar pruebas
python -m pytest api/tests/ -v

# Ejecutar pruebas específicas
python -m pytest api/tests/test_usuarios.py -v

# Ejecutar pruebas con cobertura
python -m pytest api/tests/ --cov=api --cov-report=html

# Limpiar cache de pytest
python -m pytest --cache-clear
```

## 🐛 Solución de Problemas

### Error de conexión a base de datos
- Verifica que MySQL esté ejecutándose
- Confirma las credenciales en las variables de entorno
- Asegúrate de que la base de datos `winespaapi` exista

### Error en las pruebas
- Verifica que todas las migraciones estén aplicadas
- Confirma que los modelos tengan los campos correctos
- Revisa los logs de pytest para más detalles

### Error en GitHub Actions
- Verifica que el workflow esté en la ruta correcta: `.github/workflows/`
- Confirma que el archivo YAML tenga la sintaxis correcta
- Revisa los logs del workflow en GitHub



## 👥 Autores

- *Samuel Henao Lara* -  - [ZiriusDaii](https://github.com/ZiriusDaii)

## 🙏 Agradecimientos

- Django REST Framework por el excelente framework
- pytest por las herramientas de testing
- GitHub Actions por la automatización de CI/CD
