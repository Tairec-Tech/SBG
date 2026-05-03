-- ============================================================
-- MIGRACIÓN v2 — Ejecutar SOLO si precheck_v2_registro.sql
-- retorna 0 filas en las 4 consultas.
-- ============================================================

-- Un profesor solo puede ser responsable de una brigada.
-- (NULL no viola UNIQUE en MySQL, múltiples brigadas pueden tener profesor_id = NULL)
ALTER TABLE brigada ADD UNIQUE INDEX idx_brigada_profesor_unico (profesor_id);

-- Una institución no puede tener dos brigadas del mismo tipo.
ALTER TABLE brigada ADD UNIQUE INDEX idx_brigada_tipo_inst (Institucion_Educativa_idInstitucion, tipo_brigada);
