"""
Rutas para manejar la integración con Twilio y WhatsApp.
"""
import os
from dataclasses import asdict
from twilio.rest import Client
from flask import Blueprint, request
from ai_chat_api.ai_agent.agent_node import agent_node
from ai_chat_api.ai_agent.state import AgentState
from ai_chat_api.routes.db_routes.state import get_state, save_state

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)

twilio_bp = Blueprint('twilio', __name__)


def send_twilio_message(to, body):
    """
    Enviar un mensaje a través de Twilio.
    """
    message = client.messages.create(
        from_='whatsapp:+14155238886',  # Número de WhatsApp de Twilio
        body=body,
        to='whatsapp:' + to
    )
    print(f"Mensaje enviado: {message.sid}")
    return message.sid


@twilio_bp.route('/webhook', methods=['POST'])  # Twilio usa webhook
def webhook():
    """
    Maneja los mensajes entrantes de Twilio y procesa la conversación.
    """
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

    # Actualizar el historial de conversación
    state.conversation_history.append({
        "role": "user",
        "message": state.user_msg
    })

    # Guardar el estado actualizado
    save_state(phone_number, state)

    # Responder a Twilio
    send_twilio_message(phone_number, state.agent_reply)

    return state.agent_reply
