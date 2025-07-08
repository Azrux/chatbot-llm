"""
Módulo que define el estado del agente durante la conversación.
"""
from dataclasses import dataclass, field
from typing import List, Optional


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
