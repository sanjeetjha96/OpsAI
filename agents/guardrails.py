from .base_agent import AgentBase
from typing import Dict, Any


class GuardrailsAgent(AgentBase):
    name = "guardrails"

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Apply safety policies, confidence thresholds and decide escalation.

        Keep a declarative blocklist separate from code for easy updates.
        """
        raise NotImplementedError("GuardrailsAgent.run is not implemented yet")
