# SALTWATER

**An agentic orchestration harness transcribed from the developmental biology of *Crocodylus porosus*.**

> You do not *deploy* a living system. You *raise* it.

The saltwater crocodile has been running the same deployment protocol for two hundred million years: five stages, each with eligibility, each with witnesses, ending in a withdrawal that is itself an act of care. SALTWATER copies that protocol into Python. Nothing here is invented. It is annotated.

```
Nest → Vocalize → Transport → Estuary → Open Water
```

Zero dependencies. Python 3.11+. asyncio-native. About 600 lines — read it in one sitting, the way you'd read a field guide.

---

## Install

```bash
pip install saltwater-harness        # once published
# or, from this repo:
pip install -e .
```

## The sixty-second tour

```python
import asyncio
from saltwater import Nest, Vocalize, Transport, Estuary, OpenWater

async def main():
    # I · The womb comes first — environment shapes what hatches from it
    nest = Nest(medium="estuarine", temperature=31.6, guardrails=True)
    with nest.incubate() as env:
        clutch = [env.clutch(f"agent-{i}") for i in range(3)]

    # II · Emerge together, or not at all
    chorus = Vocalize(clutch=clutch, quorum=1.0)
    async with chorus.listen() as round_:
        for a in clutch:
            round_.call(a)                      # health checks report in
        await round_.until_ready(timeout=30.0)
        await round_.hatch()

    # III · The strongest part of the system escorts the weakest
    escort = Transport.jaws(route=["nest", "bank", "estuary"], bite_pressure=0.0)
    await escort.carry(clutch).release_at("estuary")

    # IV · Real traffic, fading fences
    nursery = Estuary(live_traffic=True, fence=["irreversible_writes"])
    nursery.fade(policy="demonstrated_competence")
    await nursery.raise_(clutch, until="juvenile")

    # V · Let go exactly as fast as competence is proven
    sea = OpenWater(clutch)
    async for j in sea.graduate(metric="competence"):
        j.thrive_score = your_canary_metric(j.agent)   # you judge each wave
        if j.thrives():
            sea.withdraw(j)                     # it hunts alone now

asyncio.run(main())
```

A runnable version of this — with the field notes printed — lives at [`examples/simple_agent.py`](examples/simple_agent.py).

---

## The five stages

### I · Nest — *environment-as-configuration*

A crocodile nest is a compost heap that warms itself, and its temperature decides the sex of every egg inside. The nest doesn't advise its babies; it **designs** them. SALTWATER's `Nest` works the same way: the environment is declared and validated *before* any agent exists, and every hatchling carries its imprint.

- Environments outside the viable range (30–33 °C, or an unknown `medium`) are refused — nothing raised in a dead mound survives.
- `medium` answers the deployment question the animal answers: `sovereign` (your own river), `pelagic` (rented ocean), or `estuarine` (control plane local, data plane cloud — the default, and the crocodile's own choice).

### II · Vocalize — *consensus before emergence*

Hours before hatching, embryos call from inside their shells, and the calls synchronize the clutch: **they emerge together or not at all.** `Vocalize` gathers readiness calls from a group of agents and refuses to `hatch()` below quorum. If your launch needs ten agents and seven are ready — the crocodile says wait.

### III · Transport — *power in service of fragility*

The mother carries hatchlings in her jaws — the same jaws that crush buffalo — and doesn't leave a scratch. `Transport.jaws()` moves freshly hatched agents across hostile topology along a **pre-declared route** (the mother does not improvise with lives in her mouth), verifies every leg, and sets them down at safe water. `bite_pressure` must be `0.0`. That is not a joke; it is an invariant.

### IV · Estuary — *a true ocean, fenced*

The nursery has real prey and real current, but no sharks. `Estuary` puts agents on live traffic inside fences (`irreversible_writes`, `open_ocean`) that block the unforgivable mistakes — and `fade()` drops those fences **per agent, by demonstrated competence only**, never by calendar. Failures are recorded as `scars`: data, not shame.

### V · Open Water — *graduated abandonment*

Then the mother leaves — because care that never withdraws produces an animal that cannot hunt. `OpenWater.graduate()` yields agents in waves of rising freedom; you score each wave with your real metrics, and `withdraw()` releases only what has thrived. The bar is 0.8. Below it, the agent returns to the estuary. With a scar, not a funeral.

---

## Connect an agent — local or cloud

SALTWATER doesn't care where your agent *runs*. It cares how it's *raised*. Any object with a `name` works — wire in your own health checks and metrics with three small hooks.

**Local agent** (runs on your machine — `medium="sovereign"`):

```python
from saltwater import Agent

agent = Agent(name="my-local-agent")

# 1 · readiness — used by Vocalize.until_ready()
async def ready() -> bool:
    return my_model_is_loaded()          # your check: model loaded, port open, GPU warm

agent.ready = ready

# 2 · work — used by Estuary.raise_() as its training exercise
async def exercise(a) -> float:
    result = await run_local_inference(a, sample_batch)
    return result.accuracy               # 0.0–1.0: demonstrated competence
```

**Cloud agent** (runs on rented compute — `medium="pelagic"`):

```python
agent = Agent(name="my-cloud-agent")

async def ready() -> bool:
    return (await http.get(f"{SERVICE_URL}/health")).status_code == 200

agent.ready = ready

async def exercise(a) -> float:
    result = await http.post(f"{SERVICE_URL}/canary", json=sample_batch)
    return result.json()["score"]        # 0.0–1.0: demonstrated competence
```

**Both at once — the estuarine default** (control plane local, limbs in the cloud):

```python
nest = Nest(medium="estuarine")                     # heart at home, limbs range
nursery = Estuary(control_plane="local", data_plane="cloud")
```

Then raise them all through the same five stages. At release, feed `OpenWater` your real production metric:

```python
async for j in sea.graduate(metric="competence"):
    j.thrive_score = await your_canary_metric(j.agent)  # local fn or HTTP call — same shape
    if j.thrives():
        sea.withdraw(j)
```

That's the whole integration: **`ready()` for consensus, an `exercise` for training, a score for release.** Everything else — the fences, the route, the quorum — the harness handles.

## Local, cloud, or both?

The animal already answered: keep the heart — the control loop — in your own chest, and let the limbs range wherever the current is cheap. Every stage inherits this: `Estuary(control_plane="local", data_plane="cloud")`. Sovereignty is anatomy, not a flag.

## Running the tests

```bash
python -m unittest discover tests -v     # no dependencies needed
# or, if you have pytest:
pytest tests/ -q
```

## Project layout

```
saltwater/
  types.py               the animal, as a datatype (Agent, Stage, competence, scars)
  nest/config.py         Stage I   — environment-as-configuration
  vocalize/consensus.py  Stage II  — pre-emergence consensus
  transport/maternal.py  Stage III — guarded migration
  estuary/nursery.py     Stage IV  — bounded live staging
  open_water/release.py  Stage V   — graduated abandonment
examples/simple_agent.py one full lifecycle, mound to ocean
tests/test_lifecycle.py  the field notes, verified
```

## Lineage

SALTWATER is Wing I of CULTUS — a house of harnesses transcribed from disciplines that raised things well before software existed. Wings in transcription: **ORDO** (theology — lifecycle as liturgy), **HYPHAE** (mycology — swarm as mycelium), **MASTERWORK** (guildcraft — promotion by proof).

## License

MIT. The protocol is two hundred million years old and belongs to everyone.
