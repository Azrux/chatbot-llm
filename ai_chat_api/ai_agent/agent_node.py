"""
Módulo principal del agente de IA.
Procesa las intenciones del usuario y delega a los handlers correspondientes.
"""
from ai_chat_api.ai_agent.handlers.more_info import handle_more_info
from ai_chat_api.ai_agent.handlers.no_action import handle_no_action
from ai_chat_api.ai_agent.handlers.search_cars import handle_search_cars
from ai_chat_api.ai_agent.handlers.search_financing import handle_search_financing
from ai_chat_api.ai_agent.handlers.select_car import handle_select_car
from ai_chat_api.ai_agent.handlers.value_proposition import handle_value_proposition
from ai_chat_api.ai_agent.intent_agent import classify_user_input
from ai_chat_api.ai_agent.state import AgentState


# Handler para intents desconocidos
def handle_unknown_intent(state: AgentState) -> AgentState:
    """
    Maneja situaciones donde la intención del usuario no es reconocida.
    """
    state.agent_reply = "No logré entender tu consulta. ¿Podrías darme más detalles?"
    return state


# Dispatcher de intents
INTENT_HANDLERS = {
    "search_cars": handle_search_cars,
    "select_car": handle_select_car,
    "more_info": handle_more_info,
    "search_financing": handle_search_financing,
    "value_proposition": handle_value_proposition,
    "no_action": handle_no_action,
}


def agent_node(state: AgentState) -> AgentState:
    """
    Nodo principal del agente que procesa el mensaje del usuario,
    clasifica intenciones, delega a los handlers y actualiza el estado.
    """
    intents = classify_user_input(state.user_msg, state)
    print(f"Intenciones clasificadas: {intents}")

    if isinstance(intents, dict):
        intents = [intents]

    # Guardar en el historial de conversación
    state.conversation_history.append({
        "role": "intent_agent",
        "intents": intents
    })

    for item in intents:
        intent = item.get("intent")
        params = item.get("parameters", {})
        handler = INTENT_HANDLERS.get(
            intent, handle_unknown_intent)  # type: ignore
        state = handler(state, params)

        # Si el handler ya generó una respuesta, no seguimos procesando más intents
        if state.agent_reply:
            break

    # Si no hay respuesta del agente, asignar una por defecto
    if not state.agent_reply:
        state.agent_reply = "¡Hola! ¿En qué puedo ayudarte?"

    # Guardar la respuesta del agente en el historial
    state.conversation_history.append({
        "role": "agent",
        "message": state.agent_reply
    })

    return state
