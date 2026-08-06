"""Stage V — Open Water.

Then the mother withdraws. Not from indifference — because care that
never withdraws produces an animal that cannot hunt. Release is
graduated abandonment: autonomy granted precisely as fast as competence
is demonstrated, and not one heartbeat faster.

    from saltwater import OpenWater

    sea = OpenWater(agents)
    async for j in sea.graduate(metric="competence"):
        if j.thrives():
            sea.withdraw(j)   # it hunts alone now. that was the point.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field

from ..types import Agent, Stage

RELEASE_BAR = 0.8  # open water is earned, not defaulted


@dataclass
class Juvenile:
    """An agent in the act of earning the ocean."""

    agent: Agent
    thrive_score: float = 0.0

    def thrives(self) -> bool:
        return self.thrive_score >= RELEASE_BAR


@dataclass
class OpenWater:
    """Conditional release by demonstrated competence."""

    agents: list[Agent]
    released: list[Agent] = field(default_factory=list)

    async def graduate(self, metric: str = "competence"):
        """Yield each agent as a Juvenile, in waves of rising freedom.

        The caller evaluates each wave (real health checks, canary metrics)
        and feeds the result back with `j.thrive_score = ...`. Agents below
        the bar return to the estuary for another cycle — with a scar,
        not a funeral.
        """
        if metric != "competence":
            raise ValueError("open water recognizes one metric: competence")
        pending = [a for a in self.agents if a.stage != Stage.OPEN_WATER]
        for wave in range(3):  # three tides; then whatever remains is held
            if not pending:
                break
            still_learning = []
            for agent in pending:
                j = Juvenile(agent=agent, thrive_score=agent.competence)
                yield j
                agent.competence = j.thrive_score  # the caller's judgment, recorded
                if j.thrives():
                    continue  # caller should withdraw(j) via sea.withdraw
                if agent not in self.released:
                    agent.scar(f"tide {wave + 1}: not yet — returned to the estuary")
                    agent.stage = Stage.ESTUARY
                    still_learning.append(agent)
            pending = still_learning
            await asyncio.sleep(0)

    def withdraw(self, juvenile: Juvenile) -> Agent:
        """The final act of care. The agent hunts alone now."""
        if not juvenile.thrives():
            raise PermissionError(
                f"{juvenile.agent.name} has not demonstrated open-water competence "
                f"({juvenile.thrive_score:.2f} < {RELEASE_BAR}) — the mother stays"
            )
        juvenile.agent.stage = Stage.OPEN_WATER
        if juvenile.agent not in self.released:
            self.released.append(juvenile.agent)
        return juvenile.agent
