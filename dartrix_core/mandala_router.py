from dataclasses import dataclass, replace
from enum import IntEnum
from typing import Any, Callable, Dict, List, Tuple

import numpy as np


class MandalaRing(IntEnum):
    RING_0_CORE = 0         # Centrum / dyspozytor nadrzędny
    RING_1_SECURITY = 1     # Walidacja limitów i integralności
    RING_2_SYMMETRY = 2     # Węzły symetrii obliczeniowej
    RING_3_INTERFACE = 3    # Bramy wejściowe i telemetria


@dataclass(frozen=True)
class MandalaPacket:
    source_ring: MandalaRing
    payload: np.ndarray
    intent: str = "TELEMETRY"
    routed_nodes: Tuple[int, ...] = ()


class MandalaRouter:
    """
    Topologia Mandali jako wielopierścieniowy router zdarzeń DARTRIX.
    Centrum (Ring 0) zarządza wagami i bezpieczeństwem.
    Symetria definiuje równomierne rozproszenie strumienia w Ring 2.
    """

    def __init__(self, symmetry: int = 8):
        if symmetry <= 0:
            raise ValueError("symmetry musi być dodatnie")
        self.symmetry = symmetry
        self.weights = np.array([2, 4, 6, 2, 7], dtype=float)
        self.subscribers: Dict[MandalaRing, List[Callable[[MandalaPacket], Any]]] = {
            ring: [] for ring in MandalaRing
        }

    def register(self, ring: MandalaRing, handler: Callable[[MandalaPacket], Any]) -> None:
        self.subscribers[ring].append(handler)

    def _dispatch(self, ring: MandalaRing, packet: MandalaPacket) -> None:
        for handler in self.subscribers[ring]:
            handler(packet)

    def route(self, packet: MandalaPacket) -> Dict[str, Any]:
        # Ring 1: Walidacja integralności wektora
        payload = np.asarray(packet.payload, dtype=float)
        if payload.shape != (5,):
            raise ValueError(f"Wymagany wektor 5-elementowy, otrzymano {payload.shape}")
        if not np.all(np.isfinite(payload)):
            raise ValueError("Wektor telemetrii musi zawierać wyłącznie wartości skończone")
        if not np.all((payload >= 0.0) & (payload <= 1.0)):
            raise ValueError("Wektor telemetrii musi być znormalizowany do przedziału [0, 1]")

        # Ring 2: Deterministyczne przypisanie do węzła symetrii
        node_id = int(np.sum(payload * 100)) % self.symmetry
        routed_packet = replace(
            packet,
            payload=payload.copy(),
            routed_nodes=packet.routed_nodes + (node_id,),
        )

        # Ring 0: Filtracja przez wagi 24627
        score = float(np.dot(payload, self.weights))
        if score < 3.0:
            state = "HARMONIA"
        elif score < 6.0:
            state = "STRUKTURA"
        elif score < 9.0:
            state = "INTEGRACJA"
        else:
            state = "KOSA"

        # Ring 0 always receives the validated decision. Non-emergency traffic
        # is also sent to Ring 2; KOSA is intentionally isolated at the core.
        self._dispatch(MandalaRing.RING_0_CORE, routed_packet)
        target_ring = MandalaRing.RING_0_CORE if state == "KOSA" else MandalaRing.RING_2_SYMMETRY
        if target_ring != MandalaRing.RING_0_CORE:
            self._dispatch(target_ring, routed_packet)

        return {
            "score": score,
            "state": state,
            "node_id": node_id,
            "symmetry_pool": self.symmetry,
            "target_ring": target_ring,
            "routed": True,
        }
