-- ============================================
-- GUÍA TURÍSTICA VIRTUAL - SCHEMA COMPLETO
-- ============================================

-- Paso 1: Habilitar extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis"; -- Para funciones geoespaciales avanzadas (opcional)

-- ============================================
-- TABLA: users (Usuarios)
-- ============================================
CREATE TABLE users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    subscription_tier VARCHAR(50) DEFAULT 'free' CHECK (subscription_tier IN ('free', 'basic', 'premium', 'enterprise')),
    subscription_end_date TIMESTAMP,
    total_points INTEGER DEFAULT 0,
    level VARCHAR(50) DEFAULT 'Explorador Novato',
    avatar_url TEXT,
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Índices para usuarios
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_subscription ON users(subscription_tier);

-- ============================================
-- TABLA: cities (Ciudades)
-- ============================================
CREATE TABLE cities (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    country_code VARCHAR(2),
    description TEXT,
    image_url TEXT,
    price DECIMAL(10,2) DEFAULT 0.00,
    currency VARCHAR(3) DEFAULT 'EUR',
    is_active BOOLEAN DEFAULT true,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    timezone VARCHAR(50),
    language VARCHAR(50),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Índices para ciudades
CREATE INDEX idx_cities_name ON cities(name);
CREATE INDEX idx_cities_country ON cities(country);
CREATE INDEX idx_cities_active ON cities(is_active);

-- ============================================
-- TABLA: points_of_interest (Puntos de Interés)
-- ============================================
CREATE TABLE points_of_interest (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    city_id UUID REFERENCES cities(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    short_description VARCHAR(500),
    latitude DECIMAL(10,8) NOT NULL,
    longitude DECIMAL(11,8) NOT NULL,
    category VARCHAR(100) CHECK (category IN ('Histórico', 'Cultural', 'Arquitectónico', 'Gastronómico', 'Natural', 'Iconico', 'Religioso', 'Moderno')),
    subcategory VARCHAR(100),
    audio_guide_url TEXT,
    ar_content_url TEXT,
    image_urls JSONB DEFAULT '[]',
    visit_duration INTEGER DEFAULT 30, -- en minutos
    difficulty_level VARCHAR(20) DEFAULT 'Fácil' CHECK (difficulty_level IN ('Fácil', 'Moderado', 'Difícil')),
    accessibility_info TEXT,
    opening_hours JSONB DEFAULT '{}',
    entry_price DECIMAL(10,2) DEFAULT 0.00,
    rating DECIMAL(3,2) DEFAULT 0.00,
    total_reviews INTEGER DEFAULT 0,
    tags JSONB DEFAULT '[]',
    is_active BOOLEAN DEFAULT true,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Índices para POIs
CREATE INDEX idx_poi_city ON points_of_interest(city_id);
CREATE INDEX idx_poi_category ON points_of_interest(category);
CREATE INDEX idx_poi_active ON points_of_interest(is_active);
CREATE INDEX idx_poi_rating ON points_of_interest(rating DESC);
CREATE INDEX idx_poi_location ON points_of_interest(latitude, longitude);

-- ============================================
-- TABLA: user_visits (Visitas de Usuarios)
-- ============================================
CREATE TABLE user_visits (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    poi_id UUID REFERENCES points_of_interest(id) ON DELETE CASCADE,
    visit_date TIMESTAMP DEFAULT NOW(),
    duration_minutes INTEGER,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review TEXT,
    notes TEXT,
    photos JSONB DEFAULT '[]',
    checkin_location JSONB,
    weather_conditions VARCHAR(100),
    is_completed BOOLEAN DEFAULT false,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Índices para visitas
CREATE INDEX idx_visits_user ON user_visits(user_id);
CREATE INDEX idx_visits_poi ON user_visits(poi_id);
CREATE INDEX idx_visits_date ON user_visits(visit_date DESC);
CREATE INDEX idx_visits_rating ON user_visits(rating);

-- ============================================
-- TABLA: user_achievements (Logros/Gamificación)
-- ============================================
CREATE TABLE user_achievements (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    achievement_type VARCHAR(100) NOT NULL CHECK (achievement_type IN ('visitas', 'explorador', 'coleccionista', 'social', 'experto', 'especial')),
    achievement_name VARCHAR(200) NOT NULL,
    achievement_description TEXT,
    points INTEGER DEFAULT 0,
    badge_icon VARCHAR(50),
    badge_color VARCHAR(20),
    earned_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',
    UNIQUE(user_id, achievement_name)
);

-- Índices para logros
CREATE INDEX idx_achievements_user ON user_achievements(user_id);
CREATE INDEX idx_achievements_type ON user_achievements(achievement_type);
CREATE INDEX idx_achievements_date ON user_achievements(earned_at DESC);

-- ============================================
-- TABLA: bookings (Reservas)
-- ============================================
CREATE TABLE bookings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    poi_id UUID REFERENCES points_of_interest(id) ON DELETE CASCADE,
    booking_date TIMESTAMP NOT NULL,
    number_of_people INTEGER DEFAULT 1 CHECK (number_of_people > 0),
    total_price DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'EUR',
    status VARCHAR(50) DEFAULT 'confirmed' CHECK (status IN ('pending', 'confirmed', 'cancelled', 'completed', 'refunded')),
    payment_method VARCHAR(50),
    payment_id VARCHAR(255),
    confirmation_code VARCHAR(20) UNIQUE,
    notes TEXT,
    special_requirements TEXT,
    contact_email VARCHAR(255),
    contact_phone VARCHAR(20),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Índices para reservas
CREATE INDEX idx_bookings_user ON bookings(user_id);
CREATE INDEX idx_bookings_poi ON bookings(poi_id);
CREATE INDEX idx_bookings_date ON bookings(booking_date);
CREATE INDEX idx_bookings_status ON bookings(status);
CREATE INDEX idx_bookings_confirmation ON bookings(confirmation_code);

-- ============================================
-- TABLA: usage_stats (Estadísticas de Uso)
-- ============================================
CREATE TABLE usage_stats (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    action_type VARCHAR(100) NOT NULL CHECK (action_type IN ('audio_guide', 'poi_view', 'search', 'booking', 'review', 'share', 'favorite', 'navigation')),
    poi_id UUID REFERENCES points_of_interest(id) ON DELETE SET NULL,
    city_id UUID REFERENCES cities(id) ON DELETE SET NULL,
    timestamp TIMESTAMP DEFAULT NOW(),
    duration_seconds INTEGER,
    device_type VARCHAR(50),
    platform VARCHAR(50),
    ip_address INET,
    user_agent TEXT,
    metadata JSONB DEFAULT '{}'
);

-- Índices para estadísticas
CREATE INDEX idx_stats_user ON usage_stats(user_id);
CREATE INDEX idx_stats_action ON usage_stats(action_type);
CREATE INDEX idx_stats_timestamp ON usage_stats(timestamp DESC);
CREATE INDEX idx_stats_poi ON usage_stats(poi_id);

-- ============================================
-- TABLA: audio_guides (Audio-Guías Generadas)
-- ============================================
CREATE TABLE audio_guides (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    poi_id UUID REFERENCES points_of_interest(id) ON DELETE CASCADE,
    language VARCHAR(10) DEFAULT 'es',
    voice_type VARCHAR(50),
    transcript TEXT NOT NULL,
    audio_url TEXT,
    duration_seconds INTEGER,
    file_size_bytes BIGINT,
    generation_model VARCHAR(50),
    generation_cost DECIMAL(10,4),
    play_count INTEGER DEFAULT 0,
    last_played_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Índices para audio-guías
CREATE INDEX idx_audio_poi ON audio_guides(poi_id);
CREATE INDEX idx_audio_language ON audio_guides(language);
CREATE INDEX idx_audio_active ON audio_guides(is_active);

-- ============================================
-- TABLA: favorites (Favoritos de Usuarios)
-- ============================================
CREATE TABLE favorites (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    poi_id UUID REFERENCES points_of_interest(id) ON DELETE CASCADE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, poi_id)
);

-- Índices para favoritos
CREATE INDEX idx_favorites_user ON favorites(user_id);
CREATE INDEX idx_favorites_poi ON favorites(poi_id);

-- ============================================
-- FUNCIONES Y TRIGGERS
-- ============================================

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger a tablas relevantes
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_cities_updated_at BEFORE UPDATE ON cities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_poi_updated_at BEFORE UPDATE ON points_of_interest
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_bookings_updated_at BEFORE UPDATE ON bookings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Función para generar código de confirmación único
CREATE OR REPLACE FUNCTION generate_confirmation_code()
RETURNS TRIGGER AS $$
BEGIN
    NEW.confirmation_code = UPPER(SUBSTRING(MD5(RANDOM()::TEXT) FROM 1 FOR 10));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER generate_booking_confirmation BEFORE INSERT ON bookings
    FOR EACH ROW EXECUTE FUNCTION generate_confirmation_code();

-- Función para actualizar puntos del usuario cuando gana logros
CREATE OR REPLACE FUNCTION update_user_points_on_achievement()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE users 
    SET total_points = total_points + NEW.points
    WHERE id = NEW.user_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER add_points_on_achievement AFTER INSERT ON user_achievements
    FOR EACH ROW EXECUTE FUNCTION update_user_points_on_achievement();

-- ============================================
-- DATOS DE EJEMPLO (OPCIONAL)
-- ============================================

-- Insertar ciudades de ejemplo
INSERT INTO cities (name, country, country_code, description, price, latitude, longitude, language) VALUES
('Madrid', 'España', 'ES', 'Capital de España, rica en historia y cultura', 9.99, 40.416775, -3.703790, 'español'),
('Barcelona', 'España', 'ES', 'Ciudad cosmopolita con arquitectura única', 9.99, 41.385064, 2.173404, 'español'),
('París', 'Francia', 'FR', 'La ciudad del amor y las luces', 12.99, 48.856614, 2.352222, 'francés'),
('Roma', 'Italia', 'IT', 'La ciudad eterna con milenios de historia', 11.99, 41.902783, 12.496366, 'italiano');

-- Insertar puntos de interés de ejemplo
INSERT INTO points_of_interest (city_id, name, description, latitude, longitude, category, visit_duration, entry_price) VALUES
((SELECT id FROM cities WHERE name = 'Madrid'), 'Palacio Real', 'Residencia oficial de la Familia Real Española con más de 3,400 habitaciones', 40.417944, -3.714347, 'Histórico', 90, 12.00),
((SELECT id FROM cities WHERE name = 'Madrid'), 'Museo del Prado', 'Una de las galerías de arte más importantes del mundo', 40.413790, -3.692212, 'Cultural', 120, 15.00),
((SELECT id FROM cities WHERE name = 'Barcelona'), 'Sagrada Familia', 'Basílica diseñada por Antoni Gaudí, aún en construcción', 41.403629, 2.174356, 'Arquitectónico', 90, 26.00),
((SELECT id FROM cities WHERE name = 'París'), 'Torre Eiffel', 'Icónico símbolo de París y estructura de hierro forjado', 48.858370, 2.294481, 'Iconico', 120, 28.00);


-- ============================================
-- VISTAS ÚTILES
-- ============================================

-- Vista de POIs con información de ciudad
CREATE OR REPLACE VIEW vw_pois_with_city AS
SELECT 
    p.*,
    c.name as city_name,
    c.country,
    c.country_code
FROM points_of_interest p
JOIN cities c ON p.city_id = c.id
WHERE p.is_active = true AND c.is_active = true;

-- Vista de estadísticas por usuario
CREATE OR REPLACE VIEW vw_user_stats AS
SELECT 
    u.id,
    u.name,
    u.email,
    u.total_points,
    u.level,
    COUNT(DISTINCT v.id) as total_visits,
    COUNT(DISTINCT b.id) as total_bookings,
    COUNT(DISTINCT a.id) as total_achievements
FROM users u
LEFT JOIN user_visits v ON u.id = v.user_id
LEFT JOIN bookings b ON u.id = b.user_id
LEFT JOIN user_achievements a ON u.id = a.user_id
GROUP BY u.id, u.name, u.email, u.total_points, u.level;

-- ============================================
-- ÍNDICES DE TEXTO COMPLETO (Full-Text Search)
-- ============================================

-- Crear índice de búsqueda para POIs
CREATE INDEX idx_poi_search ON points_of_interest 
USING gin(to_tsvector('spanish', name || ' ' || COALESCE(description, '')));

-- Crear índice de búsqueda para ciudades
CREATE INDEX idx_city_search ON cities 
USING gin(to_tsvector('spanish', name || ' ' || COALESCE(description, '')));

-- ============================================
-- COMENTARIOS EN TABLAS
-- ============================================

COMMENT ON TABLE users IS 'Tabla de usuarios del sistema';
COMMENT ON TABLE cities IS 'Catálogo de ciudades disponibles';
COMMENT ON TABLE points_of_interest IS 'Puntos de interés turísticos';
COMMENT ON TABLE user_visits IS 'Registro de visitas de usuarios a POIs';
COMMENT ON TABLE user_achievements IS 'Sistema de gamificación y logros';
COMMENT ON TABLE bookings IS 'Reservas realizadas por usuarios';
COMMENT ON TABLE usage_stats IS 'Estadísticas de uso del sistema';
COMMENT ON TABLE audio_guides IS 'Audio-guías generadas por IA';
COMMENT ON TABLE favorites IS 'POIs marcados como favoritos';

-- ============================================
-- FINALIZACIÓN
-- ============================================

-- Script completado exitosamente
SELECT 'Schema de Guía Turística Virtual creado exitosamente!' as resultado;