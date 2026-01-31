import logging
from typing import Dict, Any

from .base_agent import AgentBase

logger = logging.getLogger(__name__)


class PlannerAgent(AgentBase):
    name = "planner"

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Decide execution strategy and delegate to other agents.

        This demo runner simulates orchestration by listing the planned steps.
        A full implementation should use Google ADK primitives to create and
        delegate tasks to other agents (parallel/serial/async).
        """
        plan = {
            "strategy": "serial",
            "steps": [
                "ingestion",
                "intent",
                "retrieval",
                "memory",
                "reasoning",
                "response",
                "guardrails",
            ],
        }
        logger.info("Planned steps: %s", plan["steps"])
        return {"plan": plan}

    def run_demo(self) -> None:
        """A tiny demo runner that prints the plan.

        This avoids requiring Google ADK during initial development.
        """
        result = self.run({})
        logger.info("Demo plan: %s", result)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    p = PlannerAgent()
    p.run_demo()
