from .base_agent import AgentBase
from typing import Dict, Any


class MemoryAgent(AgentBase):
    name = "memory"

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Read/write episodic and semantic memory.

        Implementations should persist memories and support queries and deletions.
        """
        raise NotImplementedError("MemoryAgent.run is not implemented yet")
