"""The animal, as a datatype.

Everything in SALTWATER raises an Agent. An Agent is deliberately small:
a name, an environment it was shaped by, a record of what it has proven,
and the stage it has reached. Competence is not asserted. It is accumulated.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum


class Stage(Enum):
    """The five stages of a raised agent, in order. There is no sixth."""

    EGG = "egg"
    NEST = "nest"
    VOCALIZED = "vocalized"
    TRANSPORTED = "transported"
    ESTUARY = "estuary"
    OPEN_WATER = "open_water"


@dataclass
class Agent:
    """A workload being raised. Born in a Nest, released to Open Water."""

    name: str
    environment: dict = field(default_factory=dict)
    stage: Stage = Stage.EGG
    competence: float = 0.0  # earned, never assigned above zero at birth
    scars: list[str] = field(default_factory=list)  # failures survived, kept on record

    def prove(self, amount: float) -> None:
        """Record demonstrated competence. The only way the number moves."""
        if amount <= 0:
            return
        self.competence = min(1.0, self.competence + amount)

    def scar(self, note: str) -> None:
        """Record a failure survived. Scars are data, not shame."""
        self.scars.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} — {note}")

    @property
    def juvenile_ready(self) -> bool:
        """A conservative readiness bar for leaving the estuary."""
        return self.competence >= 0.6

    def __repr__(self) -> str:  # keep logs legible
        return f"<Agent {self.name!r} stage={self.stage.value} competence={self.competence:.2f}>"
