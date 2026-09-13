from dataclasses import dataclass, field
from enum import IntEnum
from typing import Callable, Any, Dict, List
import numpy as np


class MandalaRing(IntEnum):
    RING_0_CORE = 0         # Centrum / dyspozytor nadrzędny
    RING_1_SECURITY = 1     # Walidacja limitów i integralności
    RING_2_SYMMETRY = 2     # Węzły symetrii obliczeniowej
    RING_3_INTERFACE = 3    # Bramy wejściowe i telemetria


@dataclass
class MandalaPacket:
    source_ring: MandalaRing
    payload: np.ndarray
    intent: str = "TELEMETRY"
    routed_nodes: List[int] = field(default_factory=list)


class MandalaRouter:
    """
    Topologia Mandali jako wielopierścieniowy router zdarzeń DARTRIX.
    Centrum (Ring 0) zarządza wagami i bezpieczeństwem.
    Symetria definiuje równomierne rozproszenie strumienia w Ring 2.
    """

    def __init__(self, symmetry: int = 8):
        self.symmetry = symmetry
        self.weights = np.array([2, 4, 6, 2, 7], dtype=float)
        self.subscribers: Dict[MandalaRing, List[Callable[[MandalaPacket], Any]]] = {
            ring: [] for ring in MandalaRing
        }

    def register(self, ring: MandalaRing, handler: Callable[[MandalaPacket], Any]) -> None:
        self.subscribers[ring].append(handler)

    def route(self, packet: MandalaPacket) -> Dict[str, Any]:
        # Ring 1: Walidacja integralności wektora
        if packet.payload.shape != (5,):
            raise ValueError(f"Wymagany wektor 5-elementowy, otrzymano {packet.payload.shape}")

        if not np.all((packet.payload >= 0.0) & (packet.payload <= 1.0)):
            raise ValueError("Wektor telemetrii musi być znormalizowany do przedziału [0, 1]")

        # Ring 2: Deterministyczne przypisanie do węzła symetrii
        node_id = int(np.sum(packet.payload * 100)) % self.symmetry
        packet.routed_nodes.append(node_id)

        # Ring 0: Filtracja przez wagi 24627
        score = float(np.dot(packet.payload, self.weights))

        if score < 3.0:
            state = "HARMONIA"
        elif score < 6.0:
            state = "STRUKTURA"
        elif score < 9.0:
            state = "INTEGRACJA"
        else:
            state = "KOSA"

        for handler in self.subscribers.get(packet.source_ring, []):
            handler(packet)

        return {
            "score": score,
            "state": state,
            "node_id": node_id,
            "symmetry_pool": self.symmetry,
            "routed": True
        }
