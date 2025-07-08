""" 
Módulo para manejar la selección de un auto de una lista de autos encontrados.
"""
from ai_chat_api.ai_agent.state import AgentState


def handle_select_car(state: AgentState, params: dict) -> AgentState:
    """
    Handle the selection of a car from the list of found cars.
    """
    stock_id = params.get("stock_id")
    car = next(
        (c for c in state.cars_found if str(  # type: ignore
            c["stock_id"]) == str(stock_id)),
        None
    )
    if not car:
        state.agent_reply = "No pude encontrar ese auto. ¿Podrías darme más detalles?"
        return state

    state.selected_car = car
    state.agent_reply = (
        f"Seleccionaste el {car['year']} {car['make']} {car['model']} "
        f"de ${car['price']}. ¿Quieres saber opciones de financiamiento?"
    )
    return state
