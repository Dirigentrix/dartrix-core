"""AladdinLamp operator pipeline: Touch, Whisper, Resonance, Djinn."""
from .resonance import Resonance108
from .types import Intent, State
from .wolf_guardian import GateDecision, WolfGuardian, GateResult

class AladdinLamp:
    def __init__(self, guardian=None, resonance=None):
        self.guardian = guardian or WolfGuardian()
        self.resonance = resonance or Resonance108()

    def touch(self, text: str, intent: Intent = Intent.OTHER) -> State:
        return State(input_text=text, intent=intent)

    def whisper(self, state: State) -> State:
        state.metadata["whispered"] = True
        state.confidence = max(state.confidence, 0.5)
        return state

    def apply_resonance(self, state: State) -> State:
        return self.resonance.enrich(state)

    def djinn(self, state: State, s_non: float = 0.0, confidence: float = 1.0) -> tuple[str, GateResult]:
        gate = self.guardian.evaluate(s_non, confidence)
        if gate.decision == GateDecision.HARD_BLOCK: return ("Request blocked by WolfGuardian.", gate)
        if gate.decision == GateDecision.SOFT_BLOCK: return ("Request requires a safer reformulation.", gate)
        return (self.resonance.transform(state.input_text), gate)

    def operate(self, text: str, intent: Intent = Intent.OTHER, s_non: float = 0.0, confidence: float = 1.0):
        state = self.apply_resonance(self.whisper(self.touch(text, intent)))
        return self.djinn(state, s_non, confidence)
