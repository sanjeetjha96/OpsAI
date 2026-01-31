from .base_agent import AgentBase
from typing import Dict, Any


class IngestionAgent(AgentBase):
    name = "ingestion"

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize incoming tickets/alerts and extract metadata.

        This is a scaffolded implementation — replace with real parsing logic.
        """
        # minimal interface — real impl should parse payload and return structured data
        raise NotImplementedError("IngestionAgent.run is not implemented yet")
