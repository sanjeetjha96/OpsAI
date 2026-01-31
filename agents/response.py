from .base_agent import AgentBase
from typing import Dict, Any


class ResponseAgent(AgentBase):
    name = "response"

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize human-readable responses and include citations.

        The real implementation should reference retrieved chunks and provide
        provenance in the returned result.
        """
        raise NotImplementedError("ResponseAgent.run is not implemented yet")
