import abc
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class AgentBase(abc.ABC):
    """Abstract base class for all agents.

    Concrete agents should implement `run` which accepts an input dict and
    returns a dict result. Raising NotImplementedError is fine for stubs.
    """

    name: str = "base"

    def __init__(self, config: Dict[str, Any] | None = None):
        self.config = config or {}

    @abc.abstractmethod
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Run the agent on the provided payload.

        Args:
            payload: a dictionary representing the agent input.

        Returns:
            A dictionary result.
        """
        raise NotImplementedError()
