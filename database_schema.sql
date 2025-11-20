-- MEMOR.IA - PostgreSQL Database Schema
-- Esquema para base de datos en Neon (PostgreSQL)

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    empresa VARCHAR(255) NOT NULL,
    telefono VARCHAR(50),
    cif VARCHAR(50),
    direccion TEXT,
    numero_cuenta VARCHAR(100),
    rol VARCHAR(50) DEFAULT 'Usuario',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    plan VARCHAR(50) DEFAULT 'basico',
    fecha_expiracion DATE
);

-- Tabla de perfiles de empresa
CREATE TABLE IF NOT EXISTS perfiles_empresa (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER UNIQUE,
    sector TEXT,
    empleados VARCHAR(100),
    experiencia_anos VARCHAR(50),
    certificaciones TEXT,  -- JSON con array de certificaciones
    otras_certificaciones TEXT,
    experiencia_similar TEXT,
    logo_path TEXT,  -- URL de Cloudinary
    medios_materiales TEXT,
    herramientas_software TEXT,
    equipo_tecnico TEXT,  -- JSON con array de técnicos
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
);

-- Tabla de pagos
CREATE TABLE IF NOT EXISTS pagos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER,
    stripe_payment_id VARCHAR(255),
    importe DECIMAL(10, 2),
    fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(50) DEFAULT 'pendiente',
    plan VARCHAR(50),
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
);

-- Tabla de tokens de recuperación
CREATE TABLE IF NOT EXISTS tokens_recuperacion (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    token VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usado BOOLEAN DEFAULT FALSE
);

-- Índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
CREATE INDEX IF NOT EXISTS idx_perfiles_usuario_id ON perfiles_empresa(usuario_id);
CREATE INDEX IF NOT EXISTS idx_pagos_usuario_id ON pagos(usuario_id);
CREATE INDEX IF NOT EXISTS idx_tokens_email ON tokens_recuperacion(email);
CREATE INDEX IF NOT EXISTS idx_tokens_token ON tokens_recuperacion(token);
