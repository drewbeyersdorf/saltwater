# AGENTS.md — SALTWATER

An agentic orchestration harness transcribed from the developmental biology of *Crocodylus porosus*.
Nest → Vocalize → Transport → Estuary → Open Water.

## For every agent (Kimi, Claude, Codex, Cursor, Claw)

**Read the narrowest matching skill before building anything visual.** Skills live in `skills/` — vendored from MengTo/skills (MIT), curated 2026-08-10. Do not fetch new design skills without a note in `skills/README.md`.

### Routing
| If you are… | Read first |
|---|---|
| Building or changing the SALTWATER site / any scroll narrative | `skills/scroll-world-storytelling/SKILL.md` then `skills/build-awwwards-quality-sites/SKILL.md` |
| Adding atmosphere (particles, drift, cursor effects) | `skills/falling-leaves/SKILL.md` or `skills/pointer-trail-emitter/SKILL.md` |
| Animating headlines / philosophy copy | `skills/staggered-word-reveal/SKILL.md` |
| Building the harness field-guide ("Pokedex") pages | `skills/editorial-portfolio-chapters/SKILL.md` |
| Anything feels slow / profiling before ship | `skills/optimize-web-animations/SKILL.md` |
| Working on the Python harness itself | No design skill — see README.md and tests/ |

### House decisions (already made — don't relitigate)
1. **Renderer mode: Three.js world.** The crocodile/harness metaphor is spatial. Video-scrub and HTML-data modes are rejected for the main site (skill forbids mixing).
2. **Weight budget: Kage-class.** ≤1 MB JS, ≤3 MB total with imagery. `optimize-web-animations` is the enforcement pass before any ship.
3. **Atmosphere mapping:** falling-leaves → mangrove/sediment drift (recolor ramp to estuary palette, not autumn); pointer-trail → water disturbance. No autumn leaves, no confetti.
4. **The harness Pokedex is a field guide, not a card grid** — editorial chapters.
5. **Anti-slop constitution** (from build-awwwards-quality-sites): no gradient blobs, no glass-everywhere, no logo-wall theater, no fake testimonials, one smooth-scroll engine max, reduced-motion fallbacks are designed stills, not hidden layers.

### Where things live
- `/saltwater`, `/tests` — the Python harness (pip-installable).
- `/skills` — vendored web-design skills (this is the only skills directory).
- `/site` — the public site will live here (GitHub Pages). Not built yet.
- Related: `drewbeyersdorf/saltwater-dogfood` (private ops: WIP guard, receipts), `drewbeyersdorf/yej-kimi` (yej-io PR control plane, separate project).
