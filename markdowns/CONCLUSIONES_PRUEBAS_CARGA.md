# Conclusiones de Pruebas de Carga, Estrés y Rendimiento

## Resumen Ejecutivo

Este documento presenta los resultados y conclusiones obtenidas de las pruebas de carga, estrés, potencia y rendimiento realizadas sobre la aplicación de Guía Turística Virtual utilizando Apache JMeter. El objetivo principal fue determinar el número máximo de usuarios conectados simultáneamente mediante pruebas iterativas.

---

## 1. Metodología de Pruebas

### 1.1 Configuración de las Pruebas

Las pruebas se dividieron en dos escenarios principales:

**Grupo 1: Pruebas de Carga Base**
- **Usuarios simultáneos:** 10 usuarios
- **Tiempo de rampa:** 30 segundos
- **Duración:** 120 segundos
- **Objetivo:** Evaluar el comportamiento bajo carga normal

**Grupo 2: Pruebas de Estrés**
- **Usuarios simultáneos:** 50 usuarios
- **Tiempo de rampa:** 60 segundos
- **Duración:** 300 segundos
- **Objetivo:** Determinar el punto de falla y capacidad máxima

### 1.2 Endpoints Evaluados

1. **Frontend Streamlit:**
   - Página Principal (`/`)
   - Página Explorar Ciudades (`/cities`)

2. **API Supabase (Backend):**
   - GET Ciudades (`/rest/v1/cities`)
   - GET Puntos de Interés (`/rest/v1/points_of_interest`)

3. **Integración n8n:**
   - Webhook de Recomendaciones (`/webhook/tourist-guide`)

---

## 2. Resultados Obtenidos

### 2.1 Métricas Generales

| Métrica | Valor Total |
|---------|-------------|
| **Total de Muestras** | 1,127 requests |
| **Tiempo Promedio de Respuesta** | 144 ms |
| **Tiempo Mínimo** | 1 ms |
| **Tiempo Máximo** | 1,167 ms |
| **Desviación Estándar** | 133.72 ms |
| **Tasa de Error** | 0.621% |
| **Throughput** | 18.80 requests/minuto |
| **KB Recibidos/segundo** | 77.21 KB/s |
| **KB Enviados/segundo** | 12.73 KB/s |

### 2.2 Análisis por Componente

#### 2.2.1 Frontend Streamlit

**Página Principal:**
- ✅ **Muestras:** 341 requests
- ✅ **Tiempo promedio:** 8 ms
- ✅ **Tiempo mínimo:** 1 ms
- ✅ **Tiempo máximo:** 99 ms
- ✅ **Desviación estándar:** 8.21 ms
- ✅ **Tasa de error:** 0.000%
- ✅ **Throughput:** 5.71 requests/minuto
- ✅ **Estado:** **ÓPTIMO** - Sin errores, respuesta rápida y estable

**Página Explorar Ciudades:**
- ✅ **Muestras:** 85 requests
- ✅ **Tiempo promedio:** 2 ms
- ✅ **Tiempo mínimo:** 1 ms
- ✅ **Tiempo máximo:** 6 ms
- ✅ **Desviación estándar:** 1.12 ms
- ✅ **Tasa de error:** 0.000%
- ✅ **Throughput:** 1.46 requests/minuto
- ✅ **Estado:** **ÓPTIMO** - Excelente rendimiento, respuesta casi instantánea

**Conclusión Frontend:** El frontend desarrollado con Streamlit demuestra excelente capacidad de escalabilidad, manteniendo tiempos de respuesta muy bajos (2-8 ms promedio) y sin errores incluso bajo carga de 50 usuarios simultáneos. La desviación estándar baja indica comportamiento consistente y predecible.

#### 2.2.2 API Supabase (Backend)

**GET Ciudades (Grupo 1 - 10 usuarios):**
- ✅ **Muestras:** 236 requests
- ✅ **Tiempo promedio:** 229 ms
- ✅ **Tiempo mínimo:** 127 ms
- ✅ **Tiempo máximo:** 751 ms
- ✅ **Desviación estándar:** 92.94 ms
- ⚠️ **Tasa de error:** 0.424% (1 error de 236 requests)
- ✅ **Throughput:** 4.14 requests/minuto
- ✅ **Estado:** **EXCELENTE** - Funcionamiento correcto tras corrección de autenticación

**GET Ciudades (Grupo 2 - 50 usuarios):**
- ✅ **Muestras:** 84 requests
- ✅ **Tiempo promedio:** 248 ms
- ✅ **Tiempo mínimo:** 128 ms
- ✅ **Tiempo máximo:** 1,167 ms
- ⚠️ **Desviación estándar:** 158.57 ms (mayor variabilidad bajo carga alta)
- ⚠️ **Tasa de error:** 1.190% (1 error de 84 requests)
- ✅ **Throughput:** 1.45 requests/minuto
- ✅ **Estado:** **BUENO** - Funciona correctamente bajo carga alta, con ligera degradación

**GET POIs:**
- ✅ **Muestras:** 81 requests
- ✅ **Tiempo promedio:** 209 ms
- ✅ **Tiempo mínimo:** 51 ms
- ✅ **Tiempo máximo:** 358 ms
- ✅ **Desviación estándar:** 53.25 ms
- ⚠️ **Tasa de error:** 1.235% (1 error de 81 requests)
- ✅ **Throughput:** 1.46 requests/minuto
- ✅ **Estado:** **BUENO** - Rendimiento estable y consistente

**Análisis:** Tras la corrección de los headers de autenticación, las consultas a Supabase funcionan correctamente. Los tiempos de respuesta (209-248 ms) son aceptables para consultas a base de datos. Se observa una ligera degradación bajo carga alta (Grupo 2), pero el sistema mantiene funcionalidad con menos del 2% de errores. La variabilidad aumenta bajo carga alta, lo cual es esperado.

#### 2.2.3 Integración n8n

**Webhook Recomendaciones (Grupo 1 - 10 usuarios):**
- ✅ **Muestras:** 222 requests
- ✅ **Tiempo promedio:** 228 ms
- ✅ **Tiempo mínimo:** 14 ms
- ✅ **Tiempo máximo:** 477 ms
- ⚠️ **Desviación estándar:** 101.29 ms
- ⚠️ **Tasa de error:** 1.802% (4 errores de 222 requests)
- ✅ **Throughput:** 4.07 requests/minuto
- ✅ **Estado:** **ACEPTABLE** - Funciona correctamente con bajo porcentaje de errores

**Webhook Recomendaciones (Grupo 2 - 50 usuarios):**
- ✅ **Muestras:** 78 requests
- ✅ **Tiempo promedio:** 215 ms
- ✅ **Tiempo mínimo:** 150 ms
- ✅ **Tiempo máximo:** 489 ms
- ✅ **Desviación estándar:** 83.78 ms
- ✅ **Tasa de error:** 0.000%
- ✅ **Throughput:** 1.44 requests/minuto
- ✅ **Estado:** **EXCELENTE** - Mejor rendimiento bajo carga alta, sin errores

**Conclusión n8n:** La integración con n8n muestra un comportamiento robusto y estable. Curiosamente, bajo carga alta (Grupo 2) el rendimiento mejora (0% errores vs 1.8% en Grupo 1), lo que sugiere que el sistema se estabiliza después del período inicial. Los tiempos de respuesta (~215-228 ms) son aceptables para operaciones que involucran procesamiento de IA y consultas externas.

---

## 3. Análisis de Capacidad y Escalabilidad

### 3.1 Número Máximo de Usuarios Simultáneos

Basado en los resultados obtenidos:

#### **Capacidad Confirmada:**

**✅ Frontend Streamlit:**
- **Usuarios simultáneos soportados:** ≥ 50 usuarios
- **Tasa de éxito:** 100%
- **Tiempo promedio:** 2-8 ms
- **Estado:** Estable sin degradación de rendimiento
- **Límite estimado:** Probablemente > 100 usuarios (requiere pruebas adicionales)

**✅ API Supabase:**
- **Usuarios simultáneos soportados:** ≥ 50 usuarios
- **Tasa de éxito:** 98.81-99.58%
- **Tiempo promedio:** 209-248 ms
- **Estado:** Funcional con errores mínimos (< 2%)
- **Límite estimado:** Probablemente 75-100 usuarios simultáneos antes de degradación significativa

**✅ Integración n8n:**
- **Usuarios simultáneos soportados:** ≥ 50 usuarios
- **Tasa de éxito:** 98.20-100%
- **Tiempo promedio:** 215-228 ms
- **Estado:** Estable, mejora bajo carga alta
- **Límite estimado:** Probablemente > 100 usuarios (requiere pruebas adicionales)

### 3.2 Punto de Degradación

**Frontend Streamlit:**
- No se observó degradación significativa hasta 50 usuarios simultáneos
- Los tiempos de respuesta se mantuvieron consistentes (2-8 ms)
- No se detectaron errores
- **Conclusión:** No se alcanzó el punto de degradación

**API Supabase:**
- Ligera degradación en tiempos de respuesta al aumentar de 10 a 50 usuarios (229 ms → 248 ms)
- Aumento en tasa de errores (0.424% → 1.190%)
- Aumento en variabilidad (desviación estándar: 92.94 ms → 158.57 ms)
- **Conclusión:** Degradación moderada pero aceptable

**Integración n8n:**
- Mejora en tiempos de respuesta bajo carga alta (228 ms → 215 ms)
- Reducción en tasa de errores (1.802% → 0.000%)
- Reducción en variabilidad (101.29 ms → 83.78 ms)
- **Conclusión:** Sistema se estabiliza y mejora bajo carga sostenida

---

## 4. Identificación de Cuellos de Botella

### 4.1 Cuellos de Botella Identificados

1. **API Supabase (MENOR):**
   - Tiempos de respuesta más altos (209-248 ms) comparado con otros componentes
   - Ligera degradación bajo carga alta
   - Aceptable dado que son consultas a base de datos
   - No representa un cuello de botella crítico

2. **Integración n8n (MENOR):**
   - Tiempos de respuesta moderados (~215-228 ms)
   - Aceptable dado el procesamiento complejo que realiza (IA, consultas externas)
   - Mejora bajo carga alta, lo que indica buena capacidad de escalamiento
   - No representa un cuello de botella crítico

### 4.2 Componentes Sin Problemas

- ✅ **Frontend Streamlit:** Excelente rendimiento sin cuellos de botella detectados
- ✅ **Navegación de páginas:** Respuesta casi instantánea (2-8 ms)
- ✅ **Sistema completo:** Funciona correctamente con tasa de error total < 1%

---

## 5. Recomendaciones

### 5.1 Optimizaciones Recomendadas

1. **Para Supabase:**
   - Implementar caché para consultas frecuentes (ciudades, POIs)
   - Optimizar índices en la base de datos para reducir tiempos de respuesta
   - Considerar uso de connection pooling
   - Implementar retry logic con backoff exponencial para manejar errores ocasionales

2. **Para n8n:**
   - El sistema ya muestra buen comportamiento, pero se puede optimizar:
   - Implementar caché para recomendaciones similares
   - Monitorear uso de recursos del servidor n8n bajo carga
   - Considerar escalamiento horizontal si se requiere más capacidad

3. **Para el Sistema Completo:**
   - Implementar load balancing si se requiere escalar más allá de 100 usuarios
   - Considerar CDN para assets estáticos del frontend
   - Implementar monitoreo en tiempo real de métricas de rendimiento
   - Establecer alertas para tasas de error > 2%

### 5.2 Pruebas Adicionales Recomendadas

1. **Pruebas de Resistencia (Endurance):**
   - Ejecutar pruebas durante períodos prolongados (1-2 horas)
   - Identificar posibles memory leaks o degradación gradual
   - Evaluar estabilidad a largo plazo

2. **Pruebas de Spike:**
   - Evaluar comportamiento ante aumentos súbitos de carga
   - Simular picos de tráfico realistas
   - Determinar capacidad de recuperación

3. **Pruebas de Volumen:**
   - Incrementar gradualmente hasta encontrar el punto de falla real
   - Probar con 75, 100, 150 usuarios simultáneos
   - Determinar límite máximo con todos los componentes funcionando

4. **Pruebas de Escalabilidad Horizontal:**
   - Evaluar comportamiento con múltiples instancias
   - Determinar beneficios de arquitectura distribuida
   - Probar con load balancer

---

## 6. Conclusiones Finales

### 6.1 Capacidad del Sistema

**Basado en los componentes evaluados:**

- **Frontend Streamlit:** ✅ **Capacidad confirmada ≥ 50 usuarios simultáneos** (100% éxito)
- **API Supabase:** ✅ **Capacidad confirmada ≥ 50 usuarios simultáneos** (98.81-99.58% éxito)
- **Integración n8n:** ✅ **Capacidad confirmada ≥ 50 usuarios simultáneos** (98.20-100% éxito)

### 6.2 Número Máximo de Usuarios Simultáneos

**Conclusión Basada en Resultados:**

El sistema completo puede soportar **al menos 50 usuarios simultáneos** con un rendimiento excelente:

- **Tasa de éxito general:** 99.38% (solo 0.621% de errores)
- **Tiempo promedio de respuesta:** 144 ms
- **Throughput:** 18.80 requests/minuto
- **Todos los componentes funcionando correctamente**

**Estimación Conservadora:**
Basado en la degradación moderada observada en Supabase bajo carga alta, se estima que el sistema puede soportar:
- **Mínimo confirmado:** 50 usuarios simultáneos
- **Estimado seguro:** 75 usuarios simultáneos
- **Estimado óptimo:** 100 usuarios simultáneos (requiere pruebas adicionales)

**Estimación Optimista:**
Considerando que:
- El frontend no muestra degradación
- n8n mejora bajo carga alta
- Supabase tiene degradación moderada pero aceptable

Se estima que el sistema podría soportar:
- **Máximo estimado:** 100-150 usuarios simultáneos (requiere pruebas adicionales con incremento gradual)

### 6.3 Limitaciones Identificadas

1. **Limitación Menor:** Degradación moderada en Supabase bajo carga alta (tiempos aumentan de 229 ms a 248 ms)
2. **Limitación Menor:** Variabilidad aumentada en tiempos de respuesta bajo carga alta
3. **Limitación Potencial:** No se evaluó el comportamiento bajo carga sostenida prolongada (> 5 minutos)

### 6.4 Fortalezas del Sistema

1. ✅ **Frontend robusto:** Excelente rendimiento sin errores (100% éxito)
2. ✅ **Backend funcional:** Supabase funciona correctamente con errores mínimos (< 2%)
3. ✅ **Integración estable:** n8n mantiene bajo porcentaje de errores y mejora bajo carga
4. ✅ **Arquitectura escalable:** Componentes independientes permiten escalamiento selectivo
5. ✅ **Tiempos de respuesta aceptables:** En general, el sistema responde rápidamente (< 250 ms promedio)
6. ✅ **Alta disponibilidad:** Tasa de éxito general del 99.38%

---

## 7. Métricas Clave para el Artículo

### 7.1 Rendimiento del Frontend

- **Tiempo promedio de respuesta:** 2-8 ms
- **Tasa de éxito:** 100%
- **Throughput:** 5.71 requests/minuto (página principal)
- **Usuarios simultáneos soportados:** ≥ 50
- **Desviación estándar:** 1.12-8.21 ms (muy baja, indica consistencia)

### 7.2 Rendimiento del Backend (Supabase)

- **Tiempo promedio de respuesta:** 209-248 ms
- **Tasa de éxito:** 98.81-99.58%
- **Throughput:** 1.45-4.14 requests/minuto
- **Usuarios simultáneos soportados:** ≥ 50
- **Desviación estándar:** 53.25-158.57 ms (moderada, aumenta bajo carga)

### 7.3 Rendimiento de Integraciones (n8n)

- **Tiempo promedio de respuesta:** 215-228 ms
- **Tasa de éxito:** 98.20-100%
- **Throughput:** 1.44-4.07 requests/minuto
- **Usuarios simultáneos soportados:** ≥ 50
- **Desviación estándar:** 83.78-101.29 ms (moderada, mejora bajo carga)

### 7.4 Métricas Generales del Sistema

- **Throughput total:** 18.80 requests/minuto
- **Tiempo promedio total:** 144 ms
- **Tasa de éxito total:** 99.38%
- **Tasa de error total:** 0.621%
- **Ancho de banda recibido:** 77.21 KB/s
- **Ancho de banda enviado:** 12.73 KB/s
- **Total de muestras:** 1,127 requests
- **Usuarios simultáneos probados:** 10 y 50 usuarios

---

## 8. Trabajo Futuro

1. **Pruebas extendidas:** Evaluar sistema con 75, 100, 150 usuarios simultáneos
2. **Pruebas de resistencia:** Ejecutar pruebas durante períodos prolongados (1-2 horas)
3. **Optimización:** Implementar mejoras identificadas (caché, índices, etc.)
4. **Monitoreo:** Establecer sistema de monitoreo en producción
5. **Documentación:** Documentar procedimientos de escalamiento y optimización
6. **Análisis de límites:** Determinar punto exacto de falla mediante incremento gradual

---

## Referencias de la Prueba

- **Herramienta:** Apache JMeter 5.6.3
- **Fecha de ejecución:** [Fecha de ejecución de las pruebas]
- **Configuración:** 2 grupos de usuarios (10 y 50 usuarios simultáneos)
- **Duración total:** ~420 segundos (7 minutos)
- **Total de muestras:** 1,127 requests
- **Estado:** Pruebas completadas exitosamente con configuración corregida

---

**Nota:** Este documento refleja los resultados obtenidos tras la corrección de los headers de autenticación de Supabase. El sistema muestra excelente rendimiento con una tasa de éxito del 99.38% y capacidad confirmada para al menos 50 usuarios simultáneos.
