-- Migración v3: Tabla para adjuntos multimedia en reportes
CREATE TABLE IF NOT EXISTS `reporte_media` (
  `idMedia` INT(11) NOT NULL AUTO_INCREMENT,
  `entidad_tipo` ENUM('actividad', 'impacto') NOT NULL,
  `entidad_id` INT(11) NOT NULL,
  `ruta_archivo` VARCHAR(255) NOT NULL,
  `tipo_archivo` ENUM('imagen', 'video') NOT NULL,
  `fecha_subida` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idMedia`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
