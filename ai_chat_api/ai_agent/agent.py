from dataclasses import dataclass, field
from typing import Optional, List
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from ai_chat_api.ai_agent.tools import get_cars, get_financing
from ai_chat_api.ai_agent.intent_agent import classify_user_input
from ai_chat_api.routes.scrape_kavak_site import kavak_rag

# Modelo LLM principal
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

# === State de LangGraph ===
# Será el "contexto" que viaja entre nodos


@dataclass
class AgentState:
    """
    Clase que representa el estado del agente durante la conversación.
    """
    user_msg: str
    agent_reply: Optional[str] = None
    final_response: Optional[str] = None
    price: Optional[float] = None
    cars_found: Optional[List[dict]] = field(default_factory=list)
    selected_car: Optional[dict] = None
    financing_options: Optional[List[dict]] = field(default_factory=list)
    conversation_history: List[dict] = field(default_factory=list)

# === NODO: Agent Node ===


def agent_node(state: AgentState) -> AgentState:
    """
    Nodo principal del agente que procesa el mensaje del usuario,
    clasifica intenciones, busca autos y financiamiento, y genera respuestas.
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

    last_6_messages = state.conversation_history[-6:]

    for item in intents:
        intent = item.get("intent")
        params = item.get("parameters", {})

        if intent == "search_cars":
            cars_response = get_cars(params)
            car_list = cars_response.get("cars", [])

            state.cars_found = car_list

            if not car_list:
                state.agent_reply = "No encontré autos con esos datos. Te interesa algún otro modelo?"
                break

            if len(car_list) == 1:
                # Si hay solo uno se selecciona automáticamente
                car = car_list[0]
                state.selected_car = car
                state.agent_reply = (
                    f"Encontré un auto que coincide: "
                    f"{car['year']} {car['make']} {car['model']} a ${car['price']}.\n"
                    f"¿Quieres conocer opciones de financiamiento?"
                )
            else:
                # Si hay varios se muestra una lista
                cars_text = "\n".join(
                    f"- ID {c['stock_id']}: {c['year']} {c['make']} {c['model']} ${c['price']}"
                    for c in car_list
                )
                state.agent_reply = (
                    "Encontré varios autos que coinciden:\n"
                    f"{cars_text}\n"
                    "¿Te interesa alguno?"
                )
            continue

        elif intent == "select_car":
            stock_id = params.get("stock_id")
            car = next(
                (c for c in state.cars_found if str(
                    c["stock_id"]) == str(stock_id)),
                None
            )
            if not car:
                state.agent_reply = "No pude encontrar ese auto. ¿Podrías darme más detalles?"
                break

            state.selected_car = car
            state.agent_reply = (
                f"Seleccionaste el {car['year']} {car['make']} {car['model']} "
                f"de ${car['price']}. ¿Quieres saber opciones de financiamiento?"
            )
            continue

        elif intent == "more_info":
            # Buscar si ya hay un auto seleccionado
            car = state.selected_car
            if not car:
                # Buscar en cars_found si hay parámetros de make/model
                make = params.get("make")
                model = params.get("model")

                if not make or not model:
                    state.agent_reply = (
                        "No encontré el auto del que quieres más información. "
                        "¿Podrías decirme al menos la marca y el modelo?"
                    )
                    break

                car = next(
                    (c for c in state.cars_found
                     if make.lower() in c["make"].lower() and model.lower() in c["model"].lower()),
                    None
                )
                if not car:
                    state.agent_reply = (
                        "No encontré el auto del que quieres más información. "
                        "¿Podrías decirme la marca y modelo?"
                    )
                    break

                state.selected_car = car

            prompt = f"""
                El usuario preguntó:
                {state.user_msg}

                Auto seleccionado:
                {car}

                Redacta un mensaje breve, cordial, para darle más información sobre este auto.
                El mensaje debe ser claro y directo, evitando tecnicismos innecesarios.

                Responde en relación a los últimos mensajes intercambiados con el usuario.

                Últimos 6 mensajes de la conversación: {last_6_messages}

                Debes asegurarte de que las respuestas sean:
                    - Coherentes y relevantes para la pregunta del usuario
                    - Apropiadas para el contexto de venta de autos
                    - Profesionales y útiles

                Las respuestas deben responder directamente a la pregunta sin información irrelevante.

                Asegúrate de que la respuesta tenga sentido en el contexto de la conversación y que no contenga errores o información confusa.
            """
            completion = llm.invoke([HumanMessage(content=prompt)])
            state.agent_reply = completion.content
            continue

        elif intent == "search_financing":
            # Buscar si ya hay un auto seleccionado
            car = state.selected_car
            if not car:
                # Buscar en cars_found si hay parámetros de make/model
                make = params.get("make")
                model = params.get("model")
                if not make or not model:
                    state.agent_reply = (
                        "No encontré el auto del que quieres financiamiento. "
                        "¿Podrías decirme la marca y modelo?"
                    )
                    break

                car = next(
                    (c for c in state.cars_found
                     if make.lower() in c["make"].lower() and model.lower() in c["model"].lower()),
                    None
                )
                if not car:
                    state.agent_reply = (
                        "No encontré el auto del que quieres financiamiento. "
                        "¿Podrías decirme la marca y modelo?"
                    )
                    break

                state.selected_car = car

            price = car["price"]
            years = params.get("years")

            financing = get_financing(price, years)
            state.financing_options = financing

            if not financing:
                state.agent_reply = "No encontré opciones de financiamiento. ¿Quieres saber sobre otros modelos?"
                break

            prompt = f"""
                El usuario preguntó:
                {state.user_msg}

                Auto seleccionado:
                {car}

                Opciones de financiación:
                {financing}

                Redacta un mensaje breve, cordial, en español para presentarle estas opciones.
                El mensaje debe ser claro y directo, evitando tecnicismos innecesarios y explicándole al usuario cómo funcionan las cuotas y tasas de interés.
                No incluyas información irrelevante o detalles técnicos complejos.

                Responde en relación a los últimos mensajes intercambiados con el usuario.

                Últimos 6 mensajes de la conversación: {last_6_messages}

                Debes asegurarte de que las respuestas sean:
                    - Coherentes y relevantes para la pregunta del usuario
                    - Apropiadas para el contexto de venta de autos
                    - Profesionales y útiles

                Las respuestas deben responder directamente a la pregunta sin información irrelevante.

                Asegúrate de que la respuesta tenga sentido en el contexto de la conversación y que no contenga errores o información confusa.
            """
            completion = llm.invoke([HumanMessage(content=prompt)])
            state.agent_reply = completion.content
            continue

        elif intent == "value_proposition":

            # Usar RAG para responder
            rag_result = kavak_rag.answer_question(state.user_msg)

            if isinstance(rag_result, dict):
                state.agent_reply = rag_result["answer"]
            else:
                state.agent_reply = "Lo siento, no pude encontrar información específica sobre eso. ¿Puedo ayudarte con algo más?"
            continue

        elif intent == "no_action":
            prompt = f"""
                El usuario preguntó:
                {state.user_msg}
                Redacta un mensaje breve, cordial, en español para responder a esta consulta que no está relacionada con autos, financiamiento o la empresa.
                
                El mensaje debe dejar en claro que no puedes ayudarlo con esa consulta específica, pero que estás disponible para cualquier otra pregunta relacionada con autos, financiamiento o la empresa.
                
                Si el mensaje es un saludo del usuario, responde con un saludo cordial y muéstrate disponible para ayudar.

                Responde en relación a los últimos mensajes intercambiados con el usuario.
                Últimos 6 mensajes de la conversación: {last_6_messages}
            """
            completion = llm.invoke([HumanMessage(content=prompt)])
            state.agent_reply = completion.content

            continue

        else:
            state.agent_reply = "No logré entender tu consulta. ¿Podrías darme más detalles?"
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
