-- ============================================================
-- Migración: Alineación de reportes con escenarios SBE
-- Se ejecuta automáticamente desde crud_reporte.py al iniciar
-- Este archivo es referencia documental.
-- ============================================================

-- 1. Reporte de Impacto: agregar columnas nuevas
ALTER TABLE `reporte_de_impacto` ADD COLUMN `brigada` VARCHAR(100) NULL AFTER `contenido`;
ALTER TABLE `reporte_de_impacto` ADD COLUMN `area_evaluada` VARCHAR(200) NULL AFTER `brigada`;
ALTER TABLE `reporte_de_impacto` ADD COLUMN `indicador` VARCHAR(100) NULL AFTER `area_evaluada`;
ALTER TABLE `reporte_de_impacto` ADD COLUMN `valor` VARCHAR(50) NULL AFTER `indicador`;
ALTER TABLE `reporte_de_impacto` ADD COLUMN `unidad` VARCHAR(50) NULL AFTER `valor`;

-- 2. Reporte de Impacto: hacer Actividad opcional (datos existentes se mantienen)
ALTER TABLE `reporte_de_impacto`
  MODIFY COLUMN `Actividad_idActividad` INT(11) NULL;

-- 3. Reporte de Impacto: contenido pasa a nullable (descripción del impacto es opcional si hay indicador)
ALTER TABLE `reporte_de_impacto`
  MODIFY COLUMN `contenido` TEXT NULL;

-- 4. Reporte de Actividades: agregar campo participantes
ALTER TABLE `reporte_actividad` ADD COLUMN `participantes` VARCHAR(500) NULL AFTER `resumen`;
