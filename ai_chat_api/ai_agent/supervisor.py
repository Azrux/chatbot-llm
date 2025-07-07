from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


def review_response(question: str, answer: str) -> str:
    """
    LLM revisa si la respuesta es coherente.
    """
    prompt = f"""
Pregunta del usuario: {question}

Respuesta generada: {answer}

¿Es esta respuesta correcta y coherente?
Responde únicamente "Sí" o "No" y explica brevemente por qué.
"""

    completion = llm.invoke([HumanMessage(content=prompt)])
    return str(getattr(completion, "content", completion))
