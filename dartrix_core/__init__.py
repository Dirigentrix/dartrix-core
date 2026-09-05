"""DARTRIX Core: deterministic operators for resonant, safe transformations."""
from .types import Intent, State
from .resonance import Resonance108
from .wolf_guardian import GateDecision, GateResult, WolfGuardian
from .lamp import AladdinLamp

__version__ = "0.1.0"
__all__ = ["Intent", "State", "Resonance108", "GateDecision", "GateResult", "WolfGuardian", "AladdinLamp"]
