# 🔌 Configuración de n8n - Guía Turística Virtual

## ✅ Estado Actual

Tu webhook de n8n está **CONFIGURADO Y FUNCIONANDO**:

```
URL: https://n8n.yamboly.lat/webhook-test/tourist-guide
```

## 🧪 Prueba Exitosa

El siguiente comando funciona correctamente:

```bash
curl -L 'https://n8n.yamboly.lat/webhook-test/tourist-guide' \
-H 'Content-Type: application/json' \
-d '{
    "action_type":"get_poi_recommendations",
    "lat":41.4036,"lng":2.1744,"city_id":"barcelona"
  }'
```

**Respuesta esperada:**
```json
{
  "id": "5a9926dd-83f9-4ec9-9d6c-8ca75b401f99",
  "city_id": "909557d0-8257-446d-acb3-c97e69a600c1",
  "name": "Sagrada Familia",
  "description": "Basílica diseñada por Antoni Gaudí, aún en construcción",
  "short_description": null,
  "latitude": 41.403629,
  "longitude": 2.174356,
  "category": "Arquitectónico",
  "subcategory": null,
  "audio_guide_url": null,
  "ar_content_url": null,
  "image_urls": [],
  "visit_duration": 90,
  "difficulty_level": "fácil",
  "accessibility_info": null,
  ...
}
```

## 📋 Endpoints Disponibles

### 1. Recomendaciones de POIs

**Action Type:** `get_poi_recommendations`

**Payload:**
```json
{
  "action_type": "get_poi_recommendations",
  "lat": 41.4036,
  "lng": 2.1744,
  "city_id": "barcelona",
  "user_id": "optional-user-id"
}
```

**Uso en Streamlit:**
```python
result = n8n.get_poi_recommendations(
    city_id="barcelona",
    lat=41.4036,
    lng=2.1744,
    user_id=st.session_state.user_id
)
```

---

### 2. Audio-Guías

**Action Type:** `audio_guide`

**Payload:**
```json
{
  "action_type": "audio_guide",
  "poi_id": "uuid-del-poi",
  "poi_name": "Sagrada Familia",
  "poi_description": "Descripción del lugar",
  "user_id": "uuid-del-usuario",
  "language": "es",
  "voice_type": "female"
}
```

**Uso en Streamlit:**
```python
result = n8n.generate_audio_guide(
    poi_id=poi['id'],
    poi_name=poi['name'],
    poi_description=poi['description'],
    user_id=st.session_state.user_id,
    language="es",
    voice_type="female"
)
```

---

### 3. Reservas con Pago

**Action Type:** `booking`

**Payload:**
```json
{
  "action_type": "booking",
  "user_id": "uuid-del-usuario",
  "poi_id": "uuid-del-poi",
  "booking_date": "2025-10-31T10:00:00Z",
  "number_of_people": 2,
  "total_price": 39.99,
  "currency": "EUR",
  "status": "pending",
  "payment_method": "stripe",
  "user_email": "usuario@ejemplo.com"
}
```

**Respuesta esperada:**
```json
{
  "user_id": "...",
  "poi_id": "...",
  "booking_date": "2025-10-31T10:00:00Z",
  "number_of_people": 2,
  "total_price": 39.99,
  "currency": "EUR",
  "status": "pending",
  "payment_id": "{{id}}"
}
```

**Nota importante:** El `payment_id` viene del PaymentIntent de Stripe.

**Uso en Streamlit:**
```python
result = n8n.create_booking_with_payment(
    poi_id=poi['id'],
    booking_date=datetime.now(),
    number_of_people=2,
    total_price=39.99,
    user_id=st.session_state.user_id,
    user_email=st.session_state.user_email,
    currency="EUR",
    payment_method="stripe"
)

# El resultado incluirá payment_id
if result and 'payment_id' in result:
    print(f"Payment ID: {result['payment_id']}")
```

---

## 🔧 Ajustes Necesarios en el Workflow

Según tu schema de Supabase, asegúrate de que tu workflow de n8n:

### 1. Para `usage_stats`:
- El campo `action_type` debe ser uno de:
  - `audio_guide` (no `get_audio_guide`)
  - `poi_view`
  - `search`
  - `booking`
  - etc.

### 2. Para `bookings`:
- Usa `payment_id` (no `payment_intent_id`)
- Incluye `currency` (EUR, USD, etc.)
- El `payment_id` debe ser el ID del PaymentIntent de Stripe

### 3. Confirmación de Reserva:
- Cuando Stripe confirme el pago (`payment_intent.succeeded`), actualiza:
  ```json
  {
    "status": "confirmed",
    "payment_id": "{{stripe_payment_intent_id}}"
  }
  ```

---

## 🧪 Script de Prueba

He creado un script para probar tu webhook:

```bash
python test_n8n.py
```

Este script probará:
- ✅ Recomendaciones de POIs
- ✅ Generación de audio-guías
- ✅ Creación de reservas

---

## 📝 Configuración en Streamlit

La aplicación ya está configurada para usar tu webhook:

**Archivo:** `.env`
```env
N8N_WEBHOOK_URL=https://n8n.yamboly.lat/webhook-test/tourist-guide
```

**Archivo:** `config.py`
```python
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "https://n8n.yamboly.lat/webhook-test/tourist-guide")
```

---

## 🚀 Cómo Usar en la Aplicación

### 1. Iniciar la Aplicación
```bash
streamlit run app.py
```

### 2. Probar Recomendaciones
1. Ve a "📍 Puntos de Interés"
2. Selecciona una ciudad (Barcelona)
3. El sistema llamará automáticamente a n8n para obtener recomendaciones

### 3. Generar Audio-Guía
1. Ve a "🎧 Audio-Guías"
2. Selecciona un POI
3. Configura idioma y voz
4. Haz clic en "Generar Audio-Guía"
5. n8n procesará la solicitud con OpenAI + ElevenLabs

### 4. Crear Reserva
1. Ve a "🎫 Mis Reservas"
2. Crea una nueva reserva
3. Completa los datos
4. Al confirmar, n8n procesará el pago con Stripe
5. Recibirás el `payment_id` en la respuesta

---

## 🐛 Solución de Problemas

### Error: "Connection refused"
- Verifica que n8n esté ejecutándose
- Verifica la URL del webhook

### Error: "Timeout"
- El workflow de n8n puede estar tardando mucho
- Aumenta el timeout en `n8n_integration.py`

### Error: "Invalid action_type"
- Verifica que el `action_type` coincida con tu workflow
- Opciones válidas:
  - `get_poi_recommendations`
  - `audio_guide`
  - `booking`

### La respuesta no tiene `payment_id`
- Verifica que Stripe esté configurado en n8n
- Verifica que el nodo de Stripe esté creando el PaymentIntent
- El `payment_id` debe venir del campo `id` del PaymentIntent

---

## 📊 Monitoreo

### Ver Logs de n8n
1. Abre n8n: `https://n8n.yamboly.lat`
2. Ve a "Executions"
3. Revisa las ejecuciones del workflow

### Ver Logs de Streamlit
- Los errores se mostrarán en la terminal donde ejecutaste `streamlit run app.py`
- También se mostrarán en la interfaz de la aplicación

---

## ✅ Checklist de Verificación

- [x] URL del webhook configurada
- [x] Endpoint de recomendaciones funcionando
- [ ] OpenAI API configurada en n8n
- [ ] ElevenLabs API configurada en n8n
- [ ] Stripe API configurada en n8n
- [ ] Google Maps API configurada en n8n

---

## 📞 Próximos Pasos

1. **Configura las APIs en n8n:**
   - OpenAI para generar texto
   - ElevenLabs para convertir a audio
   - Stripe para procesar pagos
   - Google Maps para búsquedas

2. **Prueba cada endpoint:**
   ```bash
   python test_n8n.py
   ```

3. **Usa la aplicación:**
   ```bash
   streamlit run app.py
   ```

---

**¡Tu integración con n8n está lista! 🎉**
