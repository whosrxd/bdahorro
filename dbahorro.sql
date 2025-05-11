use dbahorro;

CREATE TABLE categorias (
    id_categoria INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE unidades (
    id_unidad INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE proveedores (
    id_proveedor INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    telefono CHAR(10),
    contacto VARCHAR(100)
);

CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    telefono CHAR(10),
    direccion VARCHAR(150)
);

CREATE TABLE medicos (
    id_medico INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100),
    telefono CHAR(10)
);

CREATE TABLE recetas (
    id_receta INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT NOT NULL,
    id_medico INT NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_medico) REFERENCES medicos(id_medico)
);

CREATE TABLE empleados (
    id_empleado INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    telefono CHAR(10),
    direccion VARCHAR(150),
    puesto VARCHAR(50),
    fecha_contratacion DATE
);

CREATE TABLE medicamentos (
    codigo CHAR(13) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
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
    id_cliente INT NOT NULL,
    id_empleado INT NOT NULL,
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado),
    FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente)
);

CREATE TABLE detalle_ventas (
    id_venta INT,
    codigo CHAR(13),
    cantidad INT NOT NULL,
    id_receta INT NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_venta, codigo),
    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta),
    FOREIGN KEY (codigo) REFERENCES medicamentos(codigo)
    FOREIGN KEY (id_receta) REFERENCES recetas(id_receta)
);

CREATE TABLE consultas (
    id_consulta INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT NOT NULL,
    id_empleado INT NOT NULL,
    id_receta INT NOT NULL,
    fecha DATE NOT NULL,
    motivo VARCHAR(255),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado),
    FOREIGN KEY (id_receta) REFERENCES recetas(id_receta)
);