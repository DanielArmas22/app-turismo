# 🔧 Guía de Solución de Problemas

## Error: "Failed to load resource: net::ERR_NAME_NOT_RESOLVED"

Este error indica que el navegador no puede resolver el nombre de dominio del servidor n8n.

### Posibles Causas y Soluciones:

#### 1. **El servidor n8n no está activo**
- ✅ Verifica que n8n esté ejecutándose en `https://n8n.yamboly.lat`
- ✅ Prueba acceder directamente a la URL en tu navegador
- ✅ Revisa los logs del servidor n8n

#### 2. **Problema de DNS**
- ✅ Verifica que el dominio `n8n.yamboly.lat` esté correctamente configurado
- ✅ Prueba hacer ping al dominio: `ping n8n.yamboly.lat`
- ✅ Verifica la configuración DNS de tu proveedor

#### 3. **Certificado SSL**
- ✅ Verifica que el certificado SSL esté válido y no haya expirado
- ✅ Si usas Let's Encrypt, renueva el certificado si es necesario

#### 4. **Firewall o Proxy**
- ✅ Verifica que no haya un firewall bloqueando la conexión
- ✅ Si estás detrás de un proxy corporativo, configúralo correctamente

### Prueba Manual del Webhook

Puedes probar el webhook directamente con curl:

```bash
curl -X POST https://n8n.yamboly.lat/webhook/tourist-guide \
  -H "Content-Type: application/json" \
  -d '{
    "action_type": "get_poi_recommendations",
    "lat": 41.4036,
    "lng": 2.1744,
    "city_id": "tu-city-id",
    "user_id": "test-user",
    "timestamp": "2025-11-06T20:00:00Z"
  }'
```

### Respuesta Esperada

El webhook debe devolver un JSON con este formato:

```json
{
  "recommendations": [
    {
      "id": "poi-id",
      "name": "Nombre del lugar",
      "latitude": 41.4036,
      "longitude": 2.1744,
      "rating": 4.5,
      "category": "Histórico",
      "description": "Descripción...",
      "distance": 1.5,
      "score": 0.85
    }
  ]
}
```

O formato alternativo:

```json
{
  "pois": [...]
}
```

## Error: "Expecting value: line 1 column 1 (char 0)"

Este error indica que el servidor respondió pero no con JSON válido.

### Posibles Causas:

1. **Respuesta vacía**: El servidor devolvió una respuesta vacía
2. **Respuesta HTML**: El servidor devolvió HTML en lugar de JSON (posible página de error)
3. **Workflow no configurado**: El workflow de n8n no está devolviendo datos

### Solución:

1. Revisa los logs del workflow en n8n
2. Verifica que el workflow tenga un nodo "Respond to Webhook" configurado
3. Asegúrate de que el workflow esté activo
4. Prueba el workflow manualmente en n8n

## Modo Fallback

Si n8n no está disponible, la aplicación automáticamente:
- ✅ Muestra un mensaje de error claro
- ✅ Ofrece soluciones posibles
- ✅ Carga lugares desde la base de datos local de Supabase
- ✅ Calcula distancias usando coordenadas
- ✅ Muestra los lugares en el mapa

## Configuración de Variables de Entorno

Verifica tu archivo `.env`:

```env
SUPABASE_URL=https://eaxnurtyjkkwllodyppb.supabase.co
SUPABASE_KEY=tu-clave-supabase
N8N_WEBHOOK_URL=https://n8n.yamboly.lat/webhook/tourist-guide
```

## Contacto de Soporte

Si el problema persiste:
1. Revisa los logs de la aplicación
2. Revisa los logs de n8n
3. Verifica la conectividad de red
4. Contacta al administrador del servidor
