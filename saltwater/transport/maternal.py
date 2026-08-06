"""Stage III — The Transport.

The mother gathers the hatchlings into her jaws — the same jaws that
close on buffalo — and carries them, unharmed, through terrain that
would kill them. The most dangerous instrument in the system becomes
the vehicle of safe passage.

In the harness: maximal-privilege infrastructure escorts
minimal-privilege agents across hostile topology, verifies each leg
of the route, then lets go.

    from saltwater import Transport

    escort = Transport.jaws(route=["nest", "bank", "shallows"], bite_pressure=0.0)
    await escort.carry(agents).release_at("estuary")
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field

from ..types import Agent, Stage


class HostileTerrain(RuntimeError):
    """A leg of the route failed its safety check. The jaws close and wait."""


@dataclass
class Transport:
    """Guarded migration. Power in service of fragility."""

    route: list[str]
    bite_pressure: float = 0.0          # maximal strength, zero harm
    escorted: list[Agent] = field(default_factory=list)
    position: str = "nest"

    @classmethod
    def jaws(cls, route: list[str], bite_pressure: float = 0.0) -> "Transport":
        """Open the jaws along a fixed route. The route is declared up
        front — the mother does not improvise with lives in her mouth."""
        if not route:
            raise ValueError("a transport needs a route; the mother never wanders")
        if bite_pressure != 0.0:
            raise ValueError("bite_pressure must be 0.0 — these jaws are a cradle now")
        return cls(route=list(route), bite_pressure=bite_pressure)

    def carry(self, agents: list[Agent]) -> "Transport":
        """Gather the clutch. Nothing is carried that has not hatched."""
        for agent in agents:
            if agent.stage not in (Stage.NEST, Stage.VOCALIZED):
                raise HostileTerrain(
                    f"{agent.name} is at stage {agent.stage.value}; "
                    "only fresh hatchlings ride in the jaws"
                )
        self.escorted = list(agents)
        return self

    async def _traverse(self, leg: str, verify=None) -> None:
        """Cross one leg of the route, checking the ground first."""
        if verify is not None and not await verify(leg):
            raise HostileTerrain(f"leg {leg!r} failed its safety check — escort halted")
        await asyncio.sleep(0)  # yield: real escorts traverse real networks here
        self.position = leg

    async def release_at(self, destination: str, verify=None) -> list[Agent]:
        """Walk the declared route to `destination`, then set everyone down."""
        if not self.escorted:
            raise HostileTerrain("nothing to release — the jaws are empty")
        if destination not in self.route:
            raise HostileTerrain(
                f"{destination!r} is not on the declared route {self.route}; "
                "the mother goes where she scouted"
            )
        for leg in self.route:
            await self._traverse(leg, verify)
            if leg == destination:
                break
        for agent in self.escorted:
            agent.stage = Stage.TRANSPORTED
        released, self.escorted = self.escorted, []
        return released
