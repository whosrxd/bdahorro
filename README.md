# Base de Datos e Interfaz (dbahorro)

### Este es un proyecto para la manipulación directa de una base de datos a través de una interfaz. Todo esto con conexión a **MySQ y TKinter**.

## 1. Funcionalidades **CRUD** (Create, Read, Update, Delete) para las tablas:
### `categorias`
### `clientes`
### `empleados`
### `medicos`
### `proveedores`
### `unidades`

## 2. Características. 
###     2.1	Menú Principal de Configuración:
###	    Al iniciar la aplicación, se muestra un menú principal donde el administrador debe ingresar una contraseña para acceder a las configuraciones del sistema.
###	    2.2	Gestión CRUD:
###	    •	Desde el menú principal, se puede acceder a cada uno de los CRUD de la base de datos:
###	    •	Categorías
###	    •	Clientes
###	    •	Empleados
###	    •	Médicos
###	    •	Proveedores
###	    •	Unidades
###	    2.3	Seguridad y Control de Acceso:
###	    •	Solo usuarios con permisos de administrador pueden acceder a la configuración de la base de datos,  garantizando seguridad en la gestión de datos.
###	    2.4	Interfaz Amigable:
###	    •	La aplicación está desarrollada con Tkinter para proporcionar una experiencia intuitiva y clara para el usuario.
## 3. Requisitos.
###    - Python 3.13.0
###    - MySQL en ejecución
###    - pip para instalación de paquetes
## 4. Pasos para configuración
###    4.1 Crear entorno virtual `python -m venv env2320634`
###    4.2 Activar entorno virtual `.\env23270631\Scripts\activate`
###    4.3 Verificación de paquetes instalados `pip list`
###    4.4 Instalar dependencias utilizads `pip install mysql.connector-python tk`
## 5. Configuración de la base de datos (dbahorro) 
###    `mysql -u root -p < dbahorro.sql`
###    5.1 Credenciales de conexión
###    MYSQL_CONFIG = {
###    'host': 'localhost',
###    'user': 'root',
###    'password': 'Rodri1705',
###    'database': 'dbahorro'
###    }
## 6. Ejecución de aplicación 
###     `python main.py`