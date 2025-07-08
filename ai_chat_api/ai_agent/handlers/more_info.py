"""
Módulo para manejar la solicitud de más información sobre un auto seleccionado.
"""
from langchain_core.messages import HumanMessage
from ai_chat_api.ai_agent.state import AgentState
from ai_chat_api.ai_agent.agents import gpt_turbo


def handle_more_info(state: AgentState, params: dict) -> AgentState:
    """
    Maneja la solicitud de más información sobre un auto seleccionado.
    """
    # Buscar si ya hay un auto seleccionado
    car = state.selected_car
    if not car:
        # Buscar en cars_found si hay parámetros de make/model
        make = params.get("make")
        model = params.get("model")

        if not make or not model:
            state.agent_reply = (
                "No encontré el auto del que quieres más información. "
                "¿Podrías decirme al menos la marca y el modelo?"
            )
            return state

        car = next(
            (c for c in state.cars_found  # type: ignore
             if make.lower() in c["make"].lower() and model.lower() in c["model"].lower()),
            None
        )
        if not car:
            state.agent_reply = (
                "No encontré el auto del que quieres más información. "
                "¿Podrías decirme la marca y modelo?"
            )
            return state

        state.selected_car = car

    last_6_messages = state.conversation_history[-6:]

    prompt = f"""
        El usuario preguntó:
        {state.user_msg}

        Auto seleccionado:
        {car}

        Redacta un mensaje breve, cordial, para darle más información sobre este auto.
        El mensaje debe ser claro y directo, evitando tecnicismos innecesarios.

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
