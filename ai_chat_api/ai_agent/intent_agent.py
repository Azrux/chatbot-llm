import re
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from ai_chat_api.routes.db_routes.cars_data_available import get_makes, get_models

llm = ChatOpenAI(model="gpt-4", temperature=0)


def classify_user_input(user_msg: str, state) -> dict:
    makes = get_makes()
    models = get_models()
    prompt = f"""
      Eres un agente de atención al cliente de una concesionaria de autos.

      Analiza el siguiente mensaje de un usuario y responde SOLO en JSON puro, sin texto adicional.

      Si el mensaje del usuario contiene varias solicitudes (ej. búsqueda de autos y financiamiento), responde un array de objetos JSON ordenado por PRIORIDAD LÓGICA:

      ORDEN DE PRIORIDAD:
      1. "search_cars" - Primero buscar autos
      2. "select_car" - Luego seleccionar un auto específico  
      3. "more_info" - Si el usuario pide más información sobre un auto específico (requiere auto seleccionado)
      4. "search_financing" - Después buscar financiamiento (requiere auto seleccionado)
      5. "value_proposition" - Explicar propuesta de valor o responder preguntas generales sobre la empresa, sus servicios, sucursales, contacto, mantenimiento, garantías, procesos, o cualquier información general relacionada, aunque no se mencione el nombre de la empresa.
      6. "no_action" - Si el mensaje no se relaciona con autos, financiamiento o la empresa, responde con "no_action".

      Parameters disponibles:
      - make: Marca del auto (string, ej. "Toyota")
      - model: Modelo del auto (string, ej. "Corolla")
      - stock_id: ID de stock del auto (integer, ej. "123456")
      - price: Precio del auto (float, ej. 384999.0)
      - years: Años de financiamiento (integer, ej. 5)
      - km: Kilometraje del auto (integer, ej. 50000)
      - width: Ancho del auto (float, ej. 1.8)
      - height: Altura del auto (float, ej. 1.5)
      - length: Largo del auto (float, ej. 4.5)
      - version: Versión del auto (string, ej. "3.0 V6 TDI WOLFSBURG EDITION AUTO 4WD")
      - bluetooth: Si el auto tiene Bluetooth (boolean, ej. true)
      - car_play: Si el auto tiene GPS (boolean, ej. false)

      Ejemplo de respuesta con múltiples intenciones ORDENADAS:
      [
        {{
          "intent": "select_car",
          "parameters": {{
            "car_id": "225553"
          }}
        }},
        {{
          "intent": "search_financing",
          "parameters": {{
            "price": 384999.0
          }}
        }}
      ]

      Mensaje del usuario:
      {user_msg}

      State actual:
      {state}

      REGLAS IMPORTANTES:
        1. Si se pregunta por una marca/modelo, usa EXACTAMENTE los nombres de marcas/modelos de las listas disponibles
        2. Corrige errores de tipeo usando la opción más similar
        3. Mantén nombres compuestos completos (ej: "Land Rover", no "L Rover")
        4. Si el usuario pregunta sobre servicios, sucursales, contacto, mantenimiento, garantías, procesos, o cualquier información general de la empresa, responde con la intención "value_proposition", aunque no mencione el nombre de la empresa.

      EJEMPLOS DE CORRECCIÓN:
        - "L Rover" → "Land Rover"
        - "Mercedez" → "Mercedes Benz"

      Marcas disponibles: {makes}
      Modelos disponibles {models}
    """

    completion = llm.invoke([HumanMessage(content=prompt)])
    raw_output = completion.content.strip()  # type: ignore

    # Intenta encontrar JSON dentro de la respuesta
    json_match = re.search(r"(\{.*\}|\[.*\])", raw_output, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)
        try:
            result = json.loads(json_str)
            return result
        except json.JSONDecodeError:
            pass

    # Si no logró parsear nada válido:
    return {
        "intent": "unknown",
        "parameters": {}
    }
