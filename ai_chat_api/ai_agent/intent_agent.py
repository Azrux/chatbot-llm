from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import json
import re

llm = ChatOpenAI(model="gpt-4", temperature=0)


def classify_user_input(user_msg: str, state) -> dict:
    prompt = f"""
Eres un agente de atención al cliente de una concesionaria de autos.

Analiza el siguiente mensaje de un usuario y responde SOLO en JSON puro, sin texto adicional.

[... tu prompt actual ...]

Si el mensaje del usuario contiene varias solicitudes (ej. búsqueda de autos y financiamiento), responde un array de objetos JSON ordenado por PRIORIDAD LÓGICA:

ORDEN DE PRIORIDAD:
1. "search_cars" - Primero buscar autos
2. "select_car" - Luego seleccionar un auto específico  
3. "search_financing" - Después buscar financiamiento (requiere auto seleccionado)
4. "value_proposition" - Explicar propuesta de valor
5. "no_action" - Acciones sin prioridad específica

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
