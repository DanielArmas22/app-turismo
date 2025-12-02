# 📊 Instrucciones para Pruebas de Carga con JMeter

## 📋 División de Trabajo

### **Persona 1** - Parte 1: Pruebas de Lectura
**Archivo:** `jmeter_pruebas_parte1_streamlit_supabase_read.jmx`

**Responsabilidades:**
- ✅ Pruebas de carga en la aplicación Streamlit (navegación web)
- ✅ Operaciones de lectura en Supabase (GET ciudades, POIs)
- ✅ Webhooks básicos de n8n (recomendaciones)
- ✅ Pruebas de estrés con 10-100 usuarios simultáneos

**Objetivo:** Determinar el máximo de usuarios simultáneos para operaciones de lectura.

---

### **Persona 2** - Parte 2: Pruebas de Escritura y Avanzadas
**Archivo:** `jmeter_pruebas_parte2_supabase_write_n8n_advanced.jmx`

**Responsabilidades:**
- ✅ Operaciones de escritura en Supabase (POST usuarios, estadísticas)
- ✅ Webhooks complejos de n8n (audio-guías, reservas)
- ✅ Escenarios combinados de alta carga
- ✅ Pruebas de potencia máxima (100-200 usuarios)

**Objetivo:** Determinar el máximo de usuarios simultáneos para operaciones de escritura y procesos complejos.

---

## 🚀 Ejecución de las Pruebas

### Requisitos Previos

1. **Instalar JMeter:**
   ```bash
   # Windows (usando Chocolatey)
   choco install jmeter
   
   # O descargar desde: https://jmeter.apache.org/download_jmeter.cgi
   ```

2. **Verificar que la aplicación esté corriendo:**
   ```bash
   # Streamlit debe estar en http://localhost:8501
   streamlit run app.py
   ```

3. **Verificar conectividad:**
   - Supabase: `https://tciaojtfllfqroanvcuz.supabase.co`
   - n8n: `https://n8n.yamboly.lat/webhook/tourist-guide`

---

## 📝 Ejecución - Persona 1

### Paso 1: Ejecutar Pruebas en Modo No-GUI (Recomendado)

```bash
# Navegar a la carpeta del proyecto
cd "C:\RESPALDO LAP\SOFTWARE\APP-TURISMO"

# Ejecutar pruebas
jmeter -n -t jmeter_pruebas_parte1_streamlit_supabase_read.jmx ^
       -l resultados_parte1.jtl ^
       -e -o reporte_parte1/
```

### Paso 2: Ver Resultados

```bash
# Abrir el reporte HTML generado
start reporte_parte1\index.html
```

### Paso 3: Guardar Resultados

Los archivos generados son:
- `resultados_parte1.jtl` - Archivo de resultados (compartir)
- `reporte_parte1/` - Carpeta con reporte HTML (compartir)

---

## 📝 Ejecución - Persona 2

### Paso 1: Ejecutar Pruebas en Modo No-GUI (Recomendado)

```bash
# Navegar a la carpeta del proyecto
cd "C:\RESPALDO LAP\SOFTWARE\APP-TURISMO"

# Ejecutar pruebas
jmeter -n -t jmeter_pruebas_parte2_supabase_write_n8n_advanced.jmx ^
       -l resultados_parte2.jtl ^
       -e -o reporte_parte2/
```

### Paso 2: Ver Resultados

```bash
# Abrir el reporte HTML generado
start reporte_parte2\index.html
```

### Paso 3: Guardar Resultados

Los archivos generados son:
- `resultados_parte2.jtl` - Archivo de resultados (compartir)
- `reporte_parte2/` - Carpeta con reporte HTML (compartir)

---

## 🔗 Combinar Resultados

### Opción 1: Combinar Archivos .jtl

```bash
# Combinar ambos archivos de resultados
copy resultados_parte1.jtl + resultados_parte2.jtl resultados_combinados.jtl

# Generar reporte combinado
jmeter -g resultados_combinados.jtl -o reporte_combinado/
```

### Opción 2: Usar JMeter GUI para Combinar

1. Abrir JMeter GUI:
   ```bash
   jmeter
   ```

2. **File → Open** → Seleccionar `jmeter_pruebas_parte1_streamlit_supabase_read.jmx`

3. Agregar resultados:
   - Click derecho en "Test Plan" → **Add → Listener → Merge Results**
   - Agregar `resultados_parte1.jtl`
   - Agregar `resultados_parte2.jtl`

4. Generar reporte combinado:
   - **File → Save Test Plan As** → `resultados_combinados.jmx`
   - **Tools → Generate HTML Report** → Seleccionar carpeta de salida

---

## 📊 Métricas Clave a Reportar

### Para Cada Prueba:

1. **Usuarios Simultáneos Máximos:**
   - Con tasa de error < 1%
   - Con tiempo de respuesta < 3 segundos

2. **Throughput:**
   - Requests por segundo soportados

3. **Tiempo de Respuesta:**
   - Promedio
   - Mediana (Percentil 50)
   - Percentil 95
   - Percentil 99

4. **Tasa de Error:**
   - Por tipo de operación
   - Por código de estado HTTP

5. **Recursos del Sistema:**
   - CPU utilizada
   - Memoria utilizada
   - Conexiones de red

---

## 📈 Interpretación de Resultados

### ✅ Resultados Exitosos:
- **Tasa de error < 1%**
- **Tiempo de respuesta promedio < 2 segundos**
- **Throughput estable o creciente**

### ⚠️ Señales de Problemas:
- **Tasa de error > 5%** → Sistema sobrecargado
- **Tiempo de respuesta > 5 segundos** → Degradación de rendimiento
- **Throughput que disminuye** → Cuello de botella detectado

### 🚨 Límites Detectados:
- **Tasa de error > 10%** → Máximo de usuarios alcanzado
- **Tiempo de respuesta > 10 segundos** → Sistema no responde adecuadamente
- **Timeouts frecuentes** → Límite de capacidad superado

---

## 🔧 Ajustes Recomendados

### Si las Pruebas Son Muy Lentas:

1. **Reducir número de usuarios:**
   - Editar en JMeter GUI: Thread Group → Number of Threads

2. **Aumentar tiempo de rampa:**
   - Thread Group → Ramp-up Period (segundos)

3. **Reducir duración:**
   - Thread Group → Duration (segundos)

### Si las Pruebas Son Muy Rápidas:

1. **Aumentar número de usuarios:**
   - Incrementar gradualmente: 50 → 100 → 150 → 200

2. **Reducir tiempo de espera:**
   - Constant Timer → Delay (milisegundos)

---

## 📋 Checklist de Ejecución

### Antes de Empezar:
- [ ] JMeter instalado y funcionando
- [ ] Aplicación Streamlit corriendo en localhost:8501
- [ ] Conexión a internet estable
- [ ] Archivo .jmx correspondiente listo

### Durante la Ejecución:
- [ ] Monitorear recursos del sistema (CPU, RAM)
- [ ] Verificar que no haya errores críticos
- [ ] Anotar observaciones sobre comportamiento

### Después de Ejecutar:
- [ ] Guardar archivos .jtl generados
- [ ] Guardar carpetas de reporte HTML
- [ ] Documentar métricas clave
- [ ] Compartir resultados con el equipo

---

## 🆘 Solución de Problemas

### Error: "Address already in use"
```bash
# Verificar qué proceso usa el puerto 8501
netstat -ano | findstr :8501

# Detener proceso si es necesario
taskkill /PID <PID> /F
```

### Error: "Connection refused"
- Verificar que Streamlit esté corriendo
- Verificar firewall/antivirus
- Verificar URL en el archivo .jmx

### Error: "Out of memory"
```bash
# Aumentar memoria de JMeter
set HEAP=-Xms512m -Xmx2048m
jmeter -n -t archivo.jmx -l resultados.jtl
```

### Resultados Inconsistentes
- Ejecutar pruebas múltiples veces
- Promediar resultados
- Verificar condiciones de red

---

## 📞 Contacto y Soporte

Si encuentras problemas durante la ejecución:
1. Revisar logs de JMeter
2. Verificar conectividad de red
3. Consultar documentación de JMeter: https://jmeter.apache.org/usermanual/

---

## ✅ Resultado Final Esperado

Al finalizar ambas pruebas, deberías tener:

1. **Número máximo de usuarios simultáneos:**
   - Para operaciones de lectura: ___ usuarios
   - Para operaciones de escritura: ___ usuarios
   - Para operaciones combinadas: ___ usuarios

2. **Throughput máximo:**
   - Requests/segundo: ___

3. **Tiempo de respuesta:**
   - Promedio: ___ ms
   - Percentil 95: ___ ms

4. **Tasa de error:**
   - En condiciones normales: ___%
   - En condiciones de estrés: ___%

---

**¡Buena suerte con las pruebas! 🚀**

