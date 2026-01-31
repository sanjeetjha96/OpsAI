from .base_agent import AgentBase
from typing import Dict, Any


class IntentAgent(AgentBase):
    name = "intent"

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Detect intent, urgency, and SLA risk.

        This is a stub. Replace with classification logic or model invocation.
        """
        raise NotImplementedError("IntentAgent.run is not implemented yet")
