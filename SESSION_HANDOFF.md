# SESSION_HANDOFF.md

## Estado actual del trabajo

Este checkpoint resume el punto exacto en el que quedó el trabajo del proyecto SBE dentro del chat.

## Lo que ya se hizo

1. Se revisó el repo del proyecto subido por el usuario.
2. Se hizo auditoría técnica general del código.
3. Se comparó el software real contra:
   - Plan de Pruebas
   - Reporte de Pruebas
4. Se detectó que los documentos originales no estaban 100% alineados con el software actual.
5. Se corrigieron documentos previos.
6. Después se actualizó el nombre del sistema de SBG a SBE.
7. Finalmente se pidió una fusión estricta entre:
   - la estructura académica clásica del documento original
   - la precisión técnica de la auditoría real

## Resultado documental más importante

Se generó una línea documental donde:
- se mantiene la estructura clásica universitaria
- se usa el nombre SBE
- se asume alcance de 4 brigadas escolares
- se integran defectos reales dentro del reporte
- la evaluación global se deja como:

Aprobado condicional para uso académico/local

## Hallazgos técnicos que deben seguir considerándose verdad

- Hay inconsistencia entre variables esperadas por el código y el `.env.example`.
- El flujo de recuperación de contraseña muestra una contraseña temporal en pantalla.
- Hay inconsistencia entre `SharedPreferences` y `client_storage` para estado de sesión.
- Existen hardcodes/fallbacks con `institucion_id = 1`.
- No existe `crud_brigadista.py` como módulo independiente en el repo actual.
- El backup/restauración depende de supuestos frágiles del entorno local.
- El registro institucional puede dejar datos huérfanos si falla a mitad del flujo.

## Tema de pruebas y capturas

El usuario preguntó qué capturas conviene tomar para el informe.
Se recomendó capturar especialmente:

- Login exitoso
- Login fallido
- Registro de usuario
- Usuario legacy / hash legacy
- Crear brigada
- Error o bloqueo al eliminar brigada con dependencias
- Crear actividad
- Cambiar estado de actividad
- Crear reporte
- Exportar Word
- Pantalla de estadísticas
- Utilidades por rol
- Exportación de BD
- Recuperación de contraseña

Luego el usuario mostró capturas del CU-01 y se concluyó:
- Sí sirven bastante bien.
- Pero faltan dos pruebas para cerrar el CU-01 completo:
  1. resultado exitoso del registro
  2. login exitoso del usuario legacy `profesor1`

## Necesidad actual del usuario

El usuario quiere evitar perder contexto cuando se cae una conversación larga. Para eso se decidió crear este paquete de archivos reutilizables.

## Próximo uso recomendado

Cuando se abra un chat nuevo, compartir:
1. `BOOTSTRAP_PROMPT.md`
2. `PROJECT_CONTEXT.md`
3. `SESSION_HANDOFF.md`

Y si el trabajo es de testing/documentación:
4. `KNOWN_ISSUES.md`
5. `TEST_STATUS.md`
