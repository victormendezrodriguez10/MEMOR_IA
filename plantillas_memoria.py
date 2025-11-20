"""
Plantillas de memorias técnicas para diferentes tipos de proyectos
"""

PLANTILLAS_MEMORIA = {
    "construccion": {
        "nombre": "Construcción y Obra Civil",
        "estructura": """
        1. PRESENTACIÓN DE LA EMPRESA Y CAPACIDAD TÉCNICA
        2. ANÁLISIS DEL PROYECTO Y COMPRENSIÓN DEL OBJETO
        3. METODOLOGÍA DE TRABAJO Y FASES DE EJECUCIÓN
        4. RECURSOS HUMANOS Y ORGANIZACIÓN
        5. MAQUINARIA Y MEDIOS TÉCNICOS
        6. PROGRAMA DE TRABAJO Y PLANIFICACIÓN
        7. CONTROL DE CALIDAD Y SEGUIMIENTO
        8. PREVENCIÓN DE RIESGOS LABORALES Y SEGURIDAD
        9. SOSTENIBILIDAD Y MEDIO AMBIENTE
        10. GARANTÍAS Y MANTENIMIENTO
        """,
        "contenido_tipo": {
            "metodologia": "Describe procesos constructivos, fases de obra, técnicas específicas según normativa vigente",
            "recursos": "Equipo técnico cualificado con experiencia en proyectos similares, maquinaria especializada",
            "calidad": "Sistemas de control de calidad conforme a normativas UNE, certificaciones ISO",
            "seguridad": "Plan de seguridad y salud, medidas preventivas, coordinación de actividades"
        }
    },

    "energia_fotovoltaica": {
        "nombre": "Instalaciones Fotovoltaicas",
        "estructura": """
        1. EXPERIENCIA EN INSTALACIONES FOTOVOLTAICAS
        2. ANÁLISIS TÉCNICO DE LA INSTALACIÓN PROPUESTA
        3. METODOLOGÍA DE INSTALACIÓN Y MONTAJE
        4. EQUIPO TÉCNICO ESPECIALIZADO EN FOTOVOLTAICA
        5. EQUIPOS Y HERRAMIENTAS ESPECIALIZADAS
        6. PROGRAMA DE EJECUCIÓN Y HITOS
        7. CONTROL DE CALIDAD Y PRUEBAS
        8. MANTENIMIENTO Y GARANTÍAS
        9. GESTIÓN MEDIOAMBIENTAL
        10. TRAMITACIÓN ADMINISTRATIVA Y LEGALIZACIONES
        """,
        "contenido_tipo": {
            "metodologia": "Proceso de instalación de paneles, inversores, estructura soporte, cableado DC/AC",
            "recursos": "Instaladores certificados, técnicos en energía solar, ingenieros especializados",
            "calidad": "Pruebas eléctricas, mediciones de aislamiento, verificación de potencias",
            "tramitacion": "Gestión de permisos, memoria técnica de diseño, certificado de instalación"
        }
    },

    "instalaciones_electricas": {
        "nombre": "Instalaciones Eléctricas",
        "estructura": """
        1. CAPACIDAD TÉCNICA EN INSTALACIONES ELÉCTRICAS
        2. ANÁLISIS DE LA INSTALACIÓN ELÉCTRICA REQUERIDA
        3. METODOLOGÍA DE INSTALACIÓN ELÉCTRICA
        4. PERSONAL TÉCNICO CUALIFICADO
        5. MEDIOS TÉCNICOS Y HERRAMIENTAS
        6. PLANIFICACIÓN Y CRONOGRAMA
        7. VERIFICACIONES Y PRUEBAS ELÉCTRICAS
        8. SEGURIDAD ELÉCTRICA Y PREVENCIÓN
        9. CUMPLIMIENTO REBT Y NORMATIVA
        10. MANTENIMIENTO Y ASISTENCIA TÉCNICA
        """,
        "contenido_tipo": {
            "metodologia": "Instalación de cuadros, canalización, cableado, protecciones según REBT",
            "recursos": "Electricistas autorizados, técnicos con carnet profesional, ingenieros",
            "calidad": "Mediciones de continuidad, aislamiento, verificación de protecciones",
            "normativa": "Cumplimiento REBT, UNE 20460, certificaciones de conformidad"
        }
    },

    "servicios_mantenimiento": {
        "nombre": "Servicios de Mantenimiento",
        "estructura": """
        1. EXPERIENCIA EN SERVICIOS DE MANTENIMIENTO
        2. ANÁLISIS DE NECESIDADES DE MANTENIMIENTO
        3. METODOLOGÍA DE MANTENIMIENTO PROPUESTA
        4. ORGANIZACIÓN DEL SERVICIO
        5. RECURSOS HUMANOS Y TÉCNICOS
        6. PLANIFICACIÓN Y FRECUENCIAS
        7. SISTEMA DE GESTIÓN Y CONTROL
        8. ATENCIÓN DE EMERGENCIAS Y AVERÍAS
        9. MEJORA CONTINUA Y OPTIMIZACIÓN
        10. REPORTING Y SEGUIMIENTO
        """,
        "contenido_tipo": {
            "metodologia": "Mantenimiento preventivo, correctivo, predictivo según necesidades",
            "recursos": "Técnicos multidisciplinares, servicio 24h, repuestos y herramientas",
            "calidad": "Procedimientos normalizados, registro de actuaciones, indicadores KPI",
            "mejora": "Análisis de fallos, propuestas de mejora, optimización de recursos"
        }
    }
}

CRITERIOS_COMUNES = {
    "solvencia_tecnica": {
        "desarrollo": """
        La solvencia técnica se demuestra a través de la experiencia acumulada en proyectos similares,
        la cualificación del equipo técnico y los medios materiales disponibles. Nuestra empresa cuenta
        con [X] años de experiencia en el sector, habiendo ejecutado más de [X] proyectos de características
        similares al presente contrato.
        """
    },

    "metodologia_trabajo": {
        "desarrollo": """
        La metodología de trabajo propuesta se fundamenta en un enfoque sistemático y planificado,
        garantizando la correcta ejecución del proyecto en tiempo y forma. Se establecen fases claramente
        definidas con hitos de control, permitiendo un seguimiento exhaustivo del avance de los trabajos.
        """
    },

    "recursos_humanos": {
        "desarrollo": """
        El equipo humano asignado al proyecto está compuesto por profesionales con amplia experiencia
        y cualificación específica en el sector. Todos los técnicos cuentan con la formación reglamentaria
        y las certificaciones necesarias para el desarrollo de sus funciones.
        """
    },

    "control_calidad": {
        "desarrollo": """
        El sistema de control de calidad implementado garantiza el cumplimiento de todas las especificaciones
        técnicas y normativas aplicables. Se establecen puntos de inspección y verificación en cada fase
        del proyecto, documentando todos los controles realizados.
        """
    }
}