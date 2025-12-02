-- ============================================
-- MIGRACIÓN: Agregar campo role a usuarios
-- ============================================
-- Este script agrega el campo 'role' a la tabla users
-- y actualiza los usuarios existentes con el valor por defecto 'user'

-- Paso 1: Agregar la columna role si no existe
ALTER TABLE users
    ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'user';

-- Paso 2: Crear índice para mejorar consultas por rol
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- Paso 3: Actualizar usuarios existentes que puedan tener NULL o vacío
UPDATE users
SET role = 'user'
WHERE role IS NULL OR role = '';

-- Paso 4: Verificar que todos los usuarios tengan un rol asignado
-- (Opcional: Comentar después de verificar)
-- SELECT id, email, name FROM users WHERE role IS NULL OR role = '';

-- Script completado exitosamente
SELECT 'Migración de campo role completada exitosamente!' as resultado;

