-- Tablas independientes
CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telefono VARCHAR(50),
    fecha_registro DATE DEFAULT CURRENT_DATE
);

CREATE TABLE restaurante (
    id_restaurante SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    categoria VARCHAR(100)
);

CREATE TABLE repartidor (
    id_repartidor SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    telefono VARCHAR(50),
    vehiculo VARCHAR(100),
    esta_activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE promocion (
    id_promocion SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    porcentaje_descuento INTEGER CHECK (porcentaje_descuento BETWEEN 1 AND 100),
    fecha_inicio TIMESTAMP NOT NULL,
    fecha_fin TIMESTAMP NOT NULL,
    stock_usos INTEGER CHECK (stock_usos >= 0),
    CONSTRAINT chk_fechas CHECK (fecha_fin > fecha_inicio)
);

-- Tablas dependientes

CREATE TABLE plato (
    id_plato SERIAL PRIMARY KEY,
    id_restaurante INTEGER REFERENCES restaurante(id_restaurante),
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    precio_actual DECIMAL(10, 2) CHECK (precio_actual > 0),
    esta_disponible BOOLEAN DEFAULT TRUE
);

CREATE TABLE pedido (
    id_pedido SERIAL PRIMARY KEY,
    id_usuario INTEGER REFERENCES usuario(id_usuario),
    id_restaurante INTEGER REFERENCES restaurante(id_restaurante),
    id_repartidor INTEGER REFERENCES repartidor(id_repartidor),
    id_promocion INTEGER REFERENCES promocion(id_promocion),
    fecha_hora_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_abonado DECIMAL(10, 2) CHECK (total_abonado >= 0),
    direccion_entrega VARCHAR(255) NOT NULL
);

CREATE TABLE detalle_pedido (
    id_pedido INTEGER REFERENCES pedido(id_pedido),
    id_plato INTEGER REFERENCES plato(id_plato),
    cantidad INTEGER CHECK (cantidad > 0),
    precio_unitario_historico DECIMAL(10, 2) CHECK (precio_unitario_historico > 0),
    PRIMARY KEY (id_pedido, id_plato)
);

CREATE TABLE historial_estado_pedido (
    id_historial SERIAL PRIMARY KEY,
    id_pedido INTEGER REFERENCES pedido(id_pedido),
    estado VARCHAR(50) CHECK (estado IN ('creado', 'en_preparacion', 'en_camino', 'entregado', 'cancelado')),
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);