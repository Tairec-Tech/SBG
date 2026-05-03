-- ============================================================
-- PRECHEQUEO v2 — Ejecutar ANTES de migracion_v2_registro.sql
-- Si algún SELECT retorna filas, resolver manualmente primero.
-- ============================================================

-- 1. Profesores responsables de más de una brigada
--    (romperían UNIQUE INDEX en brigada.profesor_id)
SELECT profesor_id, COUNT(*) AS n
FROM brigada
WHERE profesor_id IS NOT NULL
GROUP BY profesor_id
HAVING n > 1;

-- 2. Brigadas duplicadas por tipo en la misma institución
--    (romperían UNIQUE INDEX en (Institucion_Educativa_idInstitucion, tipo_brigada))
SELECT Institucion_Educativa_idInstitucion, tipo_brigada, COUNT(*) AS n
FROM brigada
GROUP BY Institucion_Educativa_idInstitucion, tipo_brigada
HAVING n > 1;

-- 3. Inconsistencias: profesor dice estar en brigada X,
--    pero brigada X no lo tiene como profesor_id
SELECT u.idUsuario, u.nombre, u.apellido,
       u.Brigada_idBrigada, b.profesor_id
FROM usuario u
JOIN brigada b ON b.idBrigada = u.Brigada_idBrigada
WHERE u.rol = 'Profesor'
  AND (b.profesor_id IS NULL OR b.profesor_id != u.idUsuario);

-- 4. Cruces de institución: profesor en brigada de otra institución
SELECT u.idUsuario, u.nombre, u.apellido,
       u.Institucion_Educativa_idInstitucion AS institucion_usuario,
       b.idBrigada, b.nombre_brigada,
       b.Institucion_Educativa_idInstitucion AS institucion_brigada
FROM usuario u
JOIN brigada b ON b.idBrigada = u.Brigada_idBrigada
WHERE u.Institucion_Educativa_idInstitucion IS NOT NULL
  AND b.Institucion_Educativa_idInstitucion IS NOT NULL
  AND u.Institucion_Educativa_idInstitucion <> b.Institucion_Educativa_idInstitucion;
