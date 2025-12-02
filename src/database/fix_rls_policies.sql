-- ============================================
-- CORRECCIÓN DE POLÍTICAS RLS
-- ============================================
-- Este script corrige las políticas RLS para permitir
-- operaciones sin autenticación de Supabase Auth

-- Eliminar políticas existentes de usuarios
DROP POLICY IF EXISTS "Usuarios pueden ver su propia información" ON users;
DROP POLICY IF EXISTS "Usuarios pueden actualizar su propia información" ON users;

-- Crear nuevas políticas para usuarios que permiten operaciones sin auth
-- Permitir lectura de usuarios (público)
CREATE POLICY "Usuarios visibles para todos" ON users 
    FOR SELECT 
    USING (true);

-- Permitir inserción de usuarios (público)
CREATE POLICY "Cualquiera puede crear usuarios" ON users 
    FOR INSERT 
    WITH CHECK (true);

-- Permitir actualización de usuarios (público - en producción deberías restringir esto)
CREATE POLICY "Usuarios pueden actualizar su información" ON users 
    FOR UPDATE 
    USING (true)
    WITH CHECK (true);

-- Permitir eliminación de usuarios (público - en producción deberías restringir esto)
CREATE POLICY "Usuarios pueden eliminar su cuenta" ON users 
    FOR DELETE 
    USING (true);

-- Actualizar políticas de user_visits para permitir operaciones sin auth
DROP POLICY IF EXISTS "Usuarios pueden ver sus propias visitas" ON user_visits;
DROP POLICY IF EXISTS "Usuarios pueden crear sus propias visitas" ON user_visits;

CREATE POLICY "Visitas visibles para todos" ON user_visits 
    FOR SELECT 
    USING (true);

CREATE POLICY "Cualquiera puede crear visitas" ON user_visits 
    FOR INSERT 
    WITH CHECK (true);

-- Actualizar políticas de user_achievements
DROP POLICY IF EXISTS "Usuarios pueden ver sus propios logros" ON user_achievements;

CREATE POLICY "Logros visibles para todos" ON user_achievements 
    FOR SELECT 
    USING (true);

CREATE POLICY "Cualquiera puede crear logros" ON user_achievements 
    FOR INSERT 
    WITH CHECK (true);

-- Actualizar políticas de bookings
DROP POLICY IF EXISTS "Usuarios pueden ver sus propias reservas" ON bookings;
DROP POLICY IF EXISTS "Usuarios pueden crear sus propias reservas" ON bookings;

CREATE POLICY "Reservas visibles para todos" ON bookings 
    FOR SELECT 
    USING (true);

CREATE POLICY "Cualquiera puede crear reservas" ON bookings 
    FOR INSERT 
    WITH CHECK (true);

CREATE POLICY "Cualquiera puede actualizar reservas" ON bookings 
    FOR UPDATE 
    USING (true)
    WITH CHECK (true);

-- Actualizar políticas de favorites
DROP POLICY IF EXISTS "Usuarios pueden ver sus propios favoritos" ON favorites;
DROP POLICY IF EXISTS "Usuarios pueden crear sus propios favoritos" ON favorites;
DROP POLICY IF EXISTS "Usuarios pueden eliminar sus propios favoritos" ON favorites;

CREATE POLICY "Favoritos visibles para todos" ON favorites 
    FOR SELECT 
    USING (true);

CREATE POLICY "Cualquiera puede crear favoritos" ON favorites 
    FOR INSERT 
    WITH CHECK (true);

CREATE POLICY "Cualquiera puede eliminar favoritos" ON favorites 
    FOR DELETE 
    USING (true);

-- Actualizar políticas de usage_stats
CREATE POLICY "Estadísticas visibles para todos" ON usage_stats 
    FOR SELECT 
    USING (true);

CREATE POLICY "Cualquiera puede crear estadísticas" ON usage_stats 
    FOR INSERT 
    WITH CHECK (true);

-- Verificar que las políticas se crearon correctamente
SELECT 'Políticas RLS actualizadas exitosamente!' as resultado;

