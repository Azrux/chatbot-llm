"""
Módulo para manejar la solicitud de propuesta de valor de Kavak.
"""
from ai_chat_api.ai_agent.state import AgentState
from ai_chat_api.routes.scrape_kavak_site import kavak_rag


def handle_value_proposition(state: AgentState, params: dict) -> AgentState:
    """
    Maneja la solicitud de propuesta de valor para el usuario.
    Esta función utiliza el sistema de Recuperación y Generación (RAG) para responder a
    la pregunta del usuario sobre la propuesta de valor de Kavak.
    """
    # Usar RAG para responder la pregunta del usuario
    rag_result = kavak_rag.answer_question(state.user_msg)

    if isinstance(rag_result, dict):
        state.agent_reply = rag_result.get(
            "answer",
            "Lo siento, no pude encontrar información específica sobre eso. ¿Puedo ayudarte con algo más?"
        )
    else:
        state.agent_reply = "Lo siento, no pude encontrar información específica sobre eso. ¿Puedo ayudarte con algo más?"

    return state
