"""DARTRIX-TIME v1.0 temporal primitives.

The module deliberately uses only the Python standard library and keeps all
external time input explicit, making calculations deterministic and easy to
test.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum


class TimePhase(str, Enum):
    """Coarse phase of a UTC day."""

    NIGHT = "night"
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"


@dataclass(frozen=True)
class DartrixTime:
    """An immutable UTC timestamp with DARTRIX phase metadata."""

    instant: datetime

    def __post_init__(self) -> None:
        if self.instant.tzinfo is None or self.instant.utcoffset() is None:
            raise ValueError("DARTRIX-TIME requires a timezone-aware datetime")
        object.__setattr__(self, "instant", self.instant.astimezone(timezone.utc))

    @classmethod
    def now(cls) -> "DartrixTime":
        return cls(datetime.now(timezone.utc))

    @classmethod
    def from_isoformat(cls, value: str) -> "DartrixTime":
        """Parse an ISO-8601 timestamp, accepting a trailing ``Z``."""
        return cls(datetime.fromisoformat(value.replace("Z", "+00:00")))

    @property
    def phase(self) -> TimePhase:
        hour = self.instant.hour
        if hour < 6:
            return TimePhase.NIGHT
        if hour < 12:
            return TimePhase.MORNING
        if hour < 18:
            return TimePhase.AFTERNOON
        if hour < 22:
            return TimePhase.EVENING
        return TimePhase.NIGHT

    def add(self, **delta: float) -> "DartrixTime":
        """Return a timestamp shifted by ``timedelta`` keyword arguments."""
        return DartrixTime(self.instant + timedelta(**delta))

    def seconds_until(self, other: "DartrixTime") -> float:
        return (other.instant - self.instant).total_seconds()

    def isoformat(self) -> str:
        return self.instant.isoformat().replace("+00:00", "Z")


__all__ = ["DartrixTime", "TimePhase"]
