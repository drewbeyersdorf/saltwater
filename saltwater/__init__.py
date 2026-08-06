"""SALTWATER — an agentic orchestration harness transcribed from the
developmental biology of Crocodylus porosus.

Nest → Vocalize → Transport → Estuary → Open Water.

You do not deploy a living system. You raise it.
"""

from .types import Agent, Stage
from .nest import Nest, NestError
from .vocalize import Vocalize, QuorumNotReached
from .transport import Transport, HostileTerrain
from .estuary import Estuary, FenceViolation
from .open_water import OpenWater, Juvenile, RELEASE_BAR

__version__ = "0.1.0"

__all__ = [
    "Agent", "Stage",
    "Nest", "NestError",
    "Vocalize", "QuorumNotReached",
    "Transport", "HostileTerrain",
    "Estuary", "FenceViolation",
    "OpenWater", "Juvenile", "RELEASE_BAR",
    "__version__",
]
