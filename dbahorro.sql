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

CREATE TABLE clientes (
    telefono CHAR(10) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    id_cliente INT UNIQUE,
    direccion VARCHAR(100),
    correo VARCHAR(100)
);

CREATE TABLE medicos (
    id_medico INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    especialidad VARCHAR(100),
    telefono CHAR(10)
);

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
    id_detalle_receta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_receta INT,
    codigo_medicamento CHAR(13),
    cantidad INT NOT NULL,
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
    id_receta INT,
    subtotal DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_venta, codigo),
    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta),
    FOREIGN KEY (codigo) REFERENCES medicamentos(codigo),
    FOREIGN KEY (id_receta) REFERENCES recetas(id_receta)
);

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
(3, 'Carlos Sánchez', 'Real del Bosque No. 5', 'carloss@ahorro.com', '9611783523'),
(4, 'Ana Ramírez', 'Colonia El Retiro No. 12', 'anar@ahorro.com', '9611783533'),
(5, 'Luis Torres', 'Calle Sur No. 20', 'luist@ahorro.com', '9611783534'),
(6, 'Laura Gómez', 'Privada Las Palmas No. 7', 'laurag@ahorro.com', '9611783535'),
(7, 'Diego Martínez', 'Avenida Las Flores No. 14', 'diegom@ahorro.com', '9611783536'),
(8, 'Sofía Herrera', 'Callejón del Sol No. 2', 'sofiah@ahorro.com', '9611783537'),
(9, 'Pedro Morales', 'Barrio San Juan No. 10', 'pedrom@ahorro.com', '9611783538'),
(10, 'Fernanda Ruiz', 'Calle Roble No. 33', 'fernandar@ahorro.com', '9611783539');

-- Empleados
INSERT INTO empleados (id_empleado, nombre, telefono, direccion, puesto, fecha_contratacion)
VALUES
(1, 'Ana Martínez', '9611783524', 'Calle del Sol No. 20', 'Farmacéutica', '2022-01-15'),
(2, 'Luis García', '9611783525', 'Avenida de la Paz No. 30', 'Gerente de Tienda', '2021-06-10'),
(3, 'Patricia Torres', '9611783526', 'Calle de la Luna No. 15', 'Asistente de Ventas', '2023-03-01'),
(4, 'José Ramírez', '9611783540', 'Colonia Centro No. 1', 'Cajero', '2022-09-20'),
(5, 'Mariana Díaz', '9611783541', 'Calle Hidalgo No. 22', 'Auxiliar de Almacén', '2023-01-05'),
(6, 'Hugo Núñez', '9611783542', 'Fraccionamiento Montebello No. 18', 'Repartidor', '2021-12-15'),
(7, 'Isabel Torres', '9611783543', 'Zona Norte No. 45', 'Supervisora de Turno', '2020-11-08'),
(8, 'César Hernández', '9611783544', 'Privada Santa Elena No. 10', 'Recepcionista', '2022-07-25'),
(9, 'Paola Méndez', '9611783545', 'Colonia Jardines No. 9', 'Atención al Cliente', '2023-04-30'),
(10, 'Andrés Castillo', '9611783546', 'Barrio Nuevo No. 33', 'Encargado de Inventario', '2021-02-17');

-- Médicos
INSERT INTO medicos (id_medico, nombre, especialidad, telefono)
VALUES
(1, 'Dr. Alberto Ruiz', 'Pediatra', '9611783530'),
(2, 'Dra. Sofía Morales', 'Dermatología', '9611783531'),
(3, 'Dr. Javier López', 'Cardiología', '9611783532'),
(4, 'Dra. Elena Torres', 'Ginecología', '9611783547'),
(5, 'Dr. Mario Castro', 'Neurología', '9611783548'),
(6, 'Dra. Beatriz Luna', 'Medicina General', '9611783549'),
(7, 'Dr. Hugo García', 'Endocrinología', '9611783550'),
(8, 'Dra. Natalia Rivas', 'Oftalmología', '9611783551'),
(9, 'Dr. Ernesto Salinas', 'Traumatología', '9611783552'),
(10, 'Dra. Carmen Jiménez', 'Psiquiatría', '9611783553');

-- Proveedores
INSERT INTO proveedores (id_proveedor, nombre, telefono, contacto)
VALUES
(1, 'Distribuidora Salud', '9611783527', 'Fernando Ruiz'),
(2, 'Farmacéuticos Unidos', '9611783528', 'Laura Mendoza'),
(3, 'Medicamentos y Más', '9611783529', 'Jorge Salazar'),
(4, 'Suministros Médicos del Sur', '9611783554', 'Ricardo Pérez'),
(5, 'Farmacia Global', '9611783555', 'Mónica Vázquez'),
(6, 'Grupo Salud Integral', '9611783556', 'Andrés Gómez'),
(7, 'Distribuidora FarmaPlus', '9611783557', 'Claudia Romero'),
(8, 'Red de Medicinas', '9611783558', 'Julio Ortega'),
(9, 'Suplementos y Más', '9611783559', 'Silvia Fernández'),
(10, 'Droguería del Sureste', '9611783560', 'Gabriela Torres');

-- Unidades
INSERT INTO unidades (id_unidad, nombre)
VALUES
(1, 'Pieza'),
(2, 'Caja'),
(3, 'Botella'),
(4, 'Paquete'),
(5, 'Sobre');

-- Medicamentos
INSERT INTO medicamentos (codigo, nombre, precio, costo, existencias, id_categoria, id_proveedor, id_unidad, fecha_caducidad)
VALUES
('7701234567890', 'Paracetamol 500mg', 25.00, 10.00, 100, 1, 1, 1, '2026-05-01'),
('7701234567891', 'Ibuprofeno 400mg', 30.00, 12.00, 80, 1, 2, 1, '2026-06-15'),
('7701234567892', 'Omeprazol 20mg', 45.00, 18.00, 60, 1, 3, 2, '2026-07-20'),
('7701234567893', 'Suero Oral', 18.00, 8.00, 120, 2, 4, 3, '2025-12-10'),
('7701234567894', 'Multivitamínico', 55.00, 25.00, 70, 2, 5, 2, '2026-01-05'),
('7701234567895', 'Shampoo Anticaspa', 75.00, 40.00, 50, 3, 6, 3, '2025-11-11'),
('7701234567896', 'Jabón Neutro', 20.00, 9.00, 150, 4, 7, 1, '2025-10-01'),
('7701234567897', 'Cepillo Dental', 15.00, 5.00, 200, 4, 8, 1, '2027-01-01'),
('7701234567898', 'Maquillaje Líquido', 120.00, 70.00, 30, 5, 9, 2, '2025-08-20'),
('7701234567899', 'Labial Mate', 90.00, 50.00, 40, 5, 10, 2, '2025-09-25'),
('7701234567800', 'Vitamina C 500mg', 35.00, 15.00, 100, 2, 1, 2, '2026-03-30'),
('7701234567801', 'Aspirina 100mg', 22.00, 10.00, 95, 1, 2, 1, '2026-04-18'),
('7701234567802', 'Enjuague Bucal', 50.00, 25.00, 60, 4, 3, 3, '2025-12-01'),
('7701234567803', 'Crema Hidratante', 85.00, 45.00, 40, 3, 4, 3, '2026-01-10'),
('7701234567804', 'Proteína en Polvo', 150.00, 80.00, 25, 2, 5, 4, '2026-05-20');

INSERT INTO ventas (fecha, importe, id_cliente, id_empleado)
VALUES
('2025-05-20', 250.50, 1, 2),
('2025-05-21', 130.00, 2, 3),
('2025-05-22', 340.75, 3, 1),
('2025-05-23', 80.90, 4, 4),
('2025-05-24', 120.00, 5, 5),
('2025-05-25', 60.00, 6, 6),
('2025-05-26', 275.35, 7, 7),
('2025-05-27', 99.99, 8, 8),
('2025-05-28', 45.00, 9, 9),
('2025-05-29', 150.25, 10, 10),
('2025-05-30', 200.00, 1, 1),
('2025-05-31', 75.00, 2, 2),
('2025-06-01', 90.50, 3, 3),
('2025-06-02', 110.10, 4, 4),
('2025-06-03', 320.00, 5, 5);

IINSERT INTO detalles_venta (id_venta, codigo, cantidad, id_receta, subtotal)
VALUES
(1, '00034732', 2, 1, 99.98),
(1, '7701234567890', 3, 2, 30.00),
(1, '7701234567897', 1, 3, 5.00),
(2, '000848313', 1, 1, 39.99),
(2, '7701234567891', 2, 2, 24.00),
(2, '7701234567893', 4, 3, 32.00),
(3, '7701234567895', 1, 4, 40.00),
(3, '7701234567896', 5, 5, 45.00),
(3, '7701234567892', 2, 2, 36.00),
(4, '7701234567899', 1, 3, 50.00),
(4, '7701234567800', 2, 4, 30.00),
(4, '7701234567894', 1, 1, 25.00),
(5, '7701234567802', 3, 2, 75.00),
(5, '7701234567804', 1, 3, 80.00),
(5, '7701234567898', 2, 4, 140.00);

INSERT INTO recetas (id_receta, id_cliente, id_medico, fecha)
VALUES
(1, 1, 6, '2025-05-10'),
(2, 2, 2, '2025-05-11'),
(3, 3, 3, '2025-05-12'),
(4, 4, 1, '2025-05-12'),
(5, 5, 4, '2025-05-13'),
(6, 6, 7, '2025-05-13'),
(7, 7, 8, '2025-05-14'),
(8, 8, 5, '2025-05-14'),
(9, 9, 9, '2025-05-15'),
(10, 10, 10, '2025-05-15');

INSERT INTO consultas (id_consulta, id_cliente, id_empleado, id_receta, fecha, motivo)
VALUES
(1, 4, 2, 1, '2025-05-27', 'Dolor abdominal'),
(2, 1, 1, 2, '2025-05-10', 'Revisión general'),
(3, 2, 3, 3, '2025-05-11', 'Erupción en la piel'),
(4, 3, 4, 4, '2025-05-12', 'Palpitaciones'),
(5, 4, 5, 5, '2025-05-12', 'Chequeo pediátrico'),
(6, 5, 6, 6, '2025-05-13', 'Dolor de cabeza constante'),
(7, 6, 7, 7, '2025-05-13', 'Problemas hormonales'),
(8, 7, 8, 8, '2025-05-14', 'Revisión ocular'),
(9, 8, 9, 9, '2025-05-14', 'Dolor de espalda'),
(10, 9, 10, 10, '2025-05-15', 'Ansiedad y estrés'),
(11, 10, 1, 11, '2025-05-15', 'Chequeo anual');

INSERT INTO compras (id_proveedor, fecha, importe) VALUES
(1, '2025-04-01', 3500.00),
(2, '2025-04-03', 2700.50),
(3, '2025-04-05', 4800.75),
(4, '2025-04-07', 1900.20),
(5, '2025-04-10', 3600.00),
(6, '2025-04-12', 4100.60),
(7, '2025-04-14', 2850.10),
(8, '2025-04-16', 3250.30),
(9, '2025-04-18', 2950.80),
(10, '2025-04-20', 3750.00),
(1, '2025-04-22', 3300.90),
(2, '2025-04-24', 4100.15),
(3, '2025-04-26', 4550.00),
(4, '2025-04-28', 2850.75),
(5, '2025-04-30', 3950.60);

INSERT INTO detalle_compras (id_detalle_compra, id_compra, codigo, cantidad) VALUES
(1, 1, '00034732', 10),
(2, 1, '000848313', 5),
(3, 2, '7701234567800', 20),
(4, 2, '7701234567801', 15),
(5, 3, '7701234567802', 12),
(6, 3, '7701234567803', 7),
(7, 4, '7701234567804', 8),
(8, 4, '7701234567890', 14),
(9, 5, '7701234567891', 9),
(10, 5, '7701234567892', 11),
(11, 6, '7701234567893', 6),
(12, 6, '7701234567894', 4),
(13, 7, '7701234567895', 3),
(14, 7, '7701234567896', 25),
(15, 8, '7701234567897', 30);