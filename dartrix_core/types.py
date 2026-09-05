"""Shared types for DARTRIX Core."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional

class Intent(str, Enum):
    TRANSFORM = "transform"
    SUPPORT = "support"
    KNOWLEDGE = "knowledge"
    CREATIVE = "creative"
    REFLECT = "reflect"
    OTHER = "other"

@dataclass
class State:
    input_text: str
    intent: Intent = Intent.OTHER
    resonance_hz: float = 108.0
    s_non: float = 0.0
    confidence: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    output: Optional[str] = None
