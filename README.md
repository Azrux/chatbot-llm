# Chatbot de Autos para WhatsApp (Twilio + OpenAI)

Este proyecto es un chatbot de atención para concesionaria de autos, integrado con WhatsApp vía Twilio y usando modelos de OpenAI para procesamiento de lenguaje natural.

---

## 🚀 ¿Cómo iniciar?

1. **Instalar dependencias**

    ```bash
    pip install -r requirements.txt
    ```

2. **Configurar variables de entorno**

    - Copia el archivo `.env.template` a `.env` y completá los valores requeridos:

    ```env
    OPENAI_API_KEY=tu_clave_openai
    TWILIO_AUTH_TOKEN=tu_auth_token
    TWILIO_ACCOUNT_SID=tu_account_sid
    ```

3. **Iniciar el servidor**

    - Si tenés `make`:

        ```bash
        make server-init
        ```

    - Si no tenés `make`:

        ```bash
        source venv/Scripts/activate  # En Windows
        # o
        source venv/bin/activate      # En Linux/Mac
        python app.py
        ```

4. **Exponer el servidor a internet**

    - Si tenés [ngrok](https://ngrok.com/):

        ```bash
        ngrok http 5000
        ```

    - Copiá la URL pública que te da ngrok (ej.: `https://xxxx.ngrok.io`).

    - Si usás VSCode y el puerto 5000 está expuesto, podés usar la URL que te da VSCode (usualmente algo como `https://<tu-workspace>.vscode.app:5000`).

5. **Configurar el sandbox de WhatsApp en Twilio**

    - Ingresá a [Twilio Sandbox for WhatsApp](https://www.twilio.com/console/sms/whatsapp/sandbox).

    - Enviá el mensaje de código desde tu WhatsApp personal al número del sandbox para activar la conversación.

    - En la configuración del sandbox, actualizá la URL del webhook para mensajes entrantes:

        ```txt
        <tu-url-publica>/api/twilio/webhook
        ```

        Ejemplo:

        ```txt
        https://xxxx.ngrok.io/api/twilio/webhook
        ```

6. **¡Listo!**

    - Ahora podés enviar mensajes desde WhatsApp al número del sandbox y conversar con la IA.

---

## 📄 Estructura del proyecto
```
ai_chat_api/
│
├── models/                      # Modelos de datos y lógica de negocio
│   ├── stock_model.py           # Modelo de datos para el stock de autos
│   └── stock_filter.py          # Lógica para filtrar autos según criterios
│
├── routes/                      # Rutas/endpoints de la API Flask
│   ├── ai_routes.py             # Endpoints para interacción con la IA
│   ├── business_routes.py       # Endpoints para lógica de negocio (financiamiento)
│   ├── scrape_kavak_site        # Script para scrapear datos del sitio de Kavak
│   ├── twilio_routes.py         # Webhook y endpoints para integración con Twilio
│   └── db_routes.py             # Rutas relacionadas a la base de datos
│       ├── car.py               # Operaciones CRUD para autos
│       ├── cars_data_available.py # Gestión de datos de autos disponibles
│       └── state.py             # Manejo del estado de la conversación
│
├── ai_agent/                    # Lógica del agente conversacional y sus herramientas
│   ├── __init__.py              # Inicialización del módulo
│   ├── tools.py                 # Herramientas auxiliares para el agente (búsqueda, financiamiento)
│   ├── agents.py                # Definición de los agentes principales
│   ├── intent_agent.py          # Clasificador de intenciones del usuario
│   ├── state.py                 # Definición y manejo del estado conversacional
│   ├── agent_node.py            # Nodo principal de procesamiento del agente
│   └── handlers.py              # Handlers para cada intención específica
│       ├── more_info.py         # Handler para solicitudes de más información
│       ├── no_action.py         # Handler para mensajes sin acción requerida
│       ├── search_cars.py       # Handler para búsqueda de autos
│       ├── search_financing.py  # Handler para opciones de financiamiento
│       ├── select_car.py        # Handler para selección de auto
│       └── value_proposition.py # Handler para explicar la propuesta de valor
│
├── config.py                    # Configuración global de la app (carga de variables de entorno)
├── app.py                       # Archivo principal de la aplicación Flask
├── .gitignore                   # Archivos y carpetas a ignorar por git
├── sample_caso_ai_engineer.csv  # Archivo de ejemplo con datos de autos
├── Makefile                     # Comandos automatizados para desarrollo y despliegue
├── .env.template                # Plantilla de variables de entorno
└── requirements.txt             # Dependencias del proyecto
```