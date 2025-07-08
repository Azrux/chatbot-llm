import requests
from typing import Optional
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

BASE_URL = "http://127.0.0.1:5000"


def get_cars(filters):
    """
    - Recibe el texto del usuario
    - Llama a /api/db/cars
    - Devuelve un dict siempre, incluso si ocurre error.
    """

    try:
        resp = requests.post(
            f"{BASE_URL}/api/db/cars",
            json=filters,
            timeout=5
        )
        resp.raise_for_status()
        cars = resp.json()

        print(f"Autos encontrados: {cars}")

        if not cars.get("cars"):
            return {
                "cars": [],
                "error": "No se encontraron autos con esos filtros."
            }

        return cars

    except Exception as e:
        return {
            "cars": [],
            "error": f"Ocurrió un error buscando autos: {str(e)}"
        }


def get_financing(price: str, years: Optional[int]) -> str:
    """
    - Recibe el texto del usuario
    - Llama a /api/business/calculate-financiation
    - Envía las opciones al LLM para que genere la respuesta
    """

    try:
        resp = requests.get(
            f"{BASE_URL}/api/business/calculate-financiation?price={price}&years={years}",
            timeout=5
        )
        resp.raise_for_status()
        financing_options = resp.json()

        return financing_options

    except Exception as e:
        return f"Ocurrió un error calculando financiación: {str(e)}"
