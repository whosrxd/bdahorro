CREATE DATABASE dbahorro;
USE dbahorro;

CREATE TABLE categorias (
    id_categoria INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE unidades (
    id_unidad INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE proveedores (
    id_proveedor INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    telefono CHAR(10),
    contacto VARCHAR(100)
);

-- Tabla clientes modificada (eliminado id_cliente redundante)
CREATE TABLE clientes (
    telefono CHAR(10) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    id_cliente INT UNIQUE,  -- Identificador de referencia para empleados
    direccion VARCHAR(100),
    correo VARCHAR(100)  -- Nuevo campo para correo electrónico
);

CREATE TABLE medicos (
    id_medico INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    especialidad VARCHAR(100),
    telefono CHAR(10)
);

-- Recetas modificada para usar teléfono en vez de id_cliente
CREATE TABLE recetas (
    id_receta INT PRIMARY KEY,
    telefono_cliente CHAR(10) NOT NULL,
    id_medico INT NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (telefono_cliente) REFERENCES clientes(telefono),
    FOREIGN KEY (id_medico) REFERENCES medicos(id_medico)
);

CREATE TABLE empleados (
    id_empleado INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    telefono CHAR(10),
    direccion VARCHAR(100),
    puesto VARCHAR(50),
    fecha_contratacion DATE
);

CREATE TABLE medicamentos (
    codigo CHAR(13) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    costo DECIMAL(10,2) NOT NULL,
    existencias INT NOT NULL,
    id_categoria INT,
    id_proveedor INT,
    id_unidad INT,
    fecha_caducidad DATE,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor),
    FOREIGN KEY (id_unidad) REFERENCES unidades(id_unidad)
);

CREATE TABLE detalle_recetas (
    id_receta INT,
    codigo_medicamento CHAR(13),
    cantidad INT NOT NULL,
    PRIMARY KEY (id_receta, codigo_medicamento),
    FOREIGN KEY (id_receta) REFERENCES recetas(id_receta),
    FOREIGN KEY (codigo_medicamento) REFERENCES medicamentos(codigo)
);

CREATE TABLE compras (
    id_compra INT PRIMARY KEY AUTO_INCREMENT,
    id_proveedor INT NOT NULL,
    fecha DATE NOT NULL, 
    importe DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
);

CREATE TABLE detalle_compras (
    id_compra INT,
    codigo CHAR(13),
    cantidad INT NOT NULL,
    PRIMARY KEY (id_compra, codigo),
    FOREIGN KEY (id_compra) REFERENCES compras(id_compra),
    FOREIGN KEY (codigo) REFERENCES medicamentos(codigo)
);

CREATE TABLE ventas (
    id_venta INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL,
    importe DECIMAL(10,2) NOT NULL,
    telefono CHAR(10) NOT NULL,
    id_empleado INT NOT NULL,
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado),
    FOREIGN KEY (telefono) REFERENCES clientes(telefono)
);

CREATE TABLE detalle_ventas (
    id_venta INT,
    codigo CHAR(13),
    cantidad INT NOT NULL,
    id_receta INT,  -- Cambiado a no obligatorio
    subtotal DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_venta, codigo),
    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta),
    FOREIGN KEY (codigo) REFERENCES medicamentos(codigo),
    FOREIGN KEY (id_receta) REFERENCES recetas(id_receta)
);

-- Consultas modificada para usar teléfono en vez de id_cliente
CREATE TABLE consultas (
    id_consulta INT PRIMARY KEY AUTO_INCREMENT,
    telefono_cliente CHAR(10) NOT NULL,
    id_empleado INT NOT NULL,
    id_receta INT NOT NULL,
    fecha DATE NOT NULL,
    motivo VARCHAR(200),
    FOREIGN KEY (telefono_cliente) REFERENCES clientes(telefono),
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado),
    FOREIGN KEY (id_receta) REFERENCES recetas(id_receta)
);

-- Inserción de datos de ejemplo

-- Categorías
INSERT INTO categorias (id_categoria, nombre)
VALUES
(1, 'Medicamentos'),
(2, 'Suplementos'),
(3, 'Cuidado Personal'),
(4, 'Higiene'),
(5, 'Belleza');

-- Clientes
INSERT INTO clientes (id_cliente, nombre, direccion, correo, telefono)
VALUES
(1, 'Juan Pérez', 'Calle Norte No. 100', 'juanp@ahorro.com', '9611783521'),
(2, 'María López', 'Avenida Central No. 48', 'marial@ahorro.com', '9611783522'),
(3, 'Carlos Sánchez', 'Real del Bosque No. 5', 'carloss@ahorro.com', '9611783523');

-- Empleados
INSERT INTO empleados (id_empleado, nombre, telefono, direccion, puesto, fecha_contratacion)
VALUES
(1, 'Ana Martínez', '9611783524', 'Calle del Sol No. 20', 'Farmacéutica', '2022-01-15'),
(2, 'Luis García', '9611783525', 'Avenida de la Paz No. 30', 'Gerente de Tienda', '2021-06-10'),
(3, 'Patricia Torres', '9611783526', 'Calle de la Luna No. 15', 'Asistente de Ventas', '2023-03-01');

-- Médicos
INSERT INTO medicos (id_medico, nombre, especialidad, telefono)
VALUES
(1, 'Dr. Alberto Ruiz', 'Pediatra', '9611783530'),
(2, 'Dra. Sofía Morales', 'Dermatología', '9611783531'),
(3, 'Dr. Javier López', 'Cardiología', '9611783532');

-- Proveedores
INSERT INTO proveedores (id_proveedor, nombre, telefono, contacto)
VALUES
(1, 'Distribuidora Salud', '9611783527', 'Fernando Ruiz'),
(2, 'Farmacéuticos Unidos', '9611783528', 'Laura Mendoza'),
(3, 'Medicamentos y Más', '9611783529', 'Jorge Salazar');

-- Unidades
INSERT INTO unidades (id_unidad, nombre)
VALUES
(1, 'Pieza'),
(2, 'Caja'),
(3, 'Botella'),
(4, 'Paquete'),
(5, 'Sobre');