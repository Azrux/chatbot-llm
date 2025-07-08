"""
Módulo para manejar la solicitud de opciones de financiamiento para un auto seleccionado.
"""
from langchain_core.messages import HumanMessage
from ai_chat_api.ai_agent.state import AgentState
from ai_chat_api.ai_agent.agents import gpt_turbo
from ai_chat_api.ai_agent.tools import get_financing


def handle_search_financing(state: AgentState, params: dict) -> AgentState:
    """
    Maneja la solicitud de opciones de financiamiento para un auto seleccionado.
    """
    # Buscar si ya hay un auto seleccionado
    car = state.selected_car
    if not car:
        # Buscar en cars_found si hay parámetros de make/model
        make = params.get("make")
        model = params.get("model")
        if not make or not model:
            state.agent_reply = (
                "No encontré el auto del que quieres financiamiento. "
                "¿Podrías decirme la marca y modelo?"
            )
            return state

        car = next(
            (c for c in state.cars_found  # type: ignore
             if make.lower() in c["make"].lower() and model.lower() in c["model"].lower()),
            None
        )
        if not car:
            state.agent_reply = (
                "No encontré el auto del que quieres financiamiento. "
                "¿Podrías decirme la marca y modelo?"
            )
            return state

        state.selected_car = car

    price = car["price"]
    years = params.get("years")

    financing = get_financing(price, years)
    state.financing_options = financing

    if not financing:
        state.agent_reply = "No encontré opciones de financiamiento. ¿Quieres saber sobre otros modelos?"
        return state

    last_6_messages = state.conversation_history[-6:]

    prompt = f"""
        El usuario preguntó:
        {state.user_msg}

        Auto seleccionado:
        {car}

        Opciones de financiación:
        {financing}

        Redacta un mensaje breve, cordial, en español para presentarle estas opciones.
        El mensaje debe ser claro y directo, evitando tecnicismos innecesarios y explicándole al usuario cómo funcionan las cuotas y tasas de interés.
        No incluyas información irrelevante o detalles técnicos complejos.

        Responde en relación a los últimos mensajes intercambiados con el usuario.

        Últimos 6 mensajes de la conversación: {last_6_messages}

        Debes asegurarte de que las respuestas sean:
            - Coherentes y relevantes para la pregunta del usuario
            - Apropiadas para el contexto de venta de autos
            - Profesionales y útiles

        Las respuestas deben responder directamente a la pregunta sin información irrelevante.

        Asegúrate de que la respuesta tenga sentido en el contexto de la conversación y que no contenga errores o información confusa.
    """
    completion = gpt_turbo.invoke([HumanMessage(content=prompt)])
    state.agent_reply = completion.content  # type: ignore
    return state
