from .base_agent import AgentBase
from typing import Dict, Any


class RetrievalAgent(AgentBase):
    name = "retrieval"

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Perform retrieval (RAG) and return top-k chunks with provenance.

        This is a scaffold and should call into `tools.rag_tool` or a real
        retriever in production.
        """
        raise NotImplementedError("RetrievalAgent.run is not implemented yet")
