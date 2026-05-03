# KNOWN_ISSUES.md

## Defectos y riesgos conocidos del proyecto SBE

## 1. Inconsistencia de variables de entorno
**Severidad sugerida:** Alta

### Descripción
El código de configuración usa variables con prefijo `SBE_DB_*`, pero versiones previas de `.env.example` o documentación han usado otros nombres como `SBG_DB_*`.

### Riesgo
La aplicación puede fallar al conectar a la base de datos si el desarrollador sigue la plantilla equivocada.

### Acción recomendada
Unificar definitivamente:
- código
- `.env.example`
- documentación
- README

## 2. Recuperación de contraseña insegura
**Severidad sugerida:** Alta

### Descripción
El flujo de recuperación puede generar una contraseña temporal y mostrarla directamente en pantalla.

### Acción recomendada
Reemplazar el flujo por:
- token de recuperación
- envío por correo
- expiración temporal
- confirmación segura

## 3. Persistencia de sesión inconsistente
**Severidad sugerida:** Media/Alta

### Descripción
El sistema mezcla mecanismos distintos para persistir o leer la sesión, incluyendo `SharedPreferences` y `client_storage`.

### Acción recomendada
Definir una sola fuente de verdad para la sesión y refactorizar todas las lecturas/escrituras.

## 4. Hardcodes de `institucion_id = 1`
**Severidad sugerida:** Alta

### Descripción
Existen consultas o flujos con hardcodes o fallbacks tipo `institucion_id or 1`.

### Acción recomendada
Eliminar hardcodes y obligar a que el `institucion_id` venga del contexto válido del usuario autenticado.

## 5. Registro institucional sin transacción completa
**Severidad sugerida:** Media/Alta

### Descripción
El flujo que crea institución y usuario administrador/directivo no siempre está envuelto en una transacción atómica completa.

### Acción recomendada
Aplicar transacción con rollback total.

## 6. Permisos inconsistentes en algunas pantallas
**Severidad sugerida:** Media

### Descripción
No todas las pantallas parecen validar permisos con la misma rigurosidad, especialmente en algunos flujos de reportes.

### Acción recomendada
Centralizar validación de permisos y no depender solo de ocultar botones en UI.

## 7. Backup/restauración acoplado al entorno local
**Severidad sugerida:** Media

### Descripción
La funcionalidad de exportar/importar BD asume herramientas y rutas locales específicas.

### Acción recomendada
Tomar parámetros desde configuración, validar binarios y manejar errores de forma más robusta.

## 8. Documentación histórica desalineada
**Severidad sugerida:** Media

### Descripción
Documentos viejos hablan de SBG, brigadas ambientales solamente o módulos que ya no representan el repo actual.

### Acción recomendada
Mantener solo documentación unificada bajo:
- nombre SBE
- 4 brigadas escolares
- módulos reales del software
