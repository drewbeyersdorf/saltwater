# skills/ — vendored web-design skills

Curated 2026-08-10 from **github.com/MengTo/skills** (MIT License, © Meng To).
Upstream: 123 skills; we took 7. Do not add more without a tier decision recorded here.

## Tiers
- **Tier 1 — spine:** `scroll-world-storytelling`, `build-awwwards-quality-sites`, `optimize-web-animations`
- **Tier 2 — atmosphere (compound max 3–4):** `falling-leaves`, `pointer-trail-emitter`, `staggered-word-reveal`, `editorial-portfolio-chapters`

## Explicitly skipped upstream
- All 20 game-development skills, aura/unsplash media skills, ~70 overlapping mood/layout skills (duplicate dark-modes, three globe variants) — overlapping direction is worse than no direction.

## Adaptation notes
- Demos/assets NOT vendored (heavy). Each skill's workflow stands alone; if a demo is needed, fetch from upstream at build time.
- `scroll-world-storytelling` has three modes; house decision = Three.js world only.
- `optimize-web-animations` references Codex Browser; substitute the browser tooling of whichever agent is running — the workflow (baseline → patch smallest owner → verify offscreen count 0) is tool-agnostic.

## License
MIT — see upstream LICENSE. Attribution: "Skills adapted from MengTo/skills (github.com/MengTo/skills), MIT License."
