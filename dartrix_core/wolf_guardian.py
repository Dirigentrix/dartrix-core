"""Deterministic safety gate with thresholds, confidence, and hysteresis."""
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class GateDecision(str, Enum):
    PASS = "pass"
    SOFT_BLOCK = "soft_block"
    HARD_BLOCK = "hard_block"

@dataclass(frozen=True)
class GateResult:
    decision: GateDecision
    s_non: float
    confidence: float
    reason: str = ""

class WolfGuardian:
    def __init__(self, soft_threshold: float = 0.45, hard_threshold: float = 0.80, hysteresis: float = 0.05):
        if not 0 <= soft_threshold <= hard_threshold <= 1: raise ValueError("thresholds must satisfy 0 <= soft <= hard <= 1")
        if hysteresis < 0: raise ValueError("hysteresis must be non-negative")
        self.soft_threshold, self.hard_threshold, self.hysteresis = soft_threshold, hard_threshold, hysteresis
        self._last_decision = GateDecision.PASS

    def evaluate(self, s_non: float, confidence: float = 1.0, reason: str = "") -> GateResult:
        s_non = max(0.0, min(1.0, float(s_non))); confidence = max(0.0, min(1.0, float(confidence)))
        soft, hard = self.soft_threshold, self.hard_threshold
        if self._last_decision == GateDecision.HARD_BLOCK: hard -= self.hysteresis
        elif self._last_decision == GateDecision.SOFT_BLOCK: soft -= self.hysteresis
        if s_non >= hard: decision = GateDecision.HARD_BLOCK
        elif s_non >= soft: decision = GateDecision.SOFT_BLOCK
        else: decision = GateDecision.PASS
        self._last_decision = decision
        return GateResult(decision, s_non, confidence, reason)
