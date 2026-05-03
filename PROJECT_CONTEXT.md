# PROJECT_CONTEXT.md

## Identidad del proyecto

- Nombre oficial actual: **SBE**
- Significado: **Sistema de Brigadas Escolares**
- Nombre anterior: **SBG**
- Cambio de alcance: el proyecto comenzó orientado a brigadas ambientales, pero evolucionó para cubrir **4 brigadas escolares** definidas por el proyecto actual.
- En toda la documentación nueva debe usarse **SBE** y no SBG, salvo cuando se haga referencia histórica a versiones anteriores.

## Propósito general

SBE es un sistema de escritorio para la gestión de brigadas escolares, construido para administrar usuarios, brigadas, actividades, turnos, reportes, estadísticas, contenido educativo y utilidades del sistema.

## Stack tecnológico

- Lenguaje principal: **Python**
- UI: **Flet 0.80.5**
- Base de datos: **MySQL 8.0**
- Reportes DOCX: **python-docx**
- Gráficos: **flet-charts 0.80.5**
- Entorno objetivo de pruebas: **Windows 11**

## Navegación funcional real detectada

La app contiene o referencia estas áreas funcionales principales:

1. Panel principal / Dashboard
2. Gestión de Brigadas
3. Actividades
4. Usuarios / Brigadistas
5. Turnos y Horarios
6. Reportes de Incidentes
7. Reportes de Impacto
8. Reportes de Actividades
9. Estadísticas
10. Contenido Educativo
11. Utilidades
12. Registro / Login / Recuperación de contraseña

## Roles reales documentados en el sistema

- Directivo
- Coordinador
- Profesor

Nota: en documentos viejos puede aparecer “Docente”. Para documentación técnica alineada con el software actual, conviene usar **Profesor** cuando se hable del rol implementado.

## Hechos importantes ya confirmados

- El sistema sí tiene autenticación y registro.
- El sistema sí usa hashing de contraseñas con PBKDF2 para usuarios nuevos.
- También existe compatibilidad con hashes legacy tipo SHA-256.
- El proyecto no tiene un módulo independiente llamado `crud_brigadista.py` en el estado actual del repo revisado.
- La gestión relacionada con brigadistas/usuarios está absorbida principalmente por otros módulos, especialmente `crud_usuario.py`.
- La documentación corregida debe evitar afirmar que existe ese archivo si no está presente en el software actual.
- La gestión de instituciones no está modelada como un gran módulo CRUD visible equivalente a otros menús principales; aparece más ligada al flujo de registro institucional y configuración inicial.

## Estado general de la auditoría técnica

La revisión del repo mostró que el sistema tiene una base funcional aceptable para uso académico/local, pero no está listo para declararse como producción sin reservas.

### Fortalezas detectadas

- La mayoría de consultas SQL usan parámetros.
- No se detectaron errores generales de sintaxis en los archivos Python revisados.
- El hashing PBKDF2 está implementado para nuevos usuarios.
- Hay estructura modular razonable por pantallas y capa de datos.
- Existen pantallas y funcionalidades suficientes para sostener el plan y reporte de pruebas del proyecto.

### Riesgos y debilidades detectadas

- Inconsistencia en nombres de variables de entorno entre código y `.env.example`.
- Recuperación de contraseña insegura al mostrar contraseña temporal en pantalla.
- Persistencia de sesión inconsistente entre mecanismos distintos.
- Hardcodes y fallbacks de `institucion_id = 1`.
- Registro institucional sin transacción atómica completa.
- Permisos por rol inconsistentes en algunas pantallas de reportes.
- Utilidad de backup/restauración acoplada a entorno local con supuestos frágiles.

## Estado documental

Ya se trabajó en varias versiones de documentos:
- Plan de Pruebas corregido
- Reporte de Pruebas corregido
- versión SBE
- versión fusionada con estructura académica clásica + honestidad técnica

La mejor base actual es la versión fusionada, porque conserva formato universitario tradicional y además integra defectos reales.

## Reglas para futuros chats o asistentes

1. No volver a llamar oficialmente al sistema “SBG” en documentos finales.
2. No reducir el alcance a solo brigadas ambientales.
3. No inventar `crud_brigadista.py`.
4. Si hay contradicción entre documento y código, priorizar el código real.
5. Mantener el veredicto como Aprobado condicional para uso académico/local, salvo que se corrijan los defectos críticos y altos.
6. Cuando se redacten pruebas, usar estructura clásica si el profesor la exige:
   - Escenario
   - Entrada
   - Resultado esperado
   - Resultado obtenido
   - Errores encontrados
   - Sugerencias de corrección
   - Planilla resumen
7. Para capturas de evidencia, priorizar resultados observables y no solo formularios llenos.
