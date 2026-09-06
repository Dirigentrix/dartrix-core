"""Deterministic 1,000-match DARTRIX matrix arena CLI."""
from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from typing import Dict, Sequence, Tuple

from dartrix_core.matrix6x6 import SystemQuantifier, solve_rose_matrix
from dartrix_core.wolf_guardian import GateDecision, WolfGuardian


FEATURE_MATRIX: Tuple[Tuple[float, ...], ...] = (
    (2.0, .2, 0, 0, 0, 0), (.1, 1.8, .2, 0, 0, 0),
    (0, .1, 1.7, .2, 0, 0), (0, 0, .1, 1.6, .2, 0),
    (0, 0, 0, .1, 1.5, .2), (.1, 0, 0, 0, .1, 1.9),
)
ACTIONS = ("press", "hold", "counter", "reset")


@dataclass(frozen=True)
class MatchResult:
    goals_for: int
    goals_against: int
    decisions: int
    blocked: int
    residual: float


def _state(rng: random.Random, minute: int) -> Tuple[float, ...]:
    return tuple(max(0.0, min(1.0, rng.random() * .8 + (minute / 90.0) * .2)) for _ in range(6))


def choose_action(weights: Sequence[float], guardian: WolfGuardian) -> Tuple[str, GateDecision]:
    """Select the lowest-energy action, then apply the WolfGuardian gate."""
    energies = {
        "press": abs(weights[0]) + abs(weights[3]) * .25,
        "hold": abs(weights[1]) + abs(weights[4]) * .20,
        "counter": abs(weights[2]) + abs(weights[5]) * .15,
        "reset": sum(abs(value) for value in weights) * .08,
    }
    action = min(ACTIONS, key=lambda item: energies[item])
    risk = min(1.0, energies[action] / (1.0 + sum(abs(value) for value in weights)))
    gate = guardian.evaluate(risk, confidence=1.0)
    if gate.decision != GateDecision.PASS:
        return "reset", gate.decision
    return action, gate.decision


def simulate_match(rng: random.Random) -> MatchResult:
    guardian = WolfGuardian()
    goals_for = goals_against = blocked = 0
    residual = 0.0
    for minute in range(90):
        state = _state(rng, minute)
        rhs = tuple(value * 1.5 for value in state)
        weights = solve_rose_matrix(FEATURE_MATRIX, rhs)
        report = SystemQuantifier.assess(FEATURE_MATRIX, rhs, weights)
        residual += report.max_residual
        _, decision = choose_action(weights, guardian)
        blocked += int(decision != GateDecision.PASS)
        chance = (sum(weights) / 6.0) * .018
        if rng.random() < max(0.0, min(.08, chance)):
            goals_for += 1
        if rng.random() < .012:
            goals_against += 1
    return MatchResult(goals_for, goals_against, 90, blocked, residual)


def run_arena(matches: int = 1000, seed: int = 108) -> Dict[str, float]:
    if matches < 1:
        raise ValueError("matches must be positive")
    rng = random.Random(seed)
    results = [simulate_match(rng) for _ in range(matches)]
    return {
        "matches": matches,
        "minutes": matches * 90,
        "goals_for": sum(item.goals_for for item in results),
        "goals_against": sum(item.goals_against for item in results),
        "decisions": sum(item.decisions for item in results),
        "blocked_decisions": sum(item.blocked for item in results),
        "mean_residual": sum(item.residual for item in results) / (matches * 90),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the DARTRIX 6x6 Rose Matrix soccer arena.")
    parser.add_argument("--matches", type=int, default=1000, help="number of 90-minute matches (default: 1000)")
    parser.add_argument("--seed", type=int, default=108, help="deterministic simulation seed")
    args = parser.parse_args()
    report = run_arena(args.matches, args.seed)
    print("DARTRIX ARENA REPORT")
    print(f"matches: {int(report['matches'])}")
    print(f"simulated_minutes: {int(report['minutes'])}")
    print(f"goals_for: {int(report['goals_for'])}")
    print(f"goals_against: {int(report['goals_against'])}")
    print(f"matrix_decisions: {int(report['decisions'])}")
    print(f"wolfguardian_blocked_decisions: {int(report['blocked_decisions'])}")
    print(f"mean_system_residual: {report['mean_residual']:.3e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
