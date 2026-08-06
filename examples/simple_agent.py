"""A full lifecycle, from mound to ocean.

Run it:

    python examples/simple_agent.py

It raises three agents through all five stages and prints the field notes.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # run from a fresh clone

from saltwater import Nest, Vocalize, Transport, Estuary, OpenWater


async def main() -> None:
    # ── Stage I · The Nest — the womb comes first ────────────────────
    nest = Nest(medium="estuarine", temperature=31.6, guardrails=True)
    with nest.incubate() as env:
        clutch = [env.clutch(name) for name in ("harvester-07", "harvester-08", "harvester-09")]
    print(f"I · NEST        hatched {[a.name for a in clutch]} at {nest.temperature}°C")

    # ── Stage II · The Vocalize — together, or not at all ────────────
    chorus = Vocalize(clutch=clutch, quorum=1.0)
    async with chorus.listen() as round_:
        for agent in clutch:          # in production these calls come from
            round_.call(agent)        # health checks reporting readiness
        await round_.until_ready(timeout=5.0)
        await round_.hatch()
    print("II · VOCALIZE   the clutch sang in tune — all hatched together")

    # ── Stage III · The Transport — jaws as cradle ───────────────────
    escort = Transport.jaws(route=["nest", "bank", "shallows", "estuary"])
    await escort.carry(clutch).release_at("estuary")
    print(f"III · TRANSPORT carried to {'/'.join(escort.route)} with bite_pressure=0.0")

    # ── Stage IV · The Estuary — real water, fading fences ───────────
    nursery = Estuary(live_traffic=True, fence=["irreversible_writes"])
    nursery.fade(policy="demonstrated_competence")
    await nursery.raise_(clutch, until="juvenile")
    try:
        nursery.permit(clutch[0], "irreversible_writes")
    except Exception as e:
        print(f"IV · ESTUARY    fence held: {e}")
    print(f"IV · ESTUARY    competence after training: "
          f"{[f'{a.competence:.2f}' for a in clutch]}")

    # ── Stage V · Open Water — graduated abandonment ─────────────────
    sea = OpenWater(clutch)
    async for j in sea.graduate(metric="competence"):
        j.thrive_score = min(1.0, j.agent.competence + 0.2)  # canary results, simulated
        if j.thrives():
            sea.withdraw(j)
    print(f"V · OPEN WATER  released: {[a.name for a in sea.released]}")
    print("\nThe mother withdraws. That was the point.")


if __name__ == "__main__":
    asyncio.run(main())
