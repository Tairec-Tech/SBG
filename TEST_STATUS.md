# TEST_STATUS.md

## Estado actual de pruebas del proyecto SBE

## Veredicto actual sugerido

Aprobado condicional para uso académico/local

No debe afirmarse “listo para producción” mientras sigan abiertos los defectos altos ya detectados.

## Casos y evidencias importantes

### CU-01 — Autenticación y Control de Acceso
**Estado:** Parcialmente documentado con buenas capturas

#### Evidencias ya identificadas
- Dashboard posterior a login exitoso con usuario directivo
- Modal de error por login fallido
- Formulario de registro lleno
- Evidencia en BD de usuario legacy (`profesor1`)

#### Evidencias que todavía conviene obtener
- Resultado exitoso del registro
- Login exitoso del usuario legacy `profesor1`

### CU-02 — Gestión de Brigadas
Capturas recomendadas:
- formulario de creación de brigada
- vista con brigada creada
- edición de brigada
- intento de eliminación con dependencias y mensaje resultante

### CU-03 — Gestión de Usuarios / Brigadistas
Nota importante: no documentar el caso como si existiera `crud_brigadista.py` independiente.

Capturas recomendadas:
- registro de usuario/brigadista
- tabla/listado con nuevo registro
- filtro por brigada aplicado

### CU-04 — Actividades
Capturas recomendadas:
- formulario de creación
- actividad visible en listado/dashboard
- cambio de estado antes/después
- KPI actualizado si es posible

### CU-05 — Turnos y Horarios
Capturas recomendadas:
- formulario de turno
- grilla con turno creado
- edición de turno reflejada

### CU-06 — Reportes
Capturas recomendadas:
- creación de reporte de incidente
- exportación a Word
- archivo generado
- reportes de impacto
- reportes de actividades

### CU-07 — Estadísticas e Indicadores
Capturas recomendadas:
- pantalla completa de estadísticas con gráficos
- dashboard con KPIs

### CU-08 — Utilidades
Capturas recomendadas:
- Acerca de
- Importar/Exportar BD
- diferencia por rol en utilidades
- Manual de Usuario
- Información Legal

### CU-09 — Registro institucional
Capturas recomendadas:
- formulario de registro institucional
- resultado exitoso
- edición posterior solo si realmente existe y fue probada

## Convención sugerida de nombres de imágenes

- `CU01_Login_exitoso_01.png`
- `CU01_Login_exitoso_02_dashboard.png`
- `CU01_Login_invalido_modal.png`
- `CU01_Registro_usuario_formulario.png`
- `CU01_Registro_usuario_exito.png`
- `CU01_Legacy_hash_bd.png`
- `CU01_Legacy_login_ok.png`

## Observación estratégica

En el informe final conviene poner imágenes de:
- resultado observable
- evidencia de error o restricción
- archivos exportados
- diferencias por rol

No conviene saturar el documento con capturas redundantes de formularios vacíos o pantallas repetidas.
