# 🔧 Instrucciones para Corregir Políticas RLS

## ⚠️ Problema

Si recibes el error:
```
Error al crear usuario: {'message': 'new row violates row-level security policy for table "users"', 'code': '42501'}
```

Esto significa que las políticas RLS (Row Level Security) están bloqueando la inserción de usuarios porque están configuradas para usar `auth.uid()` de Supabase Auth, pero la aplicación usa un sistema de autenticación simple basado en email.

## ✅ Solución

### Paso 1: Acceder a Supabase

1. Ve a tu proyecto en Supabase: https://supabase.com/dashboard
2. Selecciona tu proyecto
3. Ve a **SQL Editor** en el menú lateral

### Paso 2: Ejecutar el Script SQL

1. Abre el archivo `fix_rls_policies.sql` que está en la raíz del proyecto
2. Copia todo el contenido del archivo
3. Pégalo en el SQL Editor de Supabase
4. Haz clic en **Run** o presiona `Ctrl+Enter`

### Paso 3: Verificar

El script actualizará las políticas RLS para permitir:
- ✅ Creación de usuarios sin autenticación de Supabase Auth
- ✅ Lectura y actualización de usuarios
- ✅ Operaciones CRUD en todas las tablas sin restricciones de autenticación

### ⚠️ Nota de Seguridad

**IMPORTANTE:** Las políticas actualizadas permiten operaciones públicas. En producción, deberías:

1. Implementar autenticación adecuada (Supabase Auth o JWT)
2. Restringir las políticas RLS según roles de usuario
3. Usar políticas más específicas que validen permisos

Para desarrollo y pruebas, las políticas actuales son suficientes.

## 📋 Políticas Actualizadas

El script actualiza las políticas para las siguientes tablas:

- ✅ `users` - Permite CRUD completo
- ✅ `user_visits` - Permite lectura y creación
- ✅ `user_achievements` - Permite lectura y creación
- ✅ `bookings` - Permite CRUD completo
- ✅ `favorites` - Permite CRUD completo
- ✅ `usage_stats` - Permite lectura y creación

Las tablas públicas (`cities`, `points_of_interest`, `audio_guides`) ya tienen políticas que permiten lectura pública.

## 🔄 Después de Ejecutar el Script

1. Recarga la aplicación Streamlit
2. Intenta crear un nuevo usuario
3. Debería funcionar sin errores

Si aún tienes problemas, verifica:
- ✅ Que el script se ejecutó correctamente
- ✅ Que no hay errores en la consola de Supabase
- ✅ Que las políticas se crearon correctamente (puedes verificar en **Authentication > Policies**)

