"""
Context Hacking Protocol (CHP)
A 9-layer anti-drift framework for trustworthy LLM-assisted scientific code generation.
"""

from context_hacking.core.gates import GateChecker
from context_hacking.core.memory import MemoryManager
from context_hacking.core.modes import ModeManager
from context_hacking.core.orchestrator import Orchestrator

__version__ = "0.1.0"
__all__ = ["Orchestrator", "GateChecker", "ModeManager", "MemoryManager"]
