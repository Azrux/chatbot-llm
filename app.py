from dotenv import load_dotenv
from flask import Flask
from ai_chat_api.config import Config
from ai_chat_api.routes.ai_routes import ai_bp
from ai_chat_api.routes.db_routes.car import db_bp
from ai_chat_api.routes.business_routes import business_bp
from ai_chat_api.routes.twilio_routes import twilio_bp

load_dotenv()


def create_app():
    """Factory function para crear la aplicación Flask"""
    app = Flask("AI Chat API")

    # Cargar configuración
    app.config.from_object(Config)

    # Registrar blueprints (rutas organizadas)
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(db_bp, url_prefix='/api/db')
    app.register_blueprint(business_bp, url_prefix='/api/business')
    app.register_blueprint(twilio_bp, url_prefix='/api/twilio')

    # Ruta básica de salud del servidor
    @app.route('/health')
    def health_check():
        return {'status': 'OK', 'message': 'Server is running'}

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
