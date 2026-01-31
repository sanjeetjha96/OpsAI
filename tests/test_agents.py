import pytest

from agents.base_agent import AgentBase


def test_agent_base_abstract():
    # Ensure AgentBase is abstract and cannot be instantiated directly
    with pytest.raises(TypeError):
        AgentBase()
