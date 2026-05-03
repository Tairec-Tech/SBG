<<<<<<< HEAD
-- Mensaje del día: editable por Directivo/Coordinador desde el dashboard.
-- Ejecutar una vez en MySQL.

USE db_brigadas_maracaibo;

CREATE TABLE IF NOT EXISTS `configuracion` (
  `clave` varchar(64) NOT NULL,
  `valor` text DEFAULT NULL,
  `actualizado_en` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`clave`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

INSERT INTO `configuracion` (`clave`, `valor`) VALUES ('mensaje_dia', '')
ON DUPLICATE KEY UPDATE `clave` = `clave`;
=======
-- Mensaje del día: editable por Directivo/Coordinador desde el dashboard.
-- Ejecutar una vez en MySQL.

USE db_brigadas_maracaibo;

CREATE TABLE IF NOT EXISTS `configuracion` (
  `clave` varchar(64) NOT NULL,
  `valor` text DEFAULT NULL,
  `actualizado_en` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`clave`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

INSERT INTO `configuracion` (`clave`, `valor`) VALUES ('mensaje_dia', '')
ON DUPLICATE KEY UPDATE `clave` = `clave`;
>>>>>>> 6cb1e103cc1d0d934c3f169517ceacc4cb355f96
