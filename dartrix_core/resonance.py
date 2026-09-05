"""108 Hz resonance transform and state enrichment."""
from dataclasses import replace
from .types import State

class Resonance108:
    """Apply the DARTRIX core resonance without changing user content."""
    frequency_hz = 108.0

    def enrich(self, state: State) -> State:
        metadata = dict(state.metadata)
        metadata.update({"resonance": "108 Hz", "resonance_applied": True})
        return replace(state, resonance_hz=self.frequency_hz, metadata=metadata)

    def transform(self, text: str) -> str:
        return text.strip()
