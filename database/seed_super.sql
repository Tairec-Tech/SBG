-- ================================================================
-- SUPER SEED v2 — SBE (Sistema de Brigadas Escolares)
-- Alineado con el modelo institucional: 11 brigadas (1 por tipo),
-- planificación JSON en actividades, reportes con campos extendidos.
-- Ejecutar DESPUÉS de db_brigadas_maracaibo.sql + migraciones.
-- ================================================================
-- Contraseñas (SHA-256 legacy):
--   director    → director123
--   profesor1-11 → profesor1 ... profesor11
--   alumnos     → alumno123
-- ================================================================

USE db_brigadas_maracaibo;

-- ╔═══════════════════════════════════════════════════════════════╗
-- ║ LIMPIEZA SEGURA (orden inverso por FK)                       ║
-- ╚═══════════════════════════════════════════════════════════════╝
-- Tablas que podrían no existir en esquemas antiguos: ignorar error
DELETE FROM `reporte_de_impacto`  WHERE 1=1;
DELETE FROM `reporte_actividad`   WHERE 1=1;
DELETE FROM `reporte_incidente`   WHERE 1=1;
DELETE FROM `indicador_ambiental` WHERE 1=1;
DELETE FROM `turno`               WHERE 1=1;
DELETE FROM `actividad`           WHERE 1=1;
DELETE FROM `usuario`             WHERE 1=1;
DELETE FROM `brigada`             WHERE 1=1;
DELETE FROM `institucion_educativa` WHERE 1=1;

-- ══════════════════════════════════════════════════════════════
-- 1. INSTITUCIÓN
-- ══════════════════════════════════════════════════════════════
INSERT INTO `institucion_educativa`
  (`idInstitucion`, `nombre_institucion`, `direccion`, `telefono`, `logo_ruta`)
VALUES
  (1, 'U.E. Libertador Simón Bolívar', 'Av. Universidad, Maracaibo, Zulia', '04247313983', NULL);

-- ══════════════════════════════════════════════════════════════
-- 2. BRIGADAS — 1 por tipo (11 brigadas, IDs 101-111)
--    Modelo institucional: cada institución maneja 1 brigada por tipo
-- ══════════════════════════════════════════════════════════════
INSERT INTO `brigada`
  (`idBrigada`, `nombre_brigada`, `area_accion`, `descripcion`, `coordinador`,
   `color_identificador`, `tipo_brigada`, `fecha_creacion`,
   `Institucion_Educativa_idInstitucion`, `profesor_id`, `subjefe_id`)
VALUES
(101, 'Brigada Ecológica',                     'Medio Ambiente',           'Cuidado de áreas verdes, reciclaje, reforestación y conciencia ambiental.',                         NULL, '#059669', 'ecologica',       NOW(), 1, 202, NULL),
(102, 'Brigada de Gestión de Riesgo',           'Prevención y Emergencias', 'Simulacros, primeros auxilios, rutas de evacuación y prevención de riesgos.',                       NULL, '#ea580c', 'riesgo',          NOW(), 1, 203, NULL),
(103, 'Brigada de Patrulla Escolar',            'Seguridad Vial',           'Control de paso peatonal, señalización y orden en entradas y salidas.',                              NULL, '#dc2626', 'patrulla',        NOW(), 1, 204, NULL),
(104, 'Brigada de Convivencia y Paz',           'Mediación y Valores',      'Resolución pacífica de conflictos, antibullying y promoción de valores.',                            NULL, '#64748b', 'convivencia',     NOW(), 1, 205, NULL),
(105, 'Brigada de Primeros Auxilios',            'Salud Escolar',            'Atención inmediata, botiquines, prevención de salud y primeros auxilios.',                           NULL, '#eab308', 'auxilios',        NOW(), 1, 206, NULL),
(106, 'Brigada de Educación Física',             'Deporte y Recreación',     'Promoción de actividad física, jornadas deportivas y recreación escolar.',                          NULL, '#3b82f6', 'educacion_fisica',NOW(), 1, 207, NULL),
(107, 'Brigada Mi Conuco Escolar Carlos Lanz',   'Agricultura Escolar',      'Huertos escolares, siembra, soberanía alimentaria y agroecología.',                                NULL, '#84cc16', 'conuco',          NOW(), 1, 208, NULL),
(108, 'Brigada de Patrimonio y Turismo',         'Identidad Cultural',       'Valoración del patrimonio histórico-cultural local, turismo escolar.',                              NULL, '#ec4899', 'patrimonio',      NOW(), 1, 209, NULL),
(109, 'Brigada de Artes Visuales',               'Expresión Artística',      'Murales, expresión creativa, diseño visual y apoyo artístico escolar.',                             NULL, '#a855f7', 'artes',           NOW(), 1, 210, NULL),
(110, 'Brigada Juventud Patriótica',             'Identidad Nacional',       'Efemérides, memoria histórica, actos cívicos e identidad nacional.',                               NULL, '#9ca3af', 'patriotica',      NOW(), 1, 211, NULL),
(111, 'Brigada de Derechos Humanos',             'DDHH e Inclusión',         'Dignidad, igualdad, inclusión, cultura de derechos y formación ciudadana.',                         NULL, '#1e3a8a', 'ddhh',            NOW(), 1, 212, NULL);

-- ══════════════════════════════════════════════════════════════
-- 3. DIRECTIVO (ID 201)
-- ══════════════════════════════════════════════════════════════
-- usuario: director | contraseña: director123 (SHA-256)
INSERT INTO `usuario`
  (`idUsuario`, `nombre`, `apellido`, `cedula`, `email`, `usuario`, `contrasena`, `rol`,
   `Brigada_idBrigada`, `Institucion_Educativa_idInstitucion`)
VALUES
(201, 'Ricardo', 'Mendoza Pérez', 'V-12345678', 'director@uelibertador.edu.ve', 'director',
  '9e4d7bba246abe731743986c4dc50897b68b1d0249a066abb3530fcbaa33dab3', 'Directivo', NULL, 1);

-- ══════════════════════════════════════════════════════════════
-- 4. PROFESORES (IDs 202-212, 11 profesores — 1 por brigada)
-- ══════════════════════════════════════════════════════════════
-- Cada profesor: usuario = profesorN, contraseña = profesorN (SHA-256)
INSERT INTO `usuario`
  (`idUsuario`, `nombre`, `apellido`, `cedula`, `email`, `usuario`, `contrasena`, `rol`,
   `Brigada_idBrigada`, `Institucion_Educativa_idInstitucion`)
VALUES
-- Ecológica
(202, 'Carlos',   'Martínez López',   'V-11000001', 'cmartinez@uelibertador.edu.ve',  'profesor1',
  'c5feadda95f15c08186641ec217bfde3ac211298f1912798610ef6532c7ffe1f', 'Profesor', 101, 1),
-- Gestión de Riesgo
(203, 'José',     'Hernández Gil',    'V-11000002', 'jhernandez@uelibertador.edu.ve', 'profesor2',
  'c59036fb2b020cac117abc9e4647f54bac565eddbb5aa209f9e78e5269e0ec42', 'Profesor', 102, 1),
-- Patrulla Escolar
(204, 'Pedro',    'Urdaneta Bracho',  'V-11000003', 'purdaneta@uelibertador.edu.ve',  'profesor3',
  'fa2eef54e73154938645d3b4d6207acf5b602188f4ae96ffb0863ac5fa2ad236', 'Profesor', 103, 1),
-- Convivencia y Paz
(205, 'Andrés',   'Romero Villalobos','V-11000004', 'aromero@uelibertador.edu.ve',    'profesor4',
  '7bea9b88144d12640909c0fbe039abd95317bd17910e9b02dce48da2b47400c8', 'Profesor', 104, 1),
-- Primeros Auxilios
(206, 'Laura',    'Pérez Montiel',    'V-11000005', 'lperez@uelibertador.edu.ve',     'profesor5',
  '007135061d2d39a4a5d676fda2e6e5cdf36d805b7ba95702ea6be37f39016287', 'Profesor', 105, 1),
-- Educación Física
(207, 'Carmen',   'Fuentes Nava',     'V-11000006', 'cfuentes@uelibertador.edu.ve',   'profesor6',
  'c43dfb1540a445e440543b25c2cec09e1af826cf55ea3527345cce54541412d2', 'Profesor', 106, 1),
-- Conuco Escolar
(208, 'Mariana',  'Colmenares Rivas', 'V-11000007', 'mcolmenares@uelibertador.edu.ve','profesor7',
  '916751e2461a8f8cb63a509f004a378566d51e06cd7c65f80c28ced489dfdc83', 'Profesor', 107, 1),
-- Patrimonio y Turismo
(209, 'Gabriela', 'Torres Dávila',    'V-11000008', 'gtorres@uelibertador.edu.ve',    'profesor8',
  '8146bfdf6da999566185928f47d02ab23ef1c296031a209ccf987bdbcc89d0c2', 'Profesor', 108, 1),
-- Artes Visuales
(210, 'Fernanda', 'Araujo Becerra',   'V-11000009', 'faraujo@uelibertador.edu.ve',    'profesor9',
  'ac4eefbaf4c998ed3ef0be2ff8c8e014ba1474a6823c47e29dcb6469f3ee3cb5', 'Profesor', 109, 1),
-- Juventud Patriótica
(211, 'Manuel',   'Toro Miranda',     'V-11000010', 'mtoro@uelibertador.edu.ve',      'profesor10',
  '3b229e07dea6b6ab16c7b0b439eff04d227b01b426b77a0594abf37cd03122b6', 'Profesor', 110, 1),
-- Derechos Humanos
(212, 'Natalia',  'Villegas Cedeño',  'V-11000011', 'nvillegas@uelibertador.edu.ve',  'profesor11',
  '8f0ec69e32f3a3e52e268cdb6e58bab47e113f57da06adabbc48076db2d90aef', 'Profesor', 111, 1);

-- Asignar profesores a sus brigadas
UPDATE `brigada` SET `profesor_id` = 202 WHERE `idBrigada` = 101;
UPDATE `brigada` SET `profesor_id` = 203 WHERE `idBrigada` = 102;
UPDATE `brigada` SET `profesor_id` = 204 WHERE `idBrigada` = 103;
UPDATE `brigada` SET `profesor_id` = 205 WHERE `idBrigada` = 104;
UPDATE `brigada` SET `profesor_id` = 206 WHERE `idBrigada` = 105;
UPDATE `brigada` SET `profesor_id` = 207 WHERE `idBrigada` = 106;
UPDATE `brigada` SET `profesor_id` = 208 WHERE `idBrigada` = 107;
UPDATE `brigada` SET `profesor_id` = 209 WHERE `idBrigada` = 108;
UPDATE `brigada` SET `profesor_id` = 210 WHERE `idBrigada` = 109;
UPDATE `brigada` SET `profesor_id` = 211 WHERE `idBrigada` = 110;
UPDATE `brigada` SET `profesor_id` = 212 WHERE `idBrigada` = 111;

-- ══════════════════════════════════════════════════════════════
-- 5. ALUMNOS — 4 por brigada (44 alumnos, IDs 301-344)
--    contraseña: alumno123 (SHA-256)
--    c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0
-- ══════════════════════════════════════════════════════════════

-- Brigada 101 — Ecológica
INSERT INTO `usuario` (`idUsuario`,`nombre`,`apellido`,`cedula`,`email`,`usuario`,`contrasena`,`rol`,`Brigada_idBrigada`,`Institucion_Educativa_idInstitucion`) VALUES
(301,'Miguel','Sánchez Ríos','V-30100001','msanchez301@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',101,NULL),
(302,'Valeria','Gómez Pineda','V-30100002','vgomez302@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',101,NULL),
(303,'Sebastián','Morales Castro','V-30100003','smorales303@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',101,NULL),
(304,'Isabella','Ferrer Quintero','V-30100004','iferrer304@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',101,NULL);

-- Brigada 102 — Gestión de Riesgo
INSERT INTO `usuario` (`idUsuario`,`nombre`,`apellido`,`cedula`,`email`,`usuario`,`contrasena`,`rol`,`Brigada_idBrigada`,`Institucion_Educativa_idInstitucion`) VALUES
(305,'Daniel','Ochoa Villalobos','V-30200001','dochoa305@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',102,NULL),
(306,'Camila','Parra Briceño','V-30200002','cparra306@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',102,NULL),
(307,'Andrés','Delgado Urdaneta','V-30200003','adelgado307@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',102,NULL),
(308,'Sofía','Linares Molina','V-30200004','slinares308@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',102,NULL);

-- Brigada 103 — Patrulla Escolar
INSERT INTO `usuario` (`idUsuario`,`nombre`,`apellido`,`cedula`,`email`,`usuario`,`contrasena`,`rol`,`Brigada_idBrigada`,`Institucion_Educativa_idInstitucion`) VALUES
(309,'Diego','Montilla Torres','V-30300001','dmontilla309@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',103,NULL),
(310,'Paula','Atencio Herrera','V-30300002','patencio310@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',103,NULL),
(311,'David','Ortega Colina','V-30300003','dortega311@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',103,NULL),
(312,'Andrea','Salas Moreno','V-30300004','asalas312@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',103,NULL);

-- Brigada 104 — Convivencia y Paz
INSERT INTO `usuario` (`idUsuario`,`nombre`,`apellido`,`cedula`,`email`,`usuario`,`contrasena`,`rol`,`Brigada_idBrigada`,`Institucion_Educativa_idInstitucion`) VALUES
(313,'Francisco','Barrios Acosta','V-30400001','fbarrios313@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',104,NULL),
(314,'Carolina','Peña Romero','V-30400002','cpena314@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',104,NULL),
(315,'Simón','Urdaneta Fuentes','V-30400003','surdaneta315@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',104,NULL),
(316,'Irene','Medina Leal','V-30400004','imedina316@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',104,NULL);

-- Brigada 105 — Primeros Auxilios
INSERT INTO `usuario` (`idUsuario`,`nombre`,`apellido`,`cedula`,`email`,`usuario`,`contrasena`,`rol`,`Brigada_idBrigada`,`Institucion_Educativa_idInstitucion`) VALUES
(317,'Eduardo','Méndez Contreras','V-30500001','emendez317@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',105,NULL),
(318,'Fernanda','Escalona Ruiz','V-30500002','fescalona318@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',105,NULL),
(319,'Nicolás','Bracho Lugo','V-30500003','nbracho319@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',105,NULL),
(320,'Daniela','Camacho Isea','V-30500004','dcamacho320@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',105,NULL);

-- Brigada 106 — Educación Física
INSERT INTO `usuario` (`idUsuario`,`nombre`,`apellido`,`cedula`,`email`,`usuario`,`contrasena`,`rol`,`Brigada_idBrigada`,`Institucion_Educativa_idInstitucion`) VALUES
(321,'Rafael','Perozo Medina','V-30600001','rperozo321@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',106,NULL),
(322,'Lucía','Guerrero Finol','V-30600002','lguerrero322@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',106,NULL),
(323,'Santiago','Ávila Pacheco','V-30600003','savila323@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',106,NULL),
(324,'Antonella','Pirela Soto','V-30600004','apirela324@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',106,NULL);

-- Brigada 107 — Conuco Escolar
INSERT INTO `usuario` (`idUsuario`,`nombre`,`apellido`,`cedula`,`email`,`usuario`,`contrasena`,`rol`,`Brigada_idBrigada`,`Institucion_Educativa_idInstitucion`) VALUES
(325,'Matías','Leal Andrade','V-30700001','mleal325@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',107,NULL),
(326,'Valentina','Borjas Ramírez','V-30700002','vborjas326@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',107,NULL),
(327,'Emilio','Quintero Díaz','V-30700003','equintero327@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',107,NULL),
(328,'Mariane','Rincón Vargas','V-30700004','mrincon328@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',107,NULL);

-- Brigada 108 — Patrimonio y Turismo
INSERT INTO `usuario` (`idUsuario`,`nombre`,`apellido`,`cedula`,`email`,`usuario`,`contrasena`,`rol`,`Brigada_idBrigada`,`Institucion_Educativa_idInstitucion`) VALUES
(329,'Tomás','Vera Suárez','V-30800001','tvera329@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',108,NULL),
(330,'María','Zambrano Paz','V-30800002','mzambrano330@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',108,NULL),
(331,'Lucas','Sulbarán Conde','V-30800003','lsulbaran331@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',108,NULL),
(332,'Martina','Navarro Petit','V-30800004','mnavarro332@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',108,NULL);

-- Brigada 109 — Artes Visuales
INSERT INTO `usuario` (`idUsuario`,`nombre`,`apellido`,`cedula`,`email`,`usuario`,`contrasena`,`rol`,`Brigada_idBrigada`,`Institucion_Educativa_idInstitucion`) VALUES
(333,'Samuel','Ferrer Bracho','V-30900001','sferrer333@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',109,NULL),
(334,'Elena','Matos Useche','V-30900002','ematos334@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',109,NULL),
(335,'Adrián','Labarca Ochoa','V-30900003','alabarca335@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',109,NULL),
(336,'Victoria','Angulo Baptista','V-30900004','vangulo336@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',109,NULL);

-- Brigada 110 — Juventud Patriótica
INSERT INTO `usuario` (`idUsuario`,`nombre`,`apellido`,`cedula`,`email`,`usuario`,`contrasena`,`rol`,`Brigada_idBrigada`,`Institucion_Educativa_idInstitucion`) VALUES
(337,'Esteban','Márquez Vera','V-31000001','emarquez337@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',110,NULL),
(338,'Diana','Montiel Rojas','V-31000002','dmontiel338@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',110,NULL),
(339,'Rodrigo','Cuenca Salas','V-31000003','rcuenca339@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',110,NULL),
(340,'Lorena','Rivas Duque','V-31000004','lrivas340@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',110,NULL);

-- Brigada 111 — Derechos Humanos
INSERT INTO `usuario` (`idUsuario`,`nombre`,`apellido`,`cedula`,`email`,`usuario`,`contrasena`,`rol`,`Brigada_idBrigada`,`Institucion_Educativa_idInstitucion`) VALUES
(341,'Cristian','Polanco Gil','V-31100001','cpolanco341@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',111,NULL),
(342,'Rebeca','Olivares Paz','V-31100002','rolivares342@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',111,NULL),
(343,'Gabriel','Chacón Nava','V-31100003','gchacon343@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',111,NULL),
(344,'Sara','Portillo León','V-31100004','sportillo344@uel.edu.ve',NULL,'c1042ecc51482cef39f2e89e1273a35074db7f873f1ac6050efd546a9bceefc0','Brigadista',111,NULL);

-- ══════════════════════════════════════════════════════════════
-- 6. ACTIVIDADES — Planificación JSON en columna `descripcion`
--    Mezcla de actividades con JSON v2 y una legacy (texto plano)
--    para validar retrocompatibilidad.
-- ══════════════════════════════════════════════════════════════

-- ── Ecológica (101) ──
INSERT INTO `actividad` (`titulo`, `descripcion`, `fecha_inicio`, `fecha_fin`, `estado`, `Brigada_idBrigada`, `Usuario_idUsuarioCreador`) VALUES
('Jornada de Reforestación',
 '{"momento_escolar":"Segundo Momento","origen_actividad":"Cronograma Institucional","efemeride":"Día de la Tierra","necesidad_detectada":"Áreas verdes deterioradas en el perímetro escolar","objetivo_plan":"Sembrar 80 árboles autóctonos (cují, apamate) con el apoyo de padres y representantes","nivel_educativo":"Integral","resultado_esperado":"80 árboles plantados y mantenidos","resultado_obtenido":"80 árboles plantados exitosamente"}',
 CURDATE() - INTERVAL 10 DAY, CURDATE() - INTERVAL 9 DAY, 'Completada', 101, 202),

('Eco-Auditoría del Agua',
 '{"momento_escolar":"Segundo Momento","origen_actividad":"Necesidad Detectada","efemeride":"","necesidad_detectada":"Alto consumo de agua en pabellones","objetivo_plan":"Medir el consumo de agua por pabellón durante una semana y generar informe","nivel_educativo":"Media General","resultado_esperado":"Informe de consumo por pabellón","resultado_obtenido":""}',
 CURDATE() - INTERVAL 3 DAY, CURDATE(), 'En Progreso', 101, 202),

('Campaña Cero Plástico',
 '{"momento_escolar":"Tercer Momento","origen_actividad":"Cronograma Institucional","efemeride":"Día Mundial del Ambiente","necesidad_detectada":"Acumulación de plásticos en áreas comunes","objetivo_plan":"Recolección masiva de plástico y charla sobre alternativas sostenibles","nivel_educativo":"Integral","resultado_esperado":"Reducción del 50% de plástico en la semana","resultado_obtenido":""}',
 CURDATE() + INTERVAL 7 DAY, CURDATE() + INTERVAL 8 DAY, 'Planificada', 101, 202),

-- ── Gestión de Riesgo (102) ──
('Simulacro de Evacuación',
 '{"momento_escolar":"Primer Momento","origen_actividad":"Cronograma Institucional","efemeride":"","necesidad_detectada":"Nunca se ha medido el tiempo de evacuación","objetivo_plan":"Simulacro general con cronómetro y evaluación de tiempos de salida","nivel_educativo":"Integral","resultado_esperado":"Evacuación en menos de 5 minutos","resultado_obtenido":"Evacuación en 4 minutos 30 segundos, 2 cuellos de botella identificados"}',
 CURDATE() - INTERVAL 15 DAY, CURDATE() - INTERVAL 15 DAY, 'Completada', 102, 203),

('Señalización de Rutas de Evacuación',
 '{"momento_escolar":"Segundo Momento","origen_actividad":"Necesidad Detectada","efemeride":"","necesidad_detectada":"Señalización deteriorada en pabellones","objetivo_plan":"Colocación de flechas y carteles de salida de emergencia en todos los pabellones","nivel_educativo":"Media General","resultado_esperado":"100% de pasillos señalizados","resultado_obtenido":""}',
 CURDATE() + INTERVAL 5 DAY, CURDATE() + INTERVAL 6 DAY, 'Planificada', 102, 203),

-- ── Patrulla Escolar (103) ──
('Operativo Paso Seguro',
 '{"momento_escolar":"Primer Momento","origen_actividad":"Cronograma Institucional","efemeride":"","necesidad_detectada":"Cruces peligrosos de alumnos en hora pico","objetivo_plan":"Control de tránsito peatonal en la entrada principal durante horas pico","nivel_educativo":"Primaria","resultado_esperado":"Cero incidentes de cruce peligroso","resultado_obtenido":"120 alumnos cruzaron de forma segura, sin incidentes"}',
 CURDATE() - INTERVAL 7 DAY, CURDATE() - INTERVAL 7 DAY, 'Completada', 103, 204),

('Pintura de Paso de Cebra',
 '{"momento_escolar":"Segundo Momento","origen_actividad":"Necesidad Detectada","efemeride":"","necesidad_detectada":"Paso peatonal borrado frente a la escuela","objetivo_plan":"Renovar la pintura del paso peatonal frente al portón principal","nivel_educativo":"Integral","resultado_esperado":"Paso de cebra renovado y visible","resultado_obtenido":""}',
 CURDATE() + INTERVAL 3 DAY, CURDATE() + INTERVAL 3 DAY, 'Planificada', 103, 204),

-- ── Convivencia y Paz (104) ──
('Jornada Anti-Bullying',
 '{"momento_escolar":"Primer Momento","origen_actividad":"Cronograma Institucional","efemeride":"Día contra el Bullying","necesidad_detectada":"Reportes de conflicto entre secciones","objetivo_plan":"Dinámica grupal sobre respeto, empatía y resolución de conflictos","nivel_educativo":"Media General","resultado_esperado":"Reducción de conflictos en 50%","resultado_obtenido":"3 casos identificados para seguimiento con orientación"}',
 CURDATE() - INTERVAL 12 DAY, CURDATE() - INTERVAL 12 DAY, 'Completada', 104, 205),

('Festival de la Amistad',
 '{"momento_escolar":"Tercer Momento","origen_actividad":"Cronograma Institucional","efemeride":"Día de la Amistad","necesidad_detectada":"Baja integración entre secciones","objetivo_plan":"Actividad recreativa con juegos cooperativos y mural colectivo","nivel_educativo":"Integral","resultado_esperado":"Participación del 80% de estudiantes","resultado_obtenido":""}',
 CURDATE() + INTERVAL 6 DAY, CURDATE() + INTERVAL 6 DAY, 'Planificada', 104, 205),

-- ── Primeros Auxilios (105) ──
('Curso de Primeros Auxilios',
 '{"momento_escolar":"Segundo Momento","origen_actividad":"Cronograma Institucional","efemeride":"","necesidad_detectada":"Personal sin capacitación en RCP","objetivo_plan":"Taller práctico: RCP, vendajes, manejo de fracturas","nivel_educativo":"Media General","resultado_esperado":"18 brigadistas certificados","resultado_obtenido":"18 brigadistas aprobaron la evaluación práctica"}',
 CURDATE() - INTERVAL 5 DAY, CURDATE() - INTERVAL 4 DAY, 'Completada', 105, 206),

-- ── Educación Física (106) ──
('Jornada Deportiva Interclases',
 '{"momento_escolar":"Segundo Momento","origen_actividad":"Cronograma Institucional","efemeride":"Día de la Educación Física","necesidad_detectada":"Sedentarismo estudiantil","objetivo_plan":"Competencias deportivas entre secciones: fútbol sala, voleibol, atletismo","nivel_educativo":"Integral","resultado_esperado":"Participación del 70% de las secciones","resultado_obtenido":""}',
 CURDATE() + INTERVAL 4 DAY, CURDATE() + INTERVAL 4 DAY, 'Planificada', 106, 207),

-- ── Conuco Escolar (107) ──
('Siembra del Huerto Escolar',
 '{"momento_escolar":"Primer Momento","origen_actividad":"Cronograma Institucional","efemeride":"","necesidad_detectada":"Ausencia de huerto en la institución","objetivo_plan":"Preparar terreno y sembrar hortalizas: tomate, pimentón, cilantro","nivel_educativo":"Primaria","resultado_esperado":"Huerto de 10m² produciendo en 60 días","resultado_obtenido":"Terreno preparado y 30 plántulas sembradas"}',
 CURDATE() - INTERVAL 20 DAY, CURDATE() - INTERVAL 19 DAY, 'Completada', 107, 208),

-- ── Patrimonio y Turismo (108) ──
('Recorrido por el Casco Histórico',
 '{"momento_escolar":"Segundo Momento","origen_actividad":"Cronograma Institucional","efemeride":"Día del Patrimonio","necesidad_detectada":"Desconocimiento de la historia local","objetivo_plan":"Visita guiada al casco histórico de Maracaibo con registro fotográfico","nivel_educativo":"Media General","resultado_esperado":"Exposición fotográfica en la institución","resultado_obtenido":""}',
 CURDATE() + INTERVAL 10 DAY, CURDATE() + INTERVAL 10 DAY, 'Planificada', 108, 209),

-- ── Artes Visuales (109) ──
('Mural de Convivencia',
 '{"momento_escolar":"Tercer Momento","origen_actividad":"Necesidad Detectada","efemeride":"","necesidad_detectada":"Paredes del patio deterioradas","objetivo_plan":"Diseñar y pintar un mural colectivo sobre valores y convivencia","nivel_educativo":"Integral","resultado_esperado":"Mural de 4x2m completado","resultado_obtenido":""}',
 CURDATE() + INTERVAL 8 DAY, CURDATE() + INTERVAL 9 DAY, 'Planificada', 109, 210),

-- ── Juventud Patriótica (110) ──
('Acto Cívico Día de la Bandera',
 '{"momento_escolar":"Primer Momento","origen_actividad":"Cronograma Institucional","efemeride":"Día de la Bandera","necesidad_detectada":"","objetivo_plan":"Acto cívico con izado de bandera, himno y reseña histórica","nivel_educativo":"Integral","resultado_esperado":"Participación de toda la comunidad educativa","resultado_obtenido":"Acto realizado con 350 asistentes"}',
 CURDATE() - INTERVAL 8 DAY, CURDATE() - INTERVAL 8 DAY, 'Completada', 110, 211),

-- ── Derechos Humanos (111) ──
('Taller de Derechos del Niño',
 '{"momento_escolar":"Segundo Momento","origen_actividad":"Cronograma Institucional","efemeride":"Día de los Derechos del Niño","necesidad_detectada":"Desconocimiento de derechos fundamentales","objetivo_plan":"Taller interactivo sobre los derechos del niño con material audiovisual","nivel_educativo":"Primaria","resultado_esperado":"90% de comprensión en evaluación posterior","resultado_obtenido":""}',
 CURDATE() + INTERVAL 12 DAY, CURDATE() + INTERVAL 12 DAY, 'Planificada', 111, 212),

-- ── Legacy: actividad con texto plano viejo (retrocompatibilidad) ──
('Charla de Seguridad Vial',
 'Presentación sobre señales de tránsito y cruce seguro para primaria.',
 CURDATE() - INTERVAL 2 DAY, CURDATE() - INTERVAL 1 DAY, 'Completada', 103, 204);

-- ══════════════════════════════════════════════════════════════
-- 7. INDICADORES AMBIENTALES (para actividades ecológicas)
-- ══════════════════════════════════════════════════════════════
INSERT INTO `indicador_ambiental` (`valor`, `tipo_indicador`, `unidad`, `Actividad_idActividad`) VALUES
(80.0, 'Árboles Plantados',       'uni', (SELECT idActividad FROM actividad WHERE titulo='Jornada de Reforestación' LIMIT 1)),
(12.5, 'Reducción Consumo Agua',  '%',   (SELECT idActividad FROM actividad WHERE titulo='Eco-Auditoría del Agua' LIMIT 1));

-- ══════════════════════════════════════════════════════════════
-- 8. TURNOS — 1-2 por brigada con temas variados
-- ══════════════════════════════════════════════════════════════
-- La tabla turno ahora se crea en db_brigadas_maracaibo.sql

INSERT INTO `turno` (`Brigada_idBrigada`, `fecha`, `hora_inicio`, `hora_fin`, `ubicacion`, `notas`, `estado`) VALUES
-- Ecológica
(101, CURDATE() - INTERVAL 5 DAY,  '07:00:00', '09:00:00', 'Jardines del Pabellón A',      'Riego y mantenimiento de jardín',        'Completado'),
(101, CURDATE() + INTERVAL 1 DAY,  '07:30:00', '10:00:00', 'Perímetro escolar zona norte',  'Siembra programada',                    'Programado'),
-- Gestión de Riesgo
(102, CURDATE() - INTERVAL 2 DAY,  '08:00:00', '10:00:00', 'Patio Central',                 'Simulacro: evaluación de tiempos',      'Completado'),
(102, CURDATE() + INTERVAL 2 DAY,  '09:00:00', '11:30:00', 'Salón de Usos Múltiples',       'Curso práctico de primeros auxilios',   'Programado'),
-- Patrulla Escolar
(103, CURDATE() - INTERVAL 1 DAY,  '06:30:00', '07:30:00', 'Entrada principal',             'Operativo de cruce seguro AM',          'Completado'),
(103, CURDATE(),                    '11:30:00', '12:30:00', 'Entrada principal',             'Operativo de cruce seguro PM',          'En Progreso'),
-- Convivencia y Paz
(104, CURDATE() - INTERVAL 3 DAY,  '10:00:00', '11:30:00', 'Aula 3ero A y B',              'Sesión de mediación',                   'Completado'),
(104, CURDATE() + INTERVAL 1 DAY,  '08:00:00', '09:30:00', 'Cancha techada',               'Dinámica anti-bullying',                'Programado'),
-- Primeros Auxilios
(105, CURDATE() + INTERVAL 3 DAY,  '14:00:00', '16:00:00', 'Enfermería escolar',           'Revisión de botiquines',                'Programado'),
-- Educación Física
(106, CURDATE() + INTERVAL 4 DAY,  '07:00:00', '09:00:00', 'Cancha deportiva',             'Preparación jornada deportiva',         'Programado'),
-- Conuco Escolar
(107, CURDATE() + INTERVAL 2 DAY,  '07:00:00', '09:00:00', 'Huerto escolar',               'Riego y monitoreo de plántulas',        'Programado'),
-- Patrimonio
(108, CURDATE() + INTERVAL 5 DAY,  '08:00:00', '12:00:00', 'Casco Histórico Maracaibo',    'Recorrido cultural programado',         'Programado');

-- ══════════════════════════════════════════════════════════════
-- 9. REPORTES DE INCIDENTES — distribuidos entre brigadas
-- ══════════════════════════════════════════════════════════════
INSERT INTO `reporte_incidente` (`titulo`, `descripcion`, `ubicacion`, `prioridad`, `estado`, `Brigada_idBrigada`, `creado_en`) VALUES
-- Ecológica
('Fuga de agua en baños',            'Grifo roto en baños del Pabellón B. Desperdicio constante de agua.',                               'Baños Pabellón B',     'Media',                            'En Proceso', 101, NOW() - INTERVAL 3 DAY),
('Basura en áreas verdes',           'Acumulación de desechos plásticos en el jardín trasero después del recreo.',                       'Jardín trasero',       'Baja - Situación menor',           'Resuelto',   101, NOW() - INTERVAL 8 DAY),
-- Gestión de Riesgo
('Extintores vencidos en Pabellón C','Se detectaron 3 extintores con fecha de vencimiento expirada en el tercer piso.',                  'Pabellón C, Piso 3',  'Alta - Requiere atención inmediata','En Proceso', 102, NOW() - INTERVAL 1 DAY),
('Grieta en pared del comedor',      'Fisura visible de 40cm en la pared norte del comedor. Posible riesgo estructural.',                'Comedor escolar',     'Alta - Requiere atención inmediata','En Proceso', 102, NOW() - INTERVAL 4 DAY),
-- Patrulla Escolar
('Señal de pare caída',              'La señal de PARE frente al portón principal fue derribada por el viento.',                         'Calle frente al portón','Alta - Requiere atención inmediata','En Proceso', 103, NOW() - INTERVAL 6 HOUR),
-- Convivencia y Paz
('Altercado entre estudiantes',      'Confrontación verbal entre dos alumnos de 4to año en el pasillo del 2do piso.',                    'Pasillo Piso 2',      'Media',                            'Resuelto',   104, NOW() - INTERVAL 5 DAY),
('Caso de acoso reportado',          'Un alumno reportó ser víctima de burlas repetidas por parte de compañeros de otra sección.',        'Buzón de Convivencia','Alta - Requiere atención inmediata','En Proceso', 104, NOW() - INTERVAL 1 DAY),
-- Primeros Auxilios
('Botiquín vacío en Pabellón A',     'Se reportó que el botiquín del Pabellón A no tiene gasas ni alcohol.',                             'Pabellón A',          'Media',                            'En Proceso', 105, NOW() - INTERVAL 2 DAY);

-- ══════════════════════════════════════════════════════════════
-- 10. REPORTES DE ACTIVIDADES (con campo participantes)
-- ══════════════════════════════════════════════════════════════
INSERT INTO `reporte_actividad` (`resumen`, `resultado`, `participantes`, `Actividad_idActividad`, `Usuario_idUsuario`, `fecha_reporte`) VALUES
('Se plantaron 80 árboles con apoyo de padres y representantes. Participaron 12 brigadistas.',
 'Exitoso - 80 árboles plantados', '12 brigadistas, 8 padres, Prof. Martínez',
 (SELECT idActividad FROM actividad WHERE titulo='Jornada de Reforestación' LIMIT 1), 202, NOW() - INTERVAL 9 DAY),

('El simulacro se ejecutó en 4 minutos 30 segundos. Se identificaron 2 cuellos de botella.',
 'Completado con observaciones', '4 brigadistas, 250 alumnos evacuados',
 (SELECT idActividad FROM actividad WHERE titulo='Simulacro de Evacuación' LIMIT 1), 203, NOW() - INTERVAL 14 DAY),

('Operativo matutino: 120 alumnos cruzaron de forma segura. Sin incidentes.',
 'Exitoso - Sin incidentes', '6 patrulleros',
 (SELECT idActividad FROM actividad WHERE titulo='Operativo Paso Seguro' LIMIT 1), 204, NOW() - INTERVAL 6 DAY),

('Se capacitaron 18 brigadistas en RCP y vendajes. Evaluación práctica aprobada por todos.',
 'Exitoso', '18 brigadistas, Dra. Martínez (instructora externa)',
 (SELECT idActividad FROM actividad WHERE titulo='Curso de Primeros Auxilios' LIMIT 1), 206, NOW() - INTERVAL 4 DAY),

('Dinámica con 35 alumnos. 3 casos requieren seguimiento con orientación.',
 'Completado con seguimiento requerido', '35 alumnos de 4to año, Prof. Romero, orientadora',
 (SELECT idActividad FROM actividad WHERE titulo='Jornada Anti-Bullying' LIMIT 1), 205, NOW() - INTERVAL 11 DAY),

('Terreno preparado y 30 plántulas sembradas en el huerto escolar.',
 'Exitoso', '10 brigadistas, Prof. Colmenares, conserje',
 (SELECT idActividad FROM actividad WHERE titulo='Siembra del Huerto Escolar' LIMIT 1), 208, NOW() - INTERVAL 19 DAY),

('Acto cívico con izado de bandera, himno y reseña histórica. 350 asistentes.',
 'Exitoso - Alta participación', 'Toda la comunidad educativa',
 (SELECT idActividad FROM actividad WHERE titulo='Acto Cívico Día de la Bandera' LIMIT 1), 211, NOW() - INTERVAL 7 DAY);

-- ══════════════════════════════════════════════════════════════
-- 11. REPORTES DE IMPACTO (con campos extendidos)
-- ══════════════════════════════════════════════════════════════
INSERT INTO `reporte_de_impacto` (`contenido`, `brigada`, `area_evaluada`, `indicador`, `valor`, `unidad`, `fecha_generacion`, `Actividad_idActividad`, `Usuario_idUsuario`) VALUES
('La reforestación incrementará la absorción de CO2 en aproximadamente 1.8 toneladas anuales.',
 'Brigada Ecológica', 'Absorción de carbono', 'CO2 absorbido por año', '1.8', 'toneladas',
 NOW() - INTERVAL 8 DAY, (SELECT idActividad FROM actividad WHERE titulo='Jornada de Reforestación' LIMIT 1), 202),

('El simulacro reveló que el tiempo de evacuación es 30% mayor al recomendado. Se propone ensanchar la salida del Pabellón B.',
 'Brigada de Gestión de Riesgo', 'Tiempo de evacuación', 'Tiempo de evacuación', '4.5', 'minutos',
 NOW() - INTERVAL 13 DAY, (SELECT idActividad FROM actividad WHERE titulo='Simulacro de Evacuación' LIMIT 1), 203),

('El operativo redujo los cruces peligrosos en un 85% comparado con días sin patrullaje.',
 'Brigada de Patrulla Escolar', 'Seguridad peatonal', 'Reducción de cruces peligrosos', '85', '%',
 NOW() - INTERVAL 5 DAY, (SELECT idActividad FROM actividad WHERE titulo='Operativo Paso Seguro' LIMIT 1), 204),

('La jornada redujo los reportes de conflicto entre 3ero A y B en un 60% la semana siguiente.',
 'Brigada de Convivencia y Paz', 'Conflictos entre secciones', 'Reducción de conflictos', '60', '%',
 NOW() - INTERVAL 10 DAY, (SELECT idActividad FROM actividad WHERE titulo='Jornada Anti-Bullying' LIMIT 1), 205),

('Se capacitaron 18 personas que ahora pueden brindar atención inmediata en la escuela.',
 'Brigada de Primeros Auxilios', 'Capacidad de respuesta', 'Personal capacitado en RCP', '18', 'personas',
 NOW() - INTERVAL 3 DAY, (SELECT idActividad FROM actividad WHERE titulo='Curso de Primeros Auxilios' LIMIT 1), 206),

('30 plántulas sembradas; se espera producción de hortalizas en 60 días.',
 'Brigada Mi Conuco Escolar', 'Producción agrícola', 'Plántulas sembradas', '30', 'unidades',
 NOW() - INTERVAL 18 DAY, (SELECT idActividad FROM actividad WHERE titulo='Siembra del Huerto Escolar' LIMIT 1), 208);

-- ══════════════════════════════════════════════════════════════
-- 12. CONFIGURACIÓN
-- ══════════════════════════════════════════════════════════════
INSERT INTO `configuracion` (`clave`, `valor`) VALUES
('mensaje_dia', '¡Bienvenidos al SBE! Recuerda: cada acción cuenta para una escuela más segura y armónica.')
ON DUPLICATE KEY UPDATE `valor` = VALUES(`valor`);

-- ══════════════════════════════════════════════════════════════
-- 13. AJUSTAR AUTO_INCREMENT
-- ══════════════════════════════════════════════════════════════
ALTER TABLE `brigada`  AUTO_INCREMENT = 200;
ALTER TABLE `usuario`  AUTO_INCREMENT = 400;
