import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Carga las variables de entorno necesarias para la conexión a servicios externos
    """
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    CSV_PATH = os.environ.get('CSV_PATH', '../sample_caso_ai_engineer.csv')
