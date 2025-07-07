import json
from dataclasses import dataclass, field
from typing import Optional, List
from langgraph.graph import END
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from ai_chat_api.ai_agent.tools import get_cars, get_financing
from ai_chat_api.ai_agent.intent_agent import classify_user_input


# Modelo LLM principal
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

# === State de LangGraph ===
# Será el "contexto" que viaja entre nodos


@dataclass
class AgentState:
    user_msg: str
    agent_reply: Optional[str] = None
    supervisor_review: Optional[str] = None
    final_response: Optional[str] = None
    price: Optional[float] = None
    cars_found: Optional[List[dict]] = field(default_factory=list)
    selected_car: Optional[dict] = None
    financing_options: Optional[List[dict]] = field(default_factory=list)
    conversation_history: List[dict] = field(default_factory=list)

# === NODO: Agent Node ===


def agent_node(state: AgentState) -> AgentState:
    intents = classify_user_input(state.user_msg, state)
    print(f"Intenciones clasificadas: {intents}")

    if isinstance(intents, dict):
        intents = [intents]

    # Guardar en el historial de conversación
    state.conversation_history.append({
        "role": "intent_agent",
        "intents": intents
    })

    for item in intents:
        intent = item.get("intent")
        params = item.get("parameters", {})

        if intent == "search_cars":
            cars_response = get_cars(params)
            car_list = cars_response.get("cars", [])

            state.cars_found = car_list

            if not car_list:
                state.agent_reply = "No encontré autos con esos datos."
                state.conversation_history.append({
                    "role": "agent",
                    "message": state.agent_reply
                })
                return state

            if len(car_list) == 1:
                # Si hay 1 solo → lo seleccionamos automáticamente
                car = car_list[0]
                state.selected_car = car
                state.agent_reply = (
                    f"Encontré un auto que coincide: "
                    f"{car['year']} {car['make']} {car['model']} a ${car['price']}.\n"
                    f"¿Quieres conocer opciones de financiamiento?"
                )
            else:
                # Múltiples autos → mostrar lista
                cars_text = "\n".join(
                    f"- ID {c['stock_id']}: {c['year']} {c['make']} {c['model']} ${c['price']}"
                    for c in car_list
                )
                state.agent_reply = (
                    "Encontré varios autos que coinciden:\n"
                    f"{cars_text}\n"
                    "¿Cuál te interesa?"
                )
            # seguimos procesando otros intents
            continue

        elif intent == "select_car":
            car_id = params.get("car_id")
            car = next(
                (c for c in state.cars_found if str(
                    c["stock_id"]) == str(car_id)),
                None
            )
            if not car:
                state.agent_reply = f"No encontré el auto con ID {car_id}."
                state.conversation_history.append({
                    "role": "agent",
                    "message": state.agent_reply
                })
                return state

            state.selected_car = car
            state.agent_reply = (
                f"Seleccionaste el {car['year']} {car['make']} {car['model']} "
                f"de ${car['price']}. ¿Quieres saber opciones de financiamiento?"
            )
            continue

        elif intent == "search_financing":
            # Buscamos el auto seleccionado
            car = state.selected_car
            if not car:
                # Buscar en cars_found si hay parámetros de make/model
                make = params.get("make")
                model = params.get("model")
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
                    state.conversation_history.append({
                        "role": "agent",
                        "message": state.agent_reply
                    })
                    return state

                state.selected_car = car

            price = car["price"]
            years = params.get("years")

            financing = get_financing(price, years)

            state.financing_options = financing

            if not financing:
                state.agent_reply = "No encontré opciones de financiamiento."
                state.conversation_history.append({
                    "role": "agent",
                    "message": state.agent_reply
                })
                return state

            prompt = f"""
                El usuario preguntó:
                {state.user_msg}

                Auto seleccionado:
                {car}

                Opciones de financiación:
                {financing}

                Redacta un mensaje breve, cordial, en español para presentarle estas opciones.
            """
            completion = llm.invoke([HumanMessage(content=prompt)])
            state.agent_reply = completion.content
            continue

        elif intent == "no_action":
            state.agent_reply = "¡Gracias por tu mensaje! ¿En qué puedo ayudarte?"
            continue

        else:
            state.agent_reply = "No logré entender tu consulta. ¿Podrías darme más detalles?"
            state.conversation_history.append({
                "role": "agent",
                "message": state.agent_reply
            })
            return state

    state.conversation_history.append({
        "role": "agent",
        "message": state.agent_reply
    })

    return state
