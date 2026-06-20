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

## 9. Error de Alineación en Flet (ft.alignment.center)
**Severidad sugerida:** Baja

### Descripción
Al intentar alinear elementos usando `ft.alignment.center` (ej. en modales o vistas de reporte), la aplicación arroja un error `AttributeError: module 'flet.controls.alignment' has no attribute 'center'`. Esto se debe a diferencias en la API de alineación de Flet según la versión.

### Solución / Acción recomendada
Reemplazar cualquier uso de `ft.alignment.center` u otros atributos estáticos de alineación que fallen por sus equivalentes como objeto de clase: `ft.Alignment(0, 0)` para centrar. Ya fue aplicado en `modals_jira.py`.

## 10. API Incompatible de FilePicker (on_result)
**Severidad sugerida:** Baja

### Descripción
Al intentar crear un `ft.FilePicker` pasando el argumento `on_result` en el constructor, Flet v0.8.x arroja `TypeError: FilePicker.__init__() got an unexpected keyword argument 'on_result'`.

### Solución / Acción recomendada
Instanciar el `FilePicker` sin el argumento y asignar el callback posteriormente a la propiedad (`picker.on_result = callback`). Fue corregido en los modales de `forms.py`.

## 11. Error "Unknown control: FilePicker" en Flet v0.80.x
**Severidad sugerida:** Media

### Descripción
Al intentar abrir el modal de reportes, Flet lanza un error interno en el cliente de Flutter indicando `Unknown control: FilePicker`. Esto se debe a que en versiones recientes, el componente `FilePicker` fue extraído o requiere inicialización asíncrona diferente que rompe el entorno local actual.

### Solución / Acción recomendada
Se eliminó la dependencia de `ft.FilePicker` por completo. Como es una aplicación de escritorio local, se implementó en su lugar un diálogo nativo de Windows usando `tkinter.filedialog` el cual no presenta conflictos con la UI y es 100% estable.

## 12. Atributo faltante en enum de Flet (ft.ImageFit)
**Severidad sugerida:** Baja

### Descripción
Al intentar renderizar una imagen con el ajuste de Flet (ej. `fit=ft.ImageFit.COVER`), la librería arroja el error `AttributeError: module 'flet' has no attribute 'ImageFit'`. Esto ocurre porque versiones de Flet no incluyen ciertas enumeraciones que antes o después sí existen en el API.

### Solución / Acción recomendada
Pasar directamente la cadena de texto (ej. `fit="cover"`) en lugar del objeto `ImageFit` del framework, lo cual está soportado universalmente y no rompe la ejecución. Se ha aplicado en la visualización de la galería de medios.

## 13. Desaparición del Sidebar por Imagen Local Absoluta
**Severidad sugerida:** Alta

### Descripción
Si se proporciona una ruta absoluta local a la propiedad `src` de un `ft.Image` (ej. `C:\ruta\imagen.png`), el control falla en el cliente de Flutter ya que por seguridad Flet solo sirve archivos desde su carpeta de *assets* configurada. Este error de renderizado en cascada hace que todo el contenedor padre (en este caso el Sidebar o menú) desaparezca por completo sin dejar rastro en la consola de Python.

### Solución / Acción recomendada
Convertir la imagen a Base64 usando Python (`base64.b64encode`) y pasarlo al parámetro `src` del control `ft.Image` utilizando el formato Data URI (`src="data:image/png;base64,..."`). Se debe evitar el uso de la propiedad `src_base64` ya que la misma no existe en el constructor de Flet v0.80.5 y rompe el generador de UI silenciosamente. Ya implementado en el header de `components.py`.
