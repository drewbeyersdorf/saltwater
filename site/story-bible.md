# SALTWATER — Story Bible & Beat Ledger
Per `skills/scroll-world-storytelling/SKILL.md` — written BEFORE any site code. Mode: **Three.js world** (house decision, see AGENTS.md). Renderer skeleton: `skills/scroll-world-storytelling/demo/threejs/`.
Source of truth: README.md. Nothing below invents proof; every beat cites the harness or the animal.

---

## 1 · Contract

**Goal:** Turn the SALTWATER thesis into a one-page journey of 6 beats and one action. A first-time visitor should understand — you don't *deploy* a living system, you *raise* it — without reading the README.

**The one action:** `pip install saltwater-harness` / read the 600 lines. Clone-and-raise, not "sign up."

**House rules (from skill + AGENTS.md):**
- Native reversible scroll. Never hijack the wheel.
- One world, one motion grammar, one art direction per build (studies below are alternatives, not a stack).
- Kage-class budget: ≤1 MB JS, ≤3 MB total. Pinned local Three.js (demo/assets/fetch.sh).
- Reduced motion = designed stills in ordinary document flow, never hidden layers.
- Builder ≠ verifier when two agents are available (saltwater-dogfood receipts apply).

---

## 2 · Beat Ledger

The harness already has a five-stage arc; the site adds a hook and resolves to action. **Six beats.**

| # | id | scene (in the world) | eyebrow | headline | body (<24 words) | evidence | motion verb | scroll weight |
|---|---|---|---|---|---|---|---|---|
| 1 | hook | Dark water surface from below, amber light above. A shape glides past, unhurried | 200M years | You don't deploy a living system. | The saltwater crocodile has run the same deployment protocol for two hundred million years. We transcribed it. | README thesis line; banner.jpg | slow glide, light falls | 1.6 |
| 2 | nest | Submerged mound — compost warmth made visible as a field of heat; eggs suspended in it | I · Nest | The womb comes first. | Temperature designs the clutch. Environment is declared and validated before any agent exists. | `Nest(medium, temperature)` refuses unviable ranges; medium = sovereign/pelagic/estuarine | descend into warmth | 1.2 |
| 3 | vocalize | Points of light inside shells answering each other, synchronizing into one pulse | II · Vocalize | Together, or not at all. | Embryos call from inside the shell to synchronize the clutch. Quorum, or no hatch. | `Vocalize(quorum=1.0)`, `until_ready`, refusal below quorum | scattered pulses converge | 1.0 |
| 4 | transport | The sculpture's jaws-form: crushing geometry holding something small, perfectly intact | III · Transport | Power in service of fragility. | The jaws that crush buffalo carry hatchlings without a scratch. bite_pressure must be 0.0 — an invariant, not a joke. | `Transport.jaws(route, bite_pressure=0.0)`, pre-declared route, verified legs | careful carry along a route | 1.2 |
| 5 | estuary | The nursery: real current, visible fences — and one fence fading around a single swimmer | IV · Estuary | Real traffic, fading fences. | Live prey, no sharks. Fences drop per agent, by demonstrated competence — never by calendar. Failures are scars: data, not shame. | `Estuary(fence=["irreversible_writes"])`, `fade("demonstrated_competence")` | fence dissolves around competence | 1.4 |
| 6 | open-water | The fence is gone. Vast dark water. One swimmer receding, lit amber, alone — by design | V · Open Water | Care that withdraws. | The mother leaves because care that never withdraws produces an animal that cannot hunt. Release at 0.8. Below it: a scar, not a funeral. | `OpenWater.graduate()`, `withdraw()` at thrive ≥ 0.8 | recede into open dark | 1.4 |
| 7 | action | Still water, one line of type, one command | The protocol belongs to everyone | Raise your own. | Zero dependencies. Python 3.11+. About 600 lines — read it in one sitting, like a field guide. | README install block; MIT line | settle to stillness | 0.8 + CTA |

Total scroll ≈ 8.6 viewport heights. Within the skill's 0.7–1.8 per-beat band.

---

## 3 · Style Bible

**Mood (three adjectives):** submerged, amber-lit, unhurried.

**World metaphor:** the estuary itself — one continuous body of dark water the camera moves *through*: surface → mound → nursery → open sea. Not five scenes; one dive. The hero object is not a literal crocodile (reject the obvious); it is the **current** — particulate drift, god-rays, and one recurring sculptural form (jaws-as-architecture: crushing geometry held gently open) that appears at Transport and echoes after.

**Palette (from the existing house art — banner, the-nest, the-tank):**
| role | name | approx |
|---|---|---|
| dominant field | abyss green-black | `#0b1210` |
| secondary | deep estuary | `#16241f` |
| light | amber god-ray | `#e8a33d` |
| bone | fossil ivory (type on dark) | `#e8e2d4` |
| muted | silt | `#7a7568` |
| accent (used once, at the CTA) | signal coral | `#fc4b2f` |

**Typography:** display = condensed grotesk, uppercase, tight (field-guide plate lettering); reading = old-style serif (the README's voice). Type sits fossil-ivory on dark; hairline rules; numeric tabular figures for stage indices.

**Material language:** photographic dark water + engraved plate study (the Tabula Anatomica from the README folio). No glass, no neon.

**Motion grammar:** forward glide — the camera is a slow swimmer. Ambient drift only; scroll conducts. Word-reveals (staggered-word-reveal, 0.07s stagger) for headlines; falling-leaves mechanism recolored as **sediment/mangrove drift** (tumble + slip coupling, recycled ahead of camera); pointer-trail as **water disturbance** at the surface beat only — disabled below the surface.

**Pacing:** slow at hook and open-water (awe), deliberate through the three mechanism beats, still at the CTA.

**Exclusions (visual clichés, banned):** glowing blue planet in dark space; glassmorphism panels; literal cartoon crocodile mascot. (Also per awwwards skill: no gradient blobs, no bento, no logo wall, no fake testimonials.)

---

## 4 · Three art-direction studies (pick ONE before code)

Per skill: each changes field, material, light, composition — not just accent color.

| study | field | object material | light | type relationship | verdict |
|---|---|---|---|---|---|
| **A · Abyssal amber** | abyss green-black water, particulate drift | dark sculptural forms rim-lit from above | amber god-rays, single source | fossil-ivory plate type floats left, world right | **Recommended** — matches house art exactly; the banner is already this |
| B · Field-guide paper | warm ivory `#efe9dc`, ink-etched world | engraved line + hatching, plate-study style | diffuse daylight, no god-rays | black engraved type; world rendered as anatomical plate | strong; safer, but loses the "walk into the estuary" submersion |
| C · Signal nocturne | near-black blue-green `#08130f` | bioluminescent accent — the only light is what the agents emit | darkness broken by calls (Vocalize pulses drive illumination) | dim bone type; coral reserved for calls | most poetic, highest risk of reading as generic dark-tech |

Default if no decision is recorded: **A · Abyssal amber.**

---

## 5 · Asset & provenance plan

- Existing house art (banner.jpg, the-nest.jpg, the-cradle.jpg, plate-study.jpg, the-tank.jpg) is original to the house — reuse as reduced-motion stills and texture reference; keep provenance in source comments.
- The Three.js world is procedural (instanced particles, shader rays) — no stock, no generated video in v1.
- Three.js pinned via `skills/scroll-world-storytelling/demo/threejs/assets/fetch.sh` (MIT, three@0.167.1).

## 6 · Verification bar (before ship)

Per skill + optimize-web-animations: story arc explainable after one pass; reverse scroll restores state; 390/768/1024/1440; offscreen animation count = 0; console clean; total transfer ≤3 MB measured; reduced-motion pass reviewed by a second agent; no completion claim without browser evidence.

---

*Written 2026-08-10. Decisions recorded here are binding for site builds; changes require editing this file in the same commit as the code that depends on them.*
