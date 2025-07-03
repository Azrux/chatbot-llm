from flask import Blueprint, request, jsonify

ai_bp = Blueprint('ai', __name__)


@ai_bp.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint de ejemplo para chatear con la IA.
    Espera: {"message": "Hola"}
    Devuelve: {"response": "¡Hola! Soy la IA."}
    """
    data = request.get_json()
    user_message = data.get('message', '')

    return jsonify({
        'response': f'Recibí tu mensaje: "{user_message}". ¡Hola! Soy la IA.',
        'status': 'success'
    })
