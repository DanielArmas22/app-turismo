# 🔄 Actualizaciones Realizadas - Integración con n8n

## ✅ Cambios Implementados

### 1. Configuración de URL de n8n

**Archivos modificados:**
- `config.py`
- `.env`

**Cambio:**
```python
# Antes
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/tourist-guide"

# Ahora
N8N_WEBHOOK_URL = "https://n8n.yamboly.lat/webhook-test/tourist-guide"
```

---

### 2. Actualización del Módulo de Integración n8n

**Archivo:** `n8n_integration.py`

#### Cambio 1: Método de Recomendaciones
```python
# Antes
def get_poi_recommendations(self, city_id: str, user_location: Optional[Dict] = None):
    data = {
        "city_id": city_id,
        "user_location": user_location or {}
    }

# Ahora
def get_poi_recommendations(self, city_id: str, lat: float = None, lng: float = None):
    data = {
        "city_id": city_id
    }
    if lat is not None:
        data["lat"] = lat
    if lng is not None:
        data["lng"] = lng
```

**Razón:** Coincidir con el formato del curl que funciona:
```bash
curl -d '{"action_type":"get_poi_recommendations","lat":41.4036,"lng":2.1744,"city_id":"barcelona"}'
```

#### Cambio 2: Método de Reservas
```python
# Antes
def create_booking_with_payment(self, ..., payment_method: str = "stripe"):
    data = {
        "poi_id": poi_id,
        "booking_date": booking_date.isoformat(),
        ...
    }
    return self._call_webhook("create_booking", data)

# Ahora
def create_booking_with_payment(self, ..., currency: str = "EUR", payment_method: str = "stripe"):
    data = {
        "user_id": user_id,
        "poi_id": poi_id,
        "booking_date": booking_date.isoformat(),
        "number_of_people": number_of_people,
        "total_price": total_price,
        "currency": currency,  # ← NUEVO
        "status": "pending",
        "payment_method": payment_method,
        "user_email": user_email
    }
    return self._call_webhook("booking", data)  # ← Cambio de action_type
```

**Razón:** Coincidir con el schema de Supabase que requiere `currency` y usar `payment_id` (no `payment_intent_id`).

---

### 3. Actualización de Página de Reservas

**Archivo:** `pages/bookings_page.py`

```python
# Añadido currency en la llamada a n8n
payment_result = n8n.create_booking_with_payment(
    poi_id=poi['id'],
    booking_date=booking_datetime,
    number_of_people=people,
    total_price=price,
    user_id=st.session_state.user_id,
    user_email=st.session_state.user_email,
    currency="EUR",  # ← NUEVO
    payment_method=payment_method.lower()
)

# Añadido currency en los datos de la reserva
booking_data = {
    "user_id": st.session_state.user_id,
    "poi_id": poi['id'],
    "booking_date": booking_datetime.isoformat(),
    "number_of_people": people,
    "total_price": price,
    "currency": "EUR",  # ← NUEVO
    "status": "confirmed" if payment_result else "pending",
    "payment_method": payment_method,
    "payment_id": payment_result.get('payment_id') if payment_result else None,
    ...
}
```

---

### 4. Archivos Nuevos Creados

#### `test_n8n.py`
Script de prueba para verificar la conexión con n8n:
```bash
python test_n8n.py
```

Prueba:
- ✅ Recomendaciones de POIs
- ✅ Generación de audio-guías
- ✅ Creación de reservas

#### `CONFIGURACION_N8N.md`
Documentación completa sobre:
- Endpoints disponibles
- Formato de payloads
- Respuestas esperadas
- Ejemplos de uso
- Solución de problemas

#### `ACTUALIZACIONES.md`
Este archivo con el resumen de cambios.

---

## 🧪 Cómo Probar

### Opción 1: Script de Prueba
```bash
python test_n8n.py
```

### Opción 2: Curl Directo
```bash
# Recomendaciones
curl -L 'https://n8n.yamboly.lat/webhook-test/tourist-guide' \
-H 'Content-Type: application/json' \
-d '{
    "action_type":"get_poi_recommendations",
    "lat":41.4036,
    "lng":2.1744,
    "city_id":"barcelona"
}'

# Audio-guía
curl -L 'https://n8n.yamboly.lat/webhook-test/tourist-guide' \
-H 'Content-Type: application/json' \
-d '{
    "action_type":"audio_guide",
    "poi_id":"test-123",
    "poi_name":"Sagrada Familia",
    "poi_description":"Basílica diseñada por Antoni Gaudí",
    "user_id":"test-user",
    "language":"es",
    "voice_type":"female"
}'

# Reserva
curl -L 'https://n8n.yamboly.lat/webhook-test/tourist-guide' \
-H 'Content-Type: application/json' \
-d '{
    "action_type":"booking",
    "user_id":"test-user",
    "poi_id":"test-poi",
    "booking_date":"2025-10-31T10:00:00Z",
    "number_of_people":2,
    "total_price":39.99,
    "currency":"EUR",
    "status":"pending",
    "payment_method":"stripe"
}'
```

### Opción 3: Desde Streamlit
```bash
streamlit run app.py
```

Luego:
1. Inicia sesión
2. Ve a "🎧 Audio-Guías" o "🎫 Mis Reservas"
3. Completa el formulario
4. La app llamará automáticamente a n8n

---

## 📋 Checklist de Verificación

### Configuración Básica
- [x] URL de n8n actualizada en `config.py`
- [x] URL de n8n actualizada en `.env`
- [x] Método de recomendaciones actualizado
- [x] Método de reservas actualizado con `currency`
- [x] Página de reservas actualizada

### Pruebas
- [ ] Ejecutar `python test_n8n.py`
- [ ] Probar curl de recomendaciones
- [ ] Probar curl de audio-guía
- [ ] Probar curl de reserva
- [ ] Probar desde Streamlit

### Configuración de n8n (Opcional)
- [ ] OpenAI API configurada
- [ ] ElevenLabs API configurada
- [ ] Stripe API configurada
- [ ] Google Maps API configurada

---

## 🔍 Diferencias Clave

### Action Types

| Funcionalidad | Action Type en n8n | Action Type en usage_stats |
|---------------|-------------------|---------------------------|
| Recomendaciones | `get_poi_recommendations` | `search` |
| Audio-guías | `audio_guide` | `audio_guide` |
| Reservas | `booking` | `booking` |
| Ver POI | - | `poi_view` |

**Importante:** El `action_type` que envías a n8n puede ser diferente del que guardas en `usage_stats`.

### Campos de Reserva

| Campo | Tipo | Requerido | Notas |
|-------|------|-----------|-------|
| `user_id` | UUID | Sí | ID del usuario |
| `poi_id` | UUID | Sí | ID del POI |
| `booking_date` | TIMESTAMP | Sí | ISO 8601 format |
| `number_of_people` | INTEGER | Sí | Mínimo 1 |
| `total_price` | DECIMAL | Sí | Precio total |
| `currency` | VARCHAR(3) | Sí | EUR, USD, etc. |
| `status` | VARCHAR(50) | Sí | pending, confirmed, etc. |
| `payment_id` | VARCHAR(255) | No | ID del PaymentIntent de Stripe |
| `payment_method` | VARCHAR(50) | No | stripe, paypal, etc. |

---

## 🎯 Próximos Pasos

1. **Ejecuta el script de prueba:**
   ```bash
   python test_n8n.py
   ```

2. **Verifica los resultados:**
   - ✅ Status 200
   - ✅ Respuesta JSON válida
   - ✅ Campos esperados presentes

3. **Prueba desde Streamlit:**
   ```bash
   streamlit run app.py
   ```

4. **Configura las APIs en n8n** (si aún no lo has hecho):
   - OpenAI para generar texto
   - ElevenLabs para audio
   - Stripe para pagos

5. **Ajusta el workflow de n8n** según las notas en `CONFIGURACION_N8N.md`

---

## 📞 Soporte

Si encuentras problemas:

1. **Revisa los logs:**
   - Terminal de Streamlit
   - Executions en n8n

2. **Verifica la configuración:**
   - `.env` tiene la URL correcta
   - n8n está ejecutándose
   - Las APIs están configuradas

3. **Consulta la documentación:**
   - `CONFIGURACION_N8N.md`
   - `README.md`
   - `GUIA_RAPIDA.md`

---

**¡Todo listo para usar tu integración con n8n! 🚀**
