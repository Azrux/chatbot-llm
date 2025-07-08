import json
import os
from typing import Optional
from ai_chat_api.ai_agent.state import AgentState


def get_state(phone_number: str) -> Optional[AgentState]:
    clean_phone = phone_number.replace(
        "+", "").replace("-", "").replace(" ", "")
    filename = f"sessions/state_{clean_phone}.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
            # Creamos el AgentState usando los datos del JSON
            state = AgentState(
                user_msg=data.get("user_msg", ""),
                agent_reply=data.get("agent_reply"),
                final_response=data.get("final_response"),
                price=data.get("price"),
                cars_found=data.get("cars_found", []),
                selected_car=data.get("selected_car"),
                financing_options=data.get("financing_options", []),
                conversation_history=data.get("conversation_history", [])
            )
            return state
    else:
        os.makedirs("sessions", exist_ok=True)
        return None


def save_state(phone_number, state):
    from dataclasses import asdict
    clean_phone = phone_number.replace(
        "+", "").replace("-", "").replace(" ", "")
    filename = f"sessions/state_{clean_phone}.json"
    with open(filename, "w") as f:
        json.dump(asdict(state), f, indent=2)
