"""Stage II — The Vocalize.

Hours before hatching, the embryos begin calling from inside their
shells — and the calls synchronize the clutch. They emerge together
or not at all. Consensus is not a committee. It is the sound a
distributed system makes before it agrees to be born.

    from saltwater import Vocalize

    round = Vocalize(clutch=agents, quorum=0.75)
    async with round.listen() as chorus:
        await chorus.until_ready(timeout=30.0)
        await chorus.hatch()   # all, or none
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager

from ..types import Agent, Stage


class QuorumNotReached(TimeoutError):
    """The clutch never sang in tune. Nobody hatches. That is the point."""


class Vocalize:
    """Pre-emergence consensus for a clutch of agents."""

    def __init__(self, clutch: list[Agent], quorum: float = 0.75) -> None:
        if not clutch:
            raise ValueError("an empty clutch has nothing to synchronize")
        if not 0.0 < quorum <= 1.0:
            raise ValueError("quorum must be in (0, 1]")
        self.clutch = clutch
        self.quorum = quorum
        self._ready: set[str] = set()

    @asynccontextmanager
    async def listen(self):
        """Open the chorus. Calls are gathered; nothing emerges yet."""
        yield self

    def call(self, agent: Agent) -> None:
        """One embryo announces readiness. (In real deployments, wire this
        to health checks reporting in.)"""
        if agent in self.clutch or any(a.name == agent.name for a in self.clutch):
            self._ready.add(agent.name)

    async def until_ready(self, timeout: float = 30.0, poll: float = 0.05) -> None:
        """Wait until at least `quorum` of the clutch has called.

        Agents that have not explicitly called are polled via an optional
        async `ready()` attribute — a hook for real health checks.
        """
        async def _gather() -> None:
            while True:
                for agent in self.clutch:
                    if agent.name in self._ready:
                        continue
                    probe = getattr(agent, "ready", None)
                    if probe is not None and await probe():
                        self._ready.add(agent.name)
                if self.reached:
                    return
                await asyncio.sleep(poll)

        try:
            await asyncio.wait_for(_gather(), timeout=timeout)
        except asyncio.TimeoutError as exc:
            raise QuorumNotReached(
                f"only {len(self._ready)}/{len(self.clutch)} of the clutch called "
                f"within {timeout}s (quorum {self.quorum:.0%}) — emergence aborted"
            ) from exc

    @property
    def reached(self) -> bool:
        return len(self._ready) >= self.quorum * len(self.clutch)

    async def hatch(self) -> list[Agent]:
        """Atomic, collective emergence. All, or none."""
        if not self.reached:
            raise QuorumNotReached("hatch() called before the chorus reached quorum")
        for agent in self.clutch:
            agent.stage = Stage.VOCALIZED
        return self.clutch
