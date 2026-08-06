"""Field notes, verified. Run: python -m pytest tests/ -q  (or unittest)."""

import asyncio
import unittest

from saltwater import (
    Agent, Stage, Nest, NestError, Vocalize, QuorumNotReached,
    Transport, HostileTerrain, Estuary, FenceViolation, OpenWater,
)


def hatch(n=3):
    nest = Nest(medium="estuarine", temperature=31.6)
    with nest.incubate() as env:
        return [env.clutch(f"agent-{i}") for i in range(n)]


class TestNest(unittest.TestCase):
    def test_environment_imprints(self):
        agents = hatch()
        self.assertEqual(agents[0].environment["medium"], "estuarine")
        self.assertEqual(agents[0].stage, Stage.NEST)

    def test_unviable_temperature_refused(self):
        with self.assertRaises(NestError):
            Nest(temperature=28.0)


class TestVocalize(unittest.TestCase):
    def test_no_quorum_no_hatch(self):
        chorus = Vocalize(clutch=hatch(4), quorum=0.75)
        chorus.call(chorus.clutch[0])  # only one calls
        with self.assertRaises(QuorumNotReached):
            asyncio.run(chorus.hatch())

    def test_full_chorus_hatches_together(self):
        chorus = Vocalize(clutch=hatch(), quorum=1.0)
        for a in chorus.clutch:
            chorus.call(a)
        hatched = asyncio.run(chorus.hatch())
        self.assertTrue(all(a.stage == Stage.VOCALIZED for a in hatched))


class TestTransport(unittest.TestCase):
    def test_jaws_carry_and_release(self):
        clutch = hatch()
        escort = Transport.jaws(route=["nest", "bank", "estuary"])
        released = asyncio.run(escort.carry(clutch).release_at("estuary"))
        self.assertTrue(all(a.stage == Stage.TRANSPORTED for a in released))

    def test_refuses_undeclared_destination(self):
        escort = Transport.jaws(route=["nest", "estuary"]).carry(hatch())
        with self.assertRaises(HostileTerrain):
            asyncio.run(escort.release_at("open_ocean"))

    def test_bite_pressure_must_be_zero(self):
        with self.assertRaises(ValueError):
            Transport.jaws(route=["nest"], bite_pressure=0.1)


class TestEstuary(unittest.TestCase):
    def test_fence_holds_for_unproven_agent(self):
        nursery = Estuary()
        nursery.fade()
        with self.assertRaises(FenceViolation):
            nursery.permit(hatch(1)[0], "irreversible_writes")

    def test_fence_fades_with_competence(self):
        nursery = Estuary()
        nursery.fade()
        agent = hatch(1)[0]
        agent.prove(0.7)
        nursery.permit(agent, "irreversible_writes")  # should not raise

    def test_raise_accumulates_competence(self):
        clutch = hatch()
        asyncio.run(Estuary().raise_(clutch, until="juvenile"))
        self.assertTrue(all(a.competence > 0 for a in clutch))


class TestOpenWater(unittest.TestCase):
    def test_release_requires_competence(self):
        from saltwater.open_water import Juvenile
        sea = OpenWater(hatch())
        weak = Juvenile(agent=sea.agents[0], thrive_score=0.3)
        with self.assertRaises(PermissionError):
            sea.withdraw(weak)

    def test_full_lifecycle(self):
        clutch = hatch()
        chorus = Vocalize(clutch=clutch, quorum=1.0)
        for a in chorus.clutch:
            chorus.call(a)
        asyncio.run(chorus.hatch())
        escort = Transport.jaws(route=["nest", "estuary"])
        asyncio.run(escort.carry(clutch).release_at("estuary"))
        asyncio.run(Estuary().raise_(clutch, until="juvenile"))
        sea = OpenWater(clutch)

        async def run_sea():
            async for j in sea.graduate():
                j.thrive_score = min(1.0, j.agent.competence + 0.25)
                if j.thrives():
                    sea.withdraw(j)

        asyncio.run(run_sea())
        self.assertTrue(all(a.stage == Stage.OPEN_WATER for a in sea.released))


if __name__ == "__main__":
    unittest.main()
