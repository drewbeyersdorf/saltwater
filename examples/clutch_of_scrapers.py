"""Real-life application: raising a clutch of web-research agents.

Scenario: you run a research desk. Every morning you deploy a small fleet of
agents that crawl sources, extract facts, and file briefs. They run against
real HTTP services (here: a tiny local health server), so the harness's
"connect an agent" hooks are exercised exactly as they would be in the cloud.

The harness stages map to the operation:

    NEST       -> one shared config (endpoints, timeouts, secrets location)
    VOCALIZE   -> do not launch until every agent's /health reports ready
    TRANSPORT  -> move the clutch from staging to production, zero bite
    ESTUARY    -> fenced practice runs against canary endpoints; competence
                  is earned, and only earned competence lifts the fences
    OPEN WATER -> only agents scoring >= 0.8 join the live fleet

Run it:
    python examples/clutch_of_scrapers.py
"""

import asyncio
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from saltwater import Agent, Estuary, Nest, OpenWater, Transport, Vocalize


# --- A tiny "production service" the agents will be raised against ----------

class ServiceHandler(BaseHTTPRequestHandler):
    """Fake source service: /health answers ready, /canary returns a fact."""

    def do_GET(self):  # noqa: N802 - stdlib naming
        if self.path == "/health":
            body = json.dumps({"ready": True}).encode()
        elif self.path == "/canary":
            body = json.dumps({"fact": "Crocodylus porosus can exceed 6 m."}).encode()
        else:
            body = b"{}"
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_):  # keep the demo output clean
        pass


def start_service(port=8731):
    server = HTTPServer(("127.0.0.1", port), ServiceHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


# --- The agents: same hooks for local functions or cloud services -----------

class ResearchAgent:
    """A minimal real agent. In the cloud these three methods are HTTP calls
    (GET /health, POST /canary, GET /score); locally they are plain Python."""

    def __init__(self, name, endpoint):
        self.name = name
        self.endpoint = endpoint
        self.skill = 0.0

    async def ready(self) -> bool:          # Vocalize hook
        import urllib.request
        try:
            with urllib.request.urlopen(f"{self.endpoint}/health", timeout=2) as r:
                return json.loads(r.read())["ready"]
        except Exception:
            return False

    async def exercise(self) -> float:      # Estuary hook
        import urllib.request
        try:
            with urllib.request.urlopen(f"{self.endpoint}/canary", timeout=2) as r:
                json.loads(r.read())
            self.skill = min(1.0, self.skill + 0.4)
        except Exception:
            self.skill = min(1.0, self.skill + 0.1)
        return self.skill

    @property
    def thrive_score(self) -> float:        # Open Water hook
        return self.skill


async def main():
    server = start_service()
    endpoint = "http://127.0.0.1:8731"

    # I. THE NEST -- environment as config. Viable temperature or nothing.
    nest = Nest(medium="estuarine", temperature=31.5)
    with nest.incubate():
        clutch = [nest.clutch(name) for name in ("ARCHIE", "BINDI", "CASSIUS")]

    # II. VOCALIZE -- nobody hatches until every voice answers.
    vocalize = Vocalize(clutch)
    for a in clutch:
        a.impl = ResearchAgent(a.name, endpoint)   # attach the real worker
    for a in clutch:
        a.ready = a.impl.ready                     # wire the hook
    await vocalize.until_ready(timeout=5.0)
    print("vocalize: the whole clutch answered. Hatching together.")
    await vocalize.hatch()

    # III. TRANSPORT -- staging to production, jaws never closing.
    route = Transport.jaws(route=["staging", "review", "production"])
    route.carry(clutch)
    await route.release_at("production")
    print("transport: clutch moved to production waters. bite pressure 0.0.")

    # IV. ESTUARY -- fenced practice. Fences fade by demonstrated competence.
    estuary = Estuary()
    estuary.fade(policy="demonstrated_competence")
    await estuary.raise_(clutch, exercise=lambda a: a.impl.exercise())
    for a in clutch:
        print(f"estuary: {a.name:<8} competence={a.competence:.2f} "
              f"juvenile_ready={a.juvenile_ready}")

    # V. OPEN WATER -- only the proven join the fleet.
    open_water = OpenWater(clutch)
    async for juvenile in open_water.graduate():
        # the real worker's score is the judgment that matters
        juvenile.thrive_score = juvenile.agent.impl.thrive_score
        if juvenile.thrives():
            print(f"open water: {juvenile.agent.name} joins the live fleet "
                  f"(score {juvenile.thrive_score:.2f}).")
        else:
            open_water.withdraw(juvenile)
            print(f"open water: {juvenile.agent.name} returns to the estuary.")

    server.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
