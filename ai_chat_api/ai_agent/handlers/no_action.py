"""
Módulo para manejar la situación en la que el usuario no ha realizado una acción específica.

"""
from langchain_core.messages import HumanMessage
from ai_chat_api.ai_agent.state import AgentState
from ai_chat_api.ai_agent.agents import gpt_turbo


def handle_no_action(state: AgentState, params: dict) -> AgentState:
    """
    Maneja la situación en la que el usuario no ha realizado una acción específica,
    """
    last_6_messages = state.conversation_history[-6:]

    prompt = f"""
        Eres un asistente virtual de una empresa de autos. Analiza el siguiente mensaje del usuario:

        "{state.user_msg}"

        INSTRUCCIONES ESTRICTAS:
        - Si el mensaje es solo un saludo, responde con un saludo cordial y pregunta cómo puedes ayudar.
        - Si el mensaje es una despedida, despídete cordialmente.
          - Si en el historial de conversación ya hubo una despedida, NO respondas.
        - Si el mensaje no es un saludo o despedida y NO está relacionado con autos, financiamiento o la empresa, NO respondas la pregunta. SOLO di: "Lo siento, solo puedo ayudarte con temas de autos, financiamiento o información de la empresa."

        NO respondas preguntas fuera de tu dominio. NO intentes ser útil fuera de los temas indicados. NO expliques, NO resuelvas, NO des información adicional.

        Últimos 6 mensajes de la conversación: {last_6_messages}

        Responde solo en español, de manera breve, cordial y profesional.
        """
    completion = gpt_turbo.invoke([HumanMessage(content=prompt)])
    state.agent_reply = completion.content  # type: ignore
    return state
