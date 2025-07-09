# Roadmap y Backlog

## 1. MVP

- Procesamiento de mensajes de WhatsApp vía Twilio Sandbox
- Clasificación de intenciones y respuestas automáticas
- Manejo de estado de conversación en archivos JSON
- Búsqueda y selección de autos desde CSV
- Opciones de financiamiento simuladas

## 2. Refactor y robustez

- Refactorizar la estructura de carpetas y módulos
- Mejorar manejo de errores y logs
- Validar y sanitizar inputs del usuario
- Tests unitarios y de integración básicos
- Documentación técnica y de usuario

## 3. Persistencia y escalabilidad

- Migrar almacenamiento de estado y datos a una base de datos real (ej: PostgreSQL, MongoDB)
- Implementar ORM (ej: SQLAlchemy, Tortoise)
- Soporte para múltiples usuarios concurrentes y sesiones
- Despliegue en un entorno cloud (Heroku, AWS, GCP, Azure, etc.)
- Configuración de variables de entorno seguras (AWS Secrets Manager, Infisical)

## 4. Producción y monitoreo

- Migrar de Twilio Sandbox a número de WhatsApp verificado
- Certificados SSL y HTTPS
- Monitoreo y alertas (logs, errores, uptime)
- Backups automáticos de la base de datos
- Dashboard de métricas de uso y performance

## 5. Experiencia de usuario y features avanzadas

- Mejorar prompts y respuestas para mayor naturalidad
- Soporte para imágenes y multimedia (catálogos, fotos de autos)
- Integración con CRM o sistemas internos de la concesionaria
- Feedback de usuarios y mejoras continuas

---

## Backlog

- Refactorizar el manejo de estado para usar una base de datos relacional/noSQL
- Implementar autenticación y autorización para endpoints sensibles
- Agregar validaciones de datos en los endpoints (ej: precios, IDs)
- Mejorar la gestión de errores y mensajes de error amigables
- Escribir tests unitarios para los módulos principales
- Escribir tests de integración para el flujo completo (WhatsApp → Twilio → Bot → Respuesta)
- Automatizar el despliegue (Dockerfile, CI/CD)
- Configurar variables de entorno seguras y centralizadas
- Documentar la API y el flujo de conversación
- Agregar logs estructurados y alertas de errores críticos
- Implementar métricas de uso (número de usuarios, mensajes, autos consultados, etc.)
- Preparar scripts de migración de datos (de CSV/JSON a base de datos)
- Mejorar la experiencia conversacional (respuestas más naturales, manejo de contexto)
- Soporte para mensajes multimedia (imágenes de autos, catálogos)
- Integrar con sistemas internos (CRM, inventario, etc.)
- Realizar pruebas de carga y stress
- Solicitar feedback a usuarios reales y ajustar el flujo conversacional
