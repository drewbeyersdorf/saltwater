"""Stage IV — The Estuary.

The nursery water is real — real prey, real current, real consequence —
but bounded. No pelagic predator can enter. Staging is not a fake ocean.
It is a true one with the unforgivable parts fenced out, and the fences
fade exactly as fast as competence is demonstrated.

    from saltwater import Estuary

    nursery = Estuary(live_traffic=True, fence=["irreversible_writes"])
    nursery.fade(policy="demonstrated_competence")
    await nursery.raise_(agents, until="juvenile")
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field

from ..types import Agent, Stage


class FenceViolation(PermissionError):
    """An agent reached for open-ocean power from inside the nursery."""


@dataclass
class Estuary:
    """Bounded live staging. Safety that knows how to leave."""

    live_traffic: bool = True
    fence: list[str] = field(default_factory=lambda: ["irreversible_writes", "open_ocean"])
    control_plane: str = "local"   # the heart stays home
    data_plane: str = "cloud"      # the limbs may range
    _fading: bool = False

    def fade(self, policy: str = "demonstrated_competence") -> None:
        """Arm the guardrails to decay as agents prove themselves.
        The only supported policy — fences never drop on a timer."""
        if policy != "demonstrated_competence":
            raise ValueError("fences fade by demonstrated_competence only — never by calendar")
        self._fading = True

    def permit(self, agent: Agent, action: str) -> None:
        """The gate every action inside the nursery must pass.
        A fence drops for an agent only after it has proven itself."""
        if action not in self.fence:
            return
        if self._fading and agent.juvenile_ready:
            return  # the fence has faded for this agent specifically
        agent.scar(f"fence held against {action!r}")
        raise FenceViolation(
            f"{agent.name} reached for {action!r} from inside the estuary "
            f"(competence {agent.competence:.2f} < 0.60 — the fence holds)"
        )

    async def raise_(self, agents: list[Agent], until: str = "juvenile",
                     exercise=None) -> list[Agent]:
        """Grow the clutch on real traffic.

        `exercise` is an optional async callable(agent) -> float run each
        cycle; its return value is recorded as demonstrated competence.
        Without one, agents train on the nursery's own currents.
        """
        if until != "juvenile":
            raise ValueError("the estuary raises juveniles — open water does the rest")
        for agent in agents:
            agent.stage = Stage.ESTUARY
        # training cycles: honest work, real stakes, survivable consequences
        for _ in range(3):
            for agent in agents:
                try:
                    gained = await exercise(agent) if exercise else 0.2
                    agent.prove(gained)
                except Exception as exc:  # a scar, not a funeral
                    agent.scar(f"training injury: {exc}")
            await asyncio.sleep(0)
        return agents
