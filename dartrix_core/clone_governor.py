"""Deterministic Clone Robotics governor using the Module 24627 filter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


WEIGHTS = np.array([2, 4, 6, 2, 7], dtype=float)
TELEMETRY_NAMES = (
    "T_wody",
    "p_ukladu",
    "zawory_aktywne",
    "blad_pozycji",
    "przeplyw_lpm",
)


@dataclass(frozen=True)
class GovernorDecision:
    """The deterministic operating decision for one telemetry vector."""

    score: float
    mode: str
    throughput_factor: float
    passive_cooling: bool
    hold_trajectory: bool
    grip_stabilization: bool
    emergency_pump_cutoff: bool
    pressure_dump: bool


class DARTRIXCloneGovernor:
    """Classify normalized clone telemetry with the Module 24627 weighted sum.

    Input order is [T_wody, p_ukladu, zawory_aktywne, blad_pozycji,
    przeplyw_lpm]. Every value must be finite and normalized to [0, 1].
    """

    def __init__(self, weights: Sequence[float] = WEIGHTS) -> None:
        weights_array = np.asarray(weights, dtype=float)
        if weights_array.shape != (5,) or not np.all(np.isfinite(weights_array)):
            raise ValueError("weights must contain exactly five finite values")
        self.weights = weights_array.copy()

    def evaluate(self, telemetry: Sequence[float]) -> GovernorDecision:
        vector = np.asarray(telemetry, dtype=float)
        if vector.shape != (5,):
            raise ValueError("telemetry must contain five normalized values")
        if not np.all(np.isfinite(vector)) or np.any((vector < 0.0) | (vector > 1.0)):
            raise ValueError("telemetry values must be finite and in the range [0, 1]")

        score = float(np.dot(vector, self.weights))
        if score < 3.0:
            return GovernorDecision(score, "HARMONIA", 1.0, False, False, False, False, False)
        if score < 6.0:
            return GovernorDecision(score, "STRUKTURA", 0.7, True, False, False, False, False)
        if score < 9.0:
            return GovernorDecision(score, "INTEGRACJA", 1.0, False, True, True, False, False)
        return GovernorDecision(score, "EMERGENCY / KOSA", 0.0, False, False, False, True, True)

    def decide(self, telemetry: Sequence[float]) -> GovernorDecision:
        """Alias for evaluate, retained as a concise control-loop interface."""
        return self.evaluate(telemetry)
