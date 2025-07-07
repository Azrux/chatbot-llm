from flask import Blueprint, request, jsonify
from ai_chat_api.ai_agent.agent import agent_node, AgentState

ai_bp = Blueprint('ai_bp', __name__)


@ai_bp.route('/chat', methods=['POST'])
def ai_chat():
    data = request.get_json()
    user_msg = data.get('message')

    # crear el estado inicial
    state = AgentState(user_msg=user_msg)
    print(f"Mensaje del usuario: {user_msg}")
    print(f"Estado inicial: {state}")

    # correr el agente
    state = agent_node(state)

    print(f"Respuesta del agente: {state.agent_reply}")
    print(f"Revisión del supervisor: {state.supervisor_review}")
    print(f"Respuesta final: {state.final_response}")

    # guardar el historial de la conversación
    state.conversation_history.append({
        "role": "agent",
        "message": state.agent_reply
    })

    # construir respuesta JSON
    return jsonify({
        "answer": state.agent_reply,
        "review": state.supervisor_review,
        "final_response": state.final_response
    })
