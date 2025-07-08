from ai_chat_api.ai_agent.state import AgentState
from ai_chat_api.ai_agent.tools import get_cars


def handle_search_cars(state: AgentState, params: dict) -> AgentState:
    """
    Handle the search for cars based on the provided parameters.
    This function updates the agent state with the results of the car search.
    """
    cars_response = get_cars(params)
    car_list = cars_response.get("cars", [])
    state.cars_found = car_list

    if not car_list:
        state.agent_reply = "No encontré autos con esos datos. Te interesa algún otro modelo?"
        return state

    if len(car_list) == 1:
        car = car_list[0]
        state.selected_car = car
        state.agent_reply = (
            f"Encontré un auto que coincide: "
            f"{car['year']} {car['make']} {car['model']} a ${car['price']}.\n"
            f"¿Quieres conocer opciones de financiamiento?"
        )
    else:
        cars_text = "\n".join(
            f"- ID {c['stock_id']}: {c['year']} {c['make']} {c['model']} ${c['price']}"
            for c in car_list
        )
        state.agent_reply = (
            "Encontré varios autos que coinciden:\n"
            f"{cars_text}\n"
            "¿Te interesa alguno?"
        )
    return state
