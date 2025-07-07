from dataclasses import asdict
from flask import Blueprint, request
from ai_chat_api.ai_agent.agent import agent_node, AgentState
from ai_chat_api.routes.db_routes.state import get_state, save_state

twilio_bp = Blueprint('twilio', __name__)


@twilio_bp.route('/webhook', methods=['POST'])  # Twilio usa webhook
def webhook():
    # Twilio envía los datos como form data, no JSON
    user_msg = request.form.get('Body')  # El mensaje del usuario
    print(f"Mensaje recibido: {user_msg}")
    # El número del usuario (ej: whatsapp:+5491123456789)
    from_number = request.form.get('From')

    # Limpiar el número (quitar "whatsapp:" si está presente)
    phone_number = from_number.replace("whatsapp:", "")

    print(f"Mensaje de {phone_number}: {user_msg}")

    # Cargar estado existente o crear uno nuevo
    state = get_state(phone_number)
    if state is None:
        state = AgentState(user_msg=user_msg)
        print(f"Nueva conversación iniciada para {phone_number}")
    else:
        state.user_msg = user_msg
        print(
            f"Conversación existente: {len(state.conversation_history)} mensajes previos")

    # Correr el agente
    state = agent_node(state)

    print(asdict(state))

    # Actualizar el historial de conversación
    state.conversation_history.append({
        "role": "user",
        "message": state.user_msg
    })

    # Guardar el estado actualizado
    save_state(phone_number, state)

    # Responder a Twilio (formato TwiML)
    from twilio.twiml.messaging_response import MessagingResponse

    response = MessagingResponse()
    response.message(state.final_response)

    return str(response)
