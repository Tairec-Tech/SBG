"""
Contenido educativo de las 11 brigadas escolares — SBE.

Módulo neutral: SIN dependencias de UI/Flet ni colores.
Los colores, iconos y nombres visuales se obtienen de theme.BRIGADAS en runtime.
El contenido textual proviene del documento Guias_Brigadas_SBE_Ampliadas.docx.

Claves del diccionario coinciden con los slugs de brigadas_catalogo.py y theme.py.
"""

CONTENIDO_EDUCATIVO = {
    # ─────────────────────────────────────────────────────────────
    # 1. CONVIVENCIA Y PAZ
    # ─────────────────────────────────────────────────────────────
    "convivencia": {
        "proposito": (
            "Erradicar progresivamente el hostigamiento, el acoso escolar, "
            "la discriminación, la intolerancia y las formas de violencia "
            "cotidiana, promoviendo una cultura de igualdad, buen trato, "
            "diálogo y respeto mutuo."
        ),
        "identificacion": "Brazalete blanco o distintivo institucional claro.",
        "mision": (
            "Servir como equipo promotor de paz escolar, capaz de detectar "
            "conflictos tempranos, orientar a sus compañeros hacia el diálogo "
            "y activar los canales institucionales cuando una situación supere "
            "la mediación entre pares."
        ),
        "fundamento": (
            "Derecho al buen trato, corresponsabilidad educativa, convivencia "
            "escolar, cultura de paz y prevención de violencia. La brigada no "
            "sustituye a los docentes, directivos ni órganos competentes; "
            "acompaña, orienta y reporta."
        ),
        "perfil_brigadista": [
            "Empatía y disposición para escuchar sin burlarse ni juzgar.",
            "Lenguaje respetuoso y capacidad para guardar discreción.",
            "Actitud conciliadora, evitando tomar partido en conflictos.",
            "Compromiso con la igualdad, la inclusión y el rechazo a toda forma de acoso.",
            "Responsabilidad para reportar situaciones graves o reincidentes.",
        ],
        "funciones": [
            "Observación preventiva: identificar señales de aislamiento, burlas repetidas, apodos humillantes, agresiones verbales, rumores, exclusión o cambios bruscos de conducta.",
            "Mediación básica: facilitar conversaciones en conflictos menores, ayudando a que las partes expresen cómo se sienten y qué necesitan.",
            "Promoción del buen trato: organizar campañas de respeto, carteleras, círculos de diálogo y acuerdos de convivencia.",
            "Registro responsable: documentar conflictos recurrentes o graves en la plataforma, sin exponer detalles sensibles innecesarios.",
            "Derivación institucional: informar al docente responsable cuando exista violencia física, amenazas, discriminación, acoso persistente o riesgo emocional.",
        ],
        "protocolo": [
            "Detectar: observar la situación, identificar a los involucrados y evitar intervenir de forma impulsiva.",
            "Contener: mantener un tono calmado, separar verbalmente la discusión y evitar que otros estudiantes rodeen o graben el conflicto.",
            "Escuchar: permitir que cada parte exprese su versión usando frases como «yo siento» y «yo necesito».",
            "Acordar: si es un conflicto menor, ayudar a construir un acuerdo concreto de respeto.",
            "Reportar: si hay gravedad, reincidencia o riesgo, registrar el caso y notificar al adulto responsable.",
        ],
        "actividades_pedagogicas": [
            {"nombre": "Círculos de diálogo", "descripcion": "Encuentros semanales por aula para conversar sobre respeto, tolerancia, empatía, rumores y comunicación asertiva."},
            {"nombre": "Semáforo de convivencia", "descripcion": "Dinámica donde los estudiantes clasifican conductas en verde, amarillo o rojo según su impacto en el grupo."},
            {"nombre": "Mural del buen trato", "descripcion": "Cartelera con compromisos escritos por los estudiantes para mejorar el ambiente escolar."},
        ],
        "uso_sbe": [
            "Registrar incidentes de convivencia sin emitir juicios personales.",
            "Marcar nivel de prioridad y reincidencia cuando aplique.",
            "Consultar acuerdos o actividades de prevención programadas.",
            "Cargar evidencias pedagógicas como fotos de carteleras o actas de círculos de diálogo.",
        ],
        "indicadores": [
            "Número de conflictos mediados satisfactoriamente.",
            "Cantidad de círculos de diálogo realizados.",
            "Casos graves derivados al comité institucional.",
            "Participación estudiantil en campañas de convivencia.",
            "Reducción de reportes reincidentes por aula.",
        ],
        "limites_actuacion": [
            "No investigar casos graves por cuenta propia.",
            "No exponer públicamente nombres de estudiantes involucrados.",
            "No imponer sanciones.",
            "No reemplazar la intervención del docente, directivo, orientación o protección competente.",
        ],
        "checklist": [
            "La actividad tiene responsable adulto identificado.",
            "La actividad está asociada a una brigada, momento escolar u objetivo claro.",
            "La evidencia cargada no vulnera la privacidad de ningún estudiante.",
            "Los brigadistas conocen que pueden orientar, apoyar y reportar, pero no sancionar ni sustituir al personal responsable.",
            "El resultado de la actividad fue registrado en la plataforma.",
        ],
    },

    # ─────────────────────────────────────────────────────────────
    # 2. ECOLÓGICA
    # ─────────────────────────────────────────────────────────────
    "ecologica": {
        "proposito": (
            "Convertir la institución en un espacio de aprendizaje ambiental, "
            "promoviendo hábitos de consumo responsable, cuidado de áreas verdes, "
            "reciclaje, ahorro de recursos y participación estudiantil en acciones "
            "ecológicas concretas."
        ),
        "identificacion": "Brazalete verde o distintivo ambiental.",
        "mision": (
            "Actuar como guardianes de los recursos naturales del plantel y "
            "promotores de una cultura ambiental permanente, articulada con la "
            "comunidad educativa y con proyectos de aprendizaje productivo."
        ),
        "fundamento": (
            "Educación ambiental, corresponsabilidad ciudadana, protección de "
            "recursos naturales y participación escolar. La brigada orienta y "
            "promueve acciones, pero no manipula residuos peligrosos ni realiza "
            "labores de mantenimiento técnico."
        ),
        "perfil_brigadista": [
            "Interés por el ambiente, la limpieza y el cuidado de espacios comunes.",
            "Disciplina para registrar datos periódicos.",
            "Capacidad para motivar sin imponer.",
            "Cuidado en la manipulación de materiales reciclables seguros.",
            "Trabajo en equipo con docentes, personal obrero y comunidad.",
        ],
        "funciones": [
            "Puntos limpios: organizar estaciones de reciclaje y orientar a los estudiantes sobre separación de papel, cartón, plástico y otros materiales permitidos.",
            "Ecoeficiencia: realizar recorridos para verificar luces encendidas innecesariamente, fugas visibles de agua y uso responsable de recursos.",
            "Áreas verdes: apoyar jornadas de siembra, limpieza y mantenimiento básico de jardines o zonas verdes.",
            "Vocería ambiental: difundir efemérides, recomendaciones ecológicas y campañas de conservación.",
            "Registro ambiental: cargar en la plataforma cantidades recolectadas, actividades realizadas y evidencias fotográficas.",
        ],
        "protocolo": [
            "Diagnosticar: identificar espacios con problemas de basura, consumo excesivo o deterioro ambiental.",
            "Planificar: definir una acción concreta: reciclaje, limpieza, siembra, cartelera o campaña.",
            "Ejecutar: realizar la actividad con supervisión adulta y materiales seguros.",
            "Registrar: documentar cantidades, participantes, fotos y observaciones.",
            "Evaluar: comparar resultados con la meta propuesta y proponer mejoras.",
        ],
        "actividades_pedagogicas": [
            {"nombre": "Mi Escuela, Mi Primer Ecosistema", "descripcion": "Mapeo de zonas verdes, puntos de basura, fuentes de agua y espacios recuperables."},
            {"nombre": "Semana del reciclaje", "descripcion": "Competencia sana por secciones para recolectar y clasificar materiales aprovechables."},
            {"nombre": "Guardianes del agua", "descripcion": "Campaña para detectar fugas visibles, evitar desperdicio y promover hábitos de ahorro."},
        ],
        "uso_sbe": [
            "Registrar bitácoras verdes semanales.",
            "Cargar kilos de material recolectado por tipo.",
            "Registrar actividades de siembra y mantenimiento.",
            "Reportar necesidades ambientales al directivo o responsable.",
        ],
        "indicadores": [
            "Kilogramos de material reciclable recolectado.",
            "Número de jornadas ambientales realizadas.",
            "Áreas recuperadas o mantenidas.",
            "Participación por grado o sección.",
            "Cantidad de incidencias ambientales reportadas y atendidas.",
        ],
        "limites_actuacion": [
            "No manipular residuos biológicos, cortantes o peligrosos.",
            "No realizar reparaciones eléctricas o de plomería.",
            "No aplicar químicos sin autorización.",
            "No asumir tareas de limpieza pesada que correspondan a mantenimiento institucional.",
        ],
        "checklist": [
            "La actividad tiene responsable adulto identificado.",
            "La actividad está asociada a una brigada, momento escolar u objetivo claro.",
            "La evidencia cargada no vulnera la privacidad de ningún estudiante.",
            "Los brigadistas conocen que pueden orientar, apoyar y reportar, pero no sancionar ni sustituir al personal responsable.",
            "El resultado de la actividad fue registrado en la plataforma.",
        ],
    },

    # ─────────────────────────────────────────────────────────────
    # 3. GESTIÓN DE RIESGO
    # ─────────────────────────────────────────────────────────────
    "riesgo": {
        "proposito": (
            "Preparar a la comunidad educativa para prevenir, reducir y responder "
            "organizadamente ante amenazas como sismos, incendios, lluvias intensas, "
            "fallas estructurales, accidentes colectivos u otras emergencias escolares."
        ),
        "identificacion": "Distintivo naranja de seguridad o chaleco institucional.",
        "mision": (
            "Fortalecer la cultura preventiva del plantel mediante mapas de riesgo, "
            "simulacros, rutas de evacuación, inventario de seguridad y coordinación "
            "con Primeros Auxilios durante eventos de emergencia."
        ),
        "fundamento": (
            "Gestión integral del riesgo, autoprotección escolar, prevención de "
            "emergencias y corresponsabilidad institucional. Esta brigada coordina "
            "prevención y evacuación; la atención primaria corresponde a Primeros "
            "Auxilios bajo supervisión adulta."
        ),
        "perfil_brigadista": [
            "Serenidad ante situaciones de presión.",
            "Capacidad de seguir instrucciones y orientar grupos.",
            "Responsabilidad para reportar riesgos sin alarmar.",
            "Disciplina durante simulacros y evacuaciones.",
            "Respeto por las rutas, señalizaciones y protocolos del plantel.",
        ],
        "funciones": [
            "Mapa de riesgos: identificar zonas vulnerables: escaleras, tableros eléctricos, pasillos estrechos, filtraciones, vidrios rotos o rutas obstruidas.",
            "Rutas de evacuación: apoyar la señalización y verificación de salidas seguras y puntos de encuentro.",
            "Simulacros: participar en la organización, orientación y evaluación de ejercicios preventivos.",
            "Inventario de seguridad: registrar extintores, botiquines, señaléticas y necesidades detectadas.",
            "Reporte preventivo: cargar observaciones en la plataforma para que dirección priorice acciones.",
        ],
        "protocolo": [
            "Antes: observar riesgos, actualizar mapas, revisar rutas y participar en charlas preventivas.",
            "Durante: mantener la calma, orientar al grupo según la ruta establecida, evitar carreras y apoyar a personas vulnerables.",
            "Después: verificar presencia en punto de encuentro, reportar daños visibles y esperar instrucciones.",
            "Registro: documentar simulacro o evento real con fecha, participantes, incidencias y recomendaciones.",
            "Mejora: proponer ajustes al plan de emergencia escolar.",
        ],
        "actividades_pedagogicas": [
            {"nombre": "Detectives de Riesgos con Mapas Digitales", "descripcion": "Recorrido guiado para ubicar amenazas y registrarlas en un mapa institucional."},
            {"nombre": "Simulacro con evaluación", "descripcion": "Ejercicio de evacuación con cronometraje, observación de rutas y reporte final."},
            {"nombre": "Ruta segura", "descripcion": "Campaña visual para que cada aula conozca su salida y punto de encuentro."},
        ],
        "uso_sbe": [
            "Crear reportes de riesgo preventivo.",
            "Actualizar inventario de seguridad.",
            "Registrar simulacros y observaciones.",
            "Cargar evidencias fotográficas de zonas críticas.",
        ],
        "indicadores": [
            "Número de riesgos identificados.",
            "Riesgos atendidos o mitigados.",
            "Simulacros realizados por lapso/momento.",
            "Tiempo de evacuación estimado.",
            "Participación de aulas en actividades preventivas.",
        ],
        "limites_actuacion": [
            "No apagar incendios reales sin capacitación y supervisión.",
            "No manipular tableros eléctricos o estructuras peligrosas.",
            "No generar alarma innecesaria.",
            "No sustituir organismos de emergencia ni personal adulto responsable.",
        ],
        "checklist": [
            "La actividad tiene responsable adulto identificado.",
            "La actividad está asociada a una brigada, momento escolar u objetivo claro.",
            "La evidencia cargada no vulnera la privacidad de ningún estudiante.",
            "Los brigadistas conocen que pueden orientar, apoyar y reportar, pero no sancionar ni sustituir al personal responsable.",
            "El resultado de la actividad fue registrado en la plataforma.",
        ],
    },

    # ─────────────────────────────────────────────────────────────
    # 4. PATRULLA ESCOLAR
    # ─────────────────────────────────────────────────────────────
    "patrulla": {
        "proposito": (
            "Garantizar el resguardo de estudiantes en entradas, salidas y zonas "
            "de circulación peatonal, promoviendo la cultura vial, el orden, la "
            "cortesía y el uso responsable de los espacios cercanos al plantel."
        ),
        "identificacion": "Brazalete o distintivo rojo, señal manual de PARE y elementos autorizados por la institución.",
        "mision": (
            "Apoyar la movilidad segura de la comunidad educativa mediante "
            "orientación vial escolar, organización de filas, observación "
            "preventiva y educación del transeúnte responsable."
        ),
        "fundamento": (
            "Seguridad vial escolar, convivencia ciudadana y prevención de "
            "accidentes. La patrulla orienta y alerta; no sustituye a autoridades "
            "de tránsito ni debe exponerse a circulación peligrosa."
        ),
        "perfil_brigadista": [
            "Disciplina y puntualidad durante guardias.",
            "Comunicación clara y respetuosa.",
            "Capacidad para seguir instrucciones del docente responsable.",
            "Conciencia vial y autocuidado.",
            "Actitud de servicio sin autoritarismo.",
        ],
        "funciones": [
            "Guardia de entrada y salida: apoyar el orden de estudiantes en zonas autorizadas por la institución.",
            "Orientación peatonal: recordar normas básicas: mirar ambos lados, cruzar por zonas seguras y no correr.",
            "Cultura vial: realizar campañas sobre señales, semáforos, respeto a peatones y transporte escolar.",
            "Registro de turnos: participar en rotación justa de guardias mediante el calendario de la plataforma.",
            "Observación preventiva: reportar situaciones de riesgo como vehículos a exceso de velocidad, aglomeraciones o zonas sin señalización.",
        ],
        "protocolo": [
            "Ubicación: permanecer en acera o zona segura; nunca colocarse en medio de la calle sin autorización adulta.",
            "Observación: verificar tránsito, velocidad de vehículos y flujo de estudiantes.",
            "Señalización: usar el indicador PARE o gesto autorizado de manera clara, sin juegos ni distracciones.",
            "Paso ordenado: permitir el cruce solo cuando el docente responsable lo indique o cuando sea seguro.",
            "Reporte: informar incidentes, riesgos o incumplimientos graves.",
        ],
        "actividades_pedagogicas": [
            {"nombre": "Pasaporte del Transeúnte Responsable", "descripcion": "Estaciones de aprendizaje con señales, cruces simulados y normas de peatón."},
            {"nombre": "Mapa vial escolar", "descripcion": "Identificación de entradas, salidas, paradas, cruces y zonas de riesgo."},
            {"nombre": "Campaña de llegada segura", "descripcion": "Mensajes visuales para familias y estudiantes durante la entrada/salida."},
        ],
        "uso_sbe": [
            "Gestionar roster de guardias.",
            "Registrar incidencias viales o puntos de riesgo.",
            "Cargar actividades de cultura vial.",
            "Consultar calendario de rotación de patrulleros.",
        ],
        "indicadores": [
            "Guardias realizadas según calendario.",
            "Incidencias viales reportadas.",
            "Campañas de cultura vial ejecutadas.",
            "Participación por grado o sección.",
            "Reducción de aglomeraciones o reportes en entradas/salidas.",
        ],
        "limites_actuacion": [
            "No detener vehículos por cuenta propia.",
            "No ubicarse en zonas de alto riesgo sin adulto responsable.",
            "No usar pitos o elementos no autorizados.",
            "No discutir con conductores o representantes.",
        ],
        "checklist": [
            "La actividad tiene responsable adulto identificado.",
            "La actividad está asociada a una brigada, momento escolar u objetivo claro.",
            "La evidencia cargada no vulnera la privacidad de ningún estudiante.",
            "Los brigadistas conocen que pueden orientar, apoyar y reportar, pero no sancionar ni sustituir al personal responsable.",
            "El resultado de la actividad fue registrado en la plataforma.",
        ],
    },

    # ─────────────────────────────────────────────────────────────
    # 5. PRIMEROS AUXILIOS
    # ─────────────────────────────────────────────────────────────
    "auxilios": {
        "proposito": (
            "Brindar apoyo inmediato, responsable y básico ante lesiones leves, "
            "malestares o incidentes escolares, acompañando al afectado mientras "
            "se activa la ayuda adulta o médica correspondiente."
        ),
        "identificacion": "Distintivo amarillo o brazalete de apoyo sanitario escolar.",
        "mision": (
            "Promover una cultura de autocuidado, prevención de accidentes y "
            "respuesta inicial ordenada, trabajando coordinadamente con Gestión "
            "de Riesgos, docentes y personal directivo."
        ),
        "fundamento": (
            "Derecho a la salud, protección integral de niños, niñas y adolescentes, "
            "prevención escolar y corresponsabilidad. La brigada no diagnostica, "
            "no medica y no reemplaza al personal de salud."
        ),
        "perfil_brigadista": [
            "Calma y cuidado al hablar con una persona afectada.",
            "Higiene, responsabilidad y respeto por la privacidad.",
            "Capacidad para pedir ayuda de inmediato.",
            "Disposición para aprender técnicas básicas autorizadas.",
            "Compromiso con el registro correcto de incidentes.",
        ],
        "funciones": [
            "Inventario del botiquín: verificar insumos permitidos, fechas de vencimiento y necesidades de reposición.",
            "Atención básica: acompañar lesiones leves, golpes, mareos o malestares mientras llega el adulto responsable.",
            "Triage escolar inicial: identificar prioridad de atención sin diagnosticar: leve, requiere docente, requiere traslado o emergencia.",
            "Prevención: realizar campañas sobre hidratación, higiene, cuidado durante recreos y prevención de accidentes.",
            "Registro de casos: documentar incidentes atendidos, acciones realizadas y derivaciones.",
        ],
        "protocolo": [
            "Asegurar la zona: verificar que el lugar sea seguro antes de acercarse.",
            "Avisar: notificar de inmediato al docente, coordinación o responsable adulto.",
            "Acompañar: mantener al afectado tranquilo, sentado o en posición segura según orientación adulta.",
            "No medicar: no administrar medicamentos ni alimentos sin autorización.",
            "Registrar: anotar fecha, lugar, tipo de incidente, persona responsable y derivación si aplica.",
        ],
        "actividades_pedagogicas": [
            {"nombre": "Simulacro de traslado", "descripcion": "Práctica supervisada de traslado seguro y comunicación durante una emergencia."},
            {"nombre": "Botiquín responsable", "descripcion": "Jornada para revisar insumos permitidos y crear lista de reposición."},
            {"nombre": "Prevención en recreo", "descripcion": "Campaña sobre caídas, empujones, hidratación y juegos seguros."},
        ],
        "uso_sbe": [
            "Registrar casos atendidos y derivaciones.",
            "Actualizar inventario del botiquín.",
            "Reportar necesidad de reposición de insumos.",
            "Vincular incidentes con actividades o simulacros cuando corresponda.",
        ],
        "indicadores": [
            "Casos leves atendidos y registrados.",
            "Insumos vencidos detectados y reemplazados.",
            "Charlas de prevención realizadas.",
            "Tiempo de notificación al adulto responsable.",
            "Simulacros de atención y traslado ejecutados.",
        ],
        "limites_actuacion": [
            "No diagnosticar enfermedades.",
            "No administrar medicamentos.",
            "No movilizar lesionados graves sin indicación adulta o médica.",
            "No manipular sangre u otros fluidos sin medidas adecuadas y supervisión.",
        ],
        "checklist": [
            "La actividad tiene responsable adulto identificado.",
            "La actividad está asociada a una brigada, momento escolar u objetivo claro.",
            "La evidencia cargada no vulnera la privacidad de ningún estudiante.",
            "Los brigadistas conocen que pueden orientar, apoyar y reportar, pero no sancionar ni sustituir al personal responsable.",
            "El resultado de la actividad fue registrado en la plataforma.",
        ],
    },

    # ─────────────────────────────────────────────────────────────
    # 6. EDUCACIÓN FÍSICA
    # ─────────────────────────────────────────────────────────────
    "educacion_fisica": {
        "proposito": (
            "Promover la actividad física, la recreación, el deporte escolar, "
            "los juegos tradicionales y los hábitos de vida saludable como parte "
            "de la formación integral de los estudiantes."
        ),
        "identificacion": "Distintivo azul o identificación deportiva institucional.",
        "mision": (
            "Incentivar la participación activa, inclusiva y segura en actividades "
            "deportivas y recreativas, apoyando a docentes en la organización de "
            "eventos y en la prevención de lesiones."
        ),
        "fundamento": (
            "Derecho a la recreación, educación física, deporte y salud integral. "
            "La brigada apoya actividades pedagógicas y preventivas, sin sustituir "
            "al docente especialista."
        ),
        "perfil_brigadista": [
            "Entusiasmo por el deporte y la recreación.",
            "Respeto por la inclusión y la sana competencia.",
            "Cuidado del material deportivo.",
            "Capacidad para animar actividades sin excluir a nadie.",
            "Responsabilidad para reportar riesgos en canchas o espacios físicos.",
        ],
        "funciones": [
            "Promoción deportiva: organizar juegos intercursos, estaciones recreativas y actividades de integración.",
            "Pausas activas: dirigir rutinas breves de estiramiento, movilidad o respiración durante jornadas acordadas.",
            "Cuidado de espacios: verificar uso adecuado de canchas, balones, redes y material deportivo.",
            "Prevención de lesiones: recordar calentamiento, hidratación, calzado adecuado y respeto de reglas.",
            "Apoyo a mediciones: colaborar con docentes en registros básicos autorizados como talla, peso o participación, cuidando la privacidad.",
        ],
        "protocolo": [
            "Planificar: definir objetivo: recreación, integración, salud o evento deportivo.",
            "Preparar: revisar espacio, material, hidratación y normas.",
            "Calentar: iniciar con movilidad y estiramientos adecuados.",
            "Ejecutar: desarrollar la actividad con inclusión y respeto.",
            "Cerrar: registrar participantes, incidencias, logros y recomendaciones.",
        ],
        "actividades_pedagogicas": [
            {"nombre": "Pausas Activas Digitales", "descripcion": "Rutinas breves de movimiento en cambios de hora o momentos autorizados."},
            {"nombre": "Festival de juegos tradicionales", "descripcion": "Recuperación de juegos como trompo, perinola, metras, saltos y carreras recreativas."},
            {"nombre": "Reto de hábitos saludables", "descripcion": "Registro semanal de hidratación, descanso, actividad física y alimentación balanceada."},
        ],
        "uso_sbe": [
            "Programar eventos deportivos en calendario.",
            "Registrar participantes y resultados recreativos.",
            "Reportar estado de implementos o canchas.",
            "Cargar evidencias de jornadas deportivas.",
        ],
        "indicadores": [
            "Actividades físicas realizadas.",
            "Participación por sección.",
            "Implementos revisados o recuperados.",
            "Pausas activas ejecutadas.",
            "Incidencias o lesiones prevenidas/reportadas.",
        ],
        "limites_actuacion": [
            "No exigir rendimiento competitivo extremo.",
            "No excluir estudiantes por condición física.",
            "No permitir juegos peligrosos o sin supervisión.",
            "No divulgar medidas corporales de compañeros.",
        ],
        "checklist": [
            "La actividad tiene responsable adulto identificado.",
            "La actividad está asociada a una brigada, momento escolar u objetivo claro.",
            "La evidencia cargada no vulnera la privacidad de ningún estudiante.",
            "Los brigadistas conocen que pueden orientar, apoyar y reportar, pero no sancionar ni sustituir al personal responsable.",
            "El resultado de la actividad fue registrado en la plataforma.",
        ],
    },

    # ─────────────────────────────────────────────────────────────
    # 7. MI CONUCO ESCOLAR
    # ─────────────────────────────────────────────────────────────
    "conuco": {
        "proposito": (
            "Implementar el programa de siembra escolar como aula abierta para "
            "aprender agroecología, producción responsable, cuidado de semillas, "
            "compostaje y soberanía alimentaria desde la práctica."
        ),
        "identificacion": "Distintivo verde oliva o símbolo del conuco escolar.",
        "mision": (
            "Formar produciendo y producir formando, integrando saberes "
            "científicos, populares y comunitarios para transformar espacios "
            "escolares en zonas productivas, pedagógicas y biodiversas."
        ),
        "fundamento": (
            "Educación productiva, ambiente, soberanía alimentaria y "
            "participación comunitaria. La brigada desarrolla prácticas "
            "agroecológicas seguras y supervisadas."
        ),
        "perfil_brigadista": [
            "Interés por la siembra y el trabajo colaborativo.",
            "Paciencia para observar ciclos de crecimiento.",
            "Cuidado de herramientas y semillas.",
            "Respeto por saberes campesinos y comunitarios.",
            "Disciplina para registrar avances en bitácora.",
        ],
        "funciones": [
            "Preparación de suelo: apoyar limpieza ligera, delimitación de canteros y acondicionamiento orgánico.",
            "Siembra y trasplante: sembrar semillas o plántulas según calendario y orientación docente.",
            "Banco de semillas: identificar, clasificar y conservar semillas para próximas jornadas.",
            "Compostaje: recolectar residuos orgánicos permitidos y participar en elaboración de abono.",
            "Bitácora productiva: registrar fecha de siembra, riego, crecimiento, plagas observadas y cosecha.",
        ],
        "protocolo": [
            "Diagnosticar espacio: identificar luz, agua, suelo y seguridad del área.",
            "Planificar cultivo: elegir rubro, fecha y responsables.",
            "Preparar materiales: semillas, herramientas, abono, riego y señalización.",
            "Mantener: regar, observar, retirar malezas y registrar avances.",
            "Cosechar y evaluar: documentar producción, aprendizajes y mejoras.",
        ],
        "actividades_pedagogicas": [
            {"nombre": "Círculo del Abono", "descripcion": "Crear compostero con residuos orgánicos autorizados del comedor o áreas verdes."},
            {"nombre": "Banco de Semillas Escolar", "descripcion": "Colección identificada de semillas locales con fichas de origen y fecha."},
            {"nombre": "Calendario de Siembra", "descripcion": "Cartelera o registro digital de rubros, ciclos, responsables y cosechas."},
        ],
        "uso_sbe": [
            "Registrar bitácoras de siembra.",
            "Cargar fotos de crecimiento.",
            "Registrar cosechas o pérdidas.",
            "Programar riego y mantenimiento en calendario.",
        ],
        "indicadores": [
            "Canteros activos.",
            "Semillas registradas.",
            "Jornadas de riego/mantenimiento.",
            "Cosechas obtenidas.",
            "Participación estudiantil y comunitaria.",
        ],
        "limites_actuacion": [
            "No usar agroquímicos sin autorización.",
            "No manipular herramientas peligrosas sin adulto responsable.",
            "No consumir productos sin validación sanitaria.",
            "No abandonar el registro de riego y mantenimiento.",
        ],
        "checklist": [
            "La actividad tiene responsable adulto identificado.",
            "La actividad está asociada a una brigada, momento escolar u objetivo claro.",
            "La evidencia cargada no vulnera la privacidad de ningún estudiante.",
            "Los brigadistas conocen que pueden orientar, apoyar y reportar, pero no sancionar ni sustituir al personal responsable.",
            "El resultado de la actividad fue registrado en la plataforma.",
        ],
    },

    # ─────────────────────────────────────────────────────────────
    # 8. PATRIMONIO Y TURISMO
    # ─────────────────────────────────────────────────────────────
    "patrimonio": {
        "proposito": (
            "Fomentar sentido de pertenencia mediante el conocimiento, valoración, "
            "protección y difusión del patrimonio histórico, cultural, natural y "
            "comunitario del entorno escolar."
        ),
        "identificacion": "Distintivo rosado o insignia cultural institucional.",
        "mision": (
            "Investigar, documentar y compartir la memoria local para que los "
            "estudiantes reconozcan su comunidad como espacio de identidad, "
            "aprendizaje y posible turismo pedagógico."
        ),
        "fundamento": (
            "Patrimonio cultural, memoria histórica, identidad local, "
            "participación estudiantil y respeto a la diversidad cultural."
        ),
        "perfil_brigadista": [
            "Curiosidad por la historia local y las tradiciones.",
            "Respeto por relatos comunitarios y fuentes orales.",
            "Habilidad para investigar, entrevistar y registrar.",
            "Cuidado al fotografiar o documentar espacios.",
            "Orgullo por la identidad regional sin discriminar otras culturas.",
        ],
        "funciones": [
            "Atlas patrimonial: crear fichas de lugares, árboles, monumentos, personajes, tradiciones o espacios significativos.",
            "Investigación oral: entrevistar a adultos mayores, maestros pueblo, vecinos o cultores.",
            "Rutas pedagógicas: organizar recorridos dentro o fuera del plantel con objetivos de aprendizaje.",
            "Museo escolar: apoyar exposiciones de objetos, fotografías, relatos y símbolos locales.",
            "Difusión cultural: preparar carteleras, cápsulas digitales y presentaciones sobre efemérides o tradiciones.",
        ],
        "protocolo": [
            "Elegir tema: definir patrimonio material, natural o inmaterial a investigar.",
            "Recolectar información: entrevistas, fotos autorizadas, documentos o relatos.",
            "Verificar: contrastar datos con docentes o fuentes confiables.",
            "Registrar: crear ficha patrimonial en la plataforma.",
            "Difundir: presentar hallazgos mediante exposición, ruta o cartelera.",
        ],
        "actividades_pedagogicas": [
            {"nombre": "Cronistas Escolares", "descripcion": "Entrevistas a vecinos o docentes para rescatar relatos de la comunidad."},
            {"nombre": "Mapa de identidad", "descripcion": "Ubicación de sitios importantes en un plano escolar o comunitario."},
            {"nombre": "Museo vivo", "descripcion": "Exposición de tradiciones, fotografías y objetos con explicación estudiantil."},
        ],
        "uso_sbe": [
            "Registrar fichas patrimoniales.",
            "Cargar fotos autorizadas y descripciones.",
            "Programar expediciones pedagógicas.",
            "Vincular actividades con efemérides culturales.",
        ],
        "indicadores": [
            "Fichas patrimoniales creadas.",
            "Entrevistas realizadas.",
            "Rutas pedagógicas ejecutadas.",
            "Exposiciones escolares organizadas.",
            "Participación de comunidad y estudiantes.",
        ],
        "limites_actuacion": [
            "No publicar fotos de personas sin autorización.",
            "No manipular objetos patrimoniales sin supervisión.",
            "No inventar información histórica.",
            "No promover visitas externas sin permisos institucionales.",
        ],
        "checklist": [
            "La actividad tiene responsable adulto identificado.",
            "La actividad está asociada a una brigada, momento escolar u objetivo claro.",
            "La evidencia cargada no vulnera la privacidad de ningún estudiante.",
            "Los brigadistas conocen que pueden orientar, apoyar y reportar, pero no sancionar ni sustituir al personal responsable.",
            "El resultado de la actividad fue registrado en la plataforma.",
        ],
    },

    # ─────────────────────────────────────────────────────────────
    # 9. ARTES VISUALES
    # ─────────────────────────────────────────────────────────────
    "artes": {
        "proposito": (
            "Estimular la expresión estética, la creatividad, la comunicación "
            "visual y la participación cultural, utilizando las artes como "
            "herramienta para fortalecer valores, identidad y pensamiento crítico."
        ),
        "identificacion": "Distintivo lila o credencial artística institucional.",
        "mision": (
            "Convertir los espacios escolares en escenarios de expresión "
            "artística responsable, apoyando campañas educativas, efemérides, "
            "carteleras, murales y exposiciones estudiantiles."
        ),
        "fundamento": (
            "Derecho a la cultura, recreación, expresión artística y "
            "participación escolar. La brigada promueve arte educativo, "
            "respetuoso e inclusivo."
        ),
        "perfil_brigadista": [
            "Creatividad y gusto por el dibujo, color, diseño o manualidades.",
            "Respeto por la obra de otros compañeros.",
            "Cuidado de materiales e instalaciones.",
            "Capacidad para comunicar mensajes educativos visualmente.",
            "Disposición para trabajar en equipo y aceptar retroalimentación.",
        ],
        "funciones": [
            "Muralismo escolar: diseñar murales temáticos con mensajes de paz, ambiente, historia, deporte o derechos.",
            "Carteleras educativas: crear afiches, infografías y piezas visuales para campañas institucionales.",
            "Exposiciones: organizar muestras de dibujos, pinturas, collage, fotografía o artesanía.",
            "Identidad visual: apoyar señalética, decoración de eventos y presentación de proyectos.",
            "Registro artístico: documentar obras, autores, fechas y temas en la plataforma.",
        ],
        "protocolo": [
            "Definir mensaje: aclarar qué valor, efeméride o tema se desea comunicar.",
            "Bocetar: crear propuestas antes de intervenir espacios.",
            "Aprobar: presentar diseño al docente o directivo responsable.",
            "Ejecutar: realizar la obra con materiales adecuados y respeto por el espacio.",
            "Registrar: cargar evidencia y explicación del trabajo realizado.",
        ],
        "actividades_pedagogicas": [
            {"nombre": "Pinceladas de Paz", "descripcion": "Mural colectivo sobre convivencia, buen trato y respeto."},
            {"nombre": "Galería de Efemérides", "descripcion": "Exposición mensual vinculada a fechas culturales o históricas."},
            {"nombre": "Cartelera Viva", "descripcion": "Renovación periódica de carteleras con infografías hechas por estudiantes."},
        ],
        "uso_sbe": [
            "Registrar campañas visuales.",
            "Cargar fotos de murales y exposiciones.",
            "Programar actividades artísticas.",
            "Relacionar piezas con efemérides, brigadas o proyectos.",
        ],
        "indicadores": [
            "Obras realizadas.",
            "Carteleras actualizadas.",
            "Exposiciones organizadas.",
            "Participantes por actividad.",
            "Campañas visuales apoyadas.",
        ],
        "limites_actuacion": [
            "No intervenir paredes o mobiliario sin autorización.",
            "No usar mensajes ofensivos o discriminatorios.",
            "No desperdiciar materiales.",
            "No borrar trabajos ajenos sin permiso.",
        ],
        "checklist": [
            "La actividad tiene responsable adulto identificado.",
            "La actividad está asociada a una brigada, momento escolar u objetivo claro.",
            "La evidencia cargada no vulnera la privacidad de ningún estudiante.",
            "Los brigadistas conocen que pueden orientar, apoyar y reportar, pero no sancionar ni sustituir al personal responsable.",
            "El resultado de la actividad fue registrado en la plataforma.",
        ],
    },

    # ─────────────────────────────────────────────────────────────
    # 10. JUVENTUD PATRIÓTICA
    # ─────────────────────────────────────────────────────────────
    "patriotica": {
        "proposito": (
            "Fortalecer la conciencia histórica, el respeto por los símbolos "
            "patrios, la memoria colectiva, las efemérides nacionales y la "
            "participación cívica responsable dentro de la escuela."
        ),
        "identificacion": "Distintivo gris o símbolo cívico institucional.",
        "mision": (
            "Promover actos cívicos, investigaciones históricas, conversatorios "
            "y actividades formativas que ayuden a comprender la identidad "
            "nacional de manera crítica, respetuosa y educativa."
        ),
        "fundamento": (
            "Formación ciudadana, identidad nacional, cultura cívica y "
            "participación estudiantil. La brigada debe mantener enfoque "
            "pedagógico, plural y respetuoso."
        ),
        "perfil_brigadista": [
            "Respeto por símbolos patrios e historia nacional.",
            "Capacidad de hablar en público y organizar actos.",
            "Interés por efemérides y memoria histórica.",
            "Responsabilidad y disciplina protocolar.",
            "Actitud respetuosa frente a opiniones diversas.",
        ],
        "funciones": [
            "Protocolo cívico: apoyar actos de bandera, himnos, conmemoraciones y fechas patrias.",
            "Efemérides: investigar y explicar fechas históricas mediante carteleras o presentaciones.",
            "Escenificaciones: participar en dramatizaciones de hechos históricos con enfoque pedagógico.",
            "Conversatorios: organizar espacios de diálogo sobre ciudadanía, territorio, memoria y valores cívicos.",
            "Archivo cívico: registrar actividades patrióticas, participantes y evidencias.",
        ],
        "protocolo": [
            "Identificar efeméride: seleccionar fecha o tema histórico.",
            "Investigar: consultar fuentes, docentes y materiales autorizados.",
            "Preparar actividad: definir acto, exposición, dramatización o cartelera.",
            "Ejecutar con respeto: mantener tono educativo y orden institucional.",
            "Registrar: documentar participantes, aprendizajes y evidencias.",
        ],
        "actividades_pedagogicas": [
            {"nombre": "Tribuna Bolivariana", "descripcion": "Conversatorios sobre pensamiento histórico y ciudadanía responsable."},
            {"nombre": "Calendario Patrio Escolar", "descripcion": "Planificación anual de efemérides y actos cívicos."},
            {"nombre": "Voces de la Historia", "descripcion": "Dramatizaciones breves de personajes o hechos relevantes con reflexión final."},
        ],
        "uso_sbe": [
            "Programar actos cívicos.",
            "Registrar efemérides trabajadas.",
            "Cargar evidencias de conversatorios o dramatizaciones.",
            "Vincular actividades con niveles educativos y momentos escolares.",
        ],
        "indicadores": [
            "Actos cívicos apoyados.",
            "Efemérides desarrolladas.",
            "Materiales históricos producidos.",
            "Participantes por actividad.",
            "Evidencias cargadas en plataforma.",
        ],
        "limites_actuacion": [
            "No convertir actividades en imposición ideológica.",
            "No excluir opiniones respetuosas.",
            "No usar símbolos patrios de forma inadecuada.",
            "No difundir información histórica sin verificación.",
        ],
        "checklist": [
            "La actividad tiene responsable adulto identificado.",
            "La actividad está asociada a una brigada, momento escolar u objetivo claro.",
            "La evidencia cargada no vulnera la privacidad de ningún estudiante.",
            "Los brigadistas conocen que pueden orientar, apoyar y reportar, pero no sancionar ni sustituir al personal responsable.",
            "El resultado de la actividad fue registrado en la plataforma.",
        ],
    },

    # ─────────────────────────────────────────────────────────────
    # 11. DERECHOS HUMANOS
    # ─────────────────────────────────────────────────────────────
    "ddhh": {
        "proposito": (
            "Promover el conocimiento y ejercicio responsable de derechos, "
            "deberes, igualdad, inclusión, buen trato y mecanismos de protección "
            "dentro del entorno educativo."
        ),
        "identificacion": "Distintivo azul oscuro o insignia de derechos y deberes.",
        "mision": (
            "Actuar como equipo promotor de dignidad humana, justicia escolar, "
            "participación y orientación básica, canalizando situaciones sensibles "
            "hacia adultos responsables e instancias institucionales."
        ),
        "fundamento": (
            "Protección integral de niños, niñas y adolescentes, igualdad, "
            "no discriminación, buen trato y participación. La brigada orienta "
            "y reporta; no investiga ni sanciona por cuenta propia."
        ),
        "perfil_brigadista": [
            "Sentido de justicia y respeto por la dignidad de todos.",
            "Discreción ante situaciones sensibles.",
            "Capacidad para orientar sin juzgar.",
            "Conocimiento básico de deberes y derechos escolares.",
            "Compromiso con inclusión y no discriminación.",
        ],
        "funciones": [
            "Promoción de derechos: realizar charlas, carteleras y campañas sobre derechos y deberes.",
            "Buen trato: apoyar actividades que promuevan respeto, inclusión y lenguaje no discriminatorio.",
            "Orientación inicial: indicar a compañeros a qué adulto o canal institucional acudir ante una vulneración.",
            "Detección preventiva: observar señales de exclusión, maltrato, discriminación o vulnerabilidad.",
            "Registro responsable: documentar actividades formativas y reportes institucionales sin divulgar información sensible.",
        ],
        "protocolo": [
            "Escuchar: recibir inquietudes con respeto y sin prometer soluciones imposibles.",
            "Orientar: explicar canales institucionales: docente, coordinación, dirección u orientación.",
            "Reportar: si hay riesgo, maltrato o vulneración, informar al adulto responsable.",
            "Proteger privacidad: no difundir nombres, relatos o evidencias sensibles.",
            "Acompañar: promover seguimiento institucional sin sustituir a autoridades competentes.",
        ],
        "actividades_pedagogicas": [
            {"nombre": "Mi Voz Cuenta", "descripcion": "Trípticos, volantes digitales o charlas sobre derechos y deberes."},
            {"nombre": "Mapa de Protección Escolar", "descripcion": "Identificación de adultos, espacios y canales de ayuda dentro del plantel."},
            {"nombre": "Semana de la Inclusión", "descripcion": "Actividades para valorar diversidad, accesibilidad, respeto y participación."},
        ],
        "uso_sbe": [
            "Registrar actividades de formación ciudadana.",
            "Canalizar reportes sensibles hacia responsables autorizados.",
            "Cargar evidencias pedagógicas sin exponer datos privados.",
            "Consultar campañas o materiales de derechos y deberes.",
        ],
        "indicadores": [
            "Charlas realizadas.",
            "Materiales informativos creados.",
            "Casos orientados a adultos responsables.",
            "Campañas de inclusión ejecutadas.",
            "Participación estudiantil por nivel.",
        ],
        "limites_actuacion": [
            "No investigar denuncias graves por cuenta propia.",
            "No publicar nombres ni detalles sensibles.",
            "No confrontar agresores sin adulto responsable.",
            "No emitir sanciones ni decisiones institucionales.",
        ],
        "checklist": [
            "La actividad tiene responsable adulto identificado.",
            "La actividad está asociada a una brigada, momento escolar u objetivo claro.",
            "La evidencia cargada no vulnera la privacidad de ningún estudiante.",
            "Los brigadistas conocen que pueden orientar, apoyar y reportar, pero no sancionar ni sustituir al personal responsable.",
            "El resultado de la actividad fue registrado en la plataforma.",
        ],
    },
}
