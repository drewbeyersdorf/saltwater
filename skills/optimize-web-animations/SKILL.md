---
name: optimize-web-animations
description: Profile, audit, and optimize frontend page performance with emphasis on animation work, memory-leak risks, long-session slowdowns, CSS animations, canvas/WebGL requestAnimationFrame loops, marquees, skeletons, GSAP/Three/Matter effects, timers, listeners, and observers. Use when the user asks to make animations performant, pause offscreen animations, look for memory leaks, profile pages that slow the computer over time, fix janky scrolling, or reduce CPU/GPU use on frontend pages.
---

# Optimize Web Animations

## Core Rule

Measure the real page before editing. The goal is not to remove motion; it is to make offscreen work stop, visible motion resume correctly, and route/unmount cleanup release long-lived resources.

Use whatever browser tooling the running agent has (Codex Browser, Playwright, headless Chrome). The workflow is tool-agnostic.

## Workflow

1. Inspect repo context.
   - Read `AGENTS.md` or local instructions.
   - Run `git status --short` early.
   - Find page components, animation hooks, CSS keyframes, `requestAnimationFrame`, `setInterval`, `setTimeout`, canvas/WebGL/physics components, media elements, GSAP timelines/tweens, and existing visibility utilities.
   - Search effect cleanup for event listeners, observers, RAF loops, intervals, timers, external scripts, media streams, WebGL textures/materials/geometries/renderers, and async work that can complete after unmount.

2. Capture a baseline in the browser.
   - Open the exact route the user named.
   - Profile at top, mid-page, footer/lower content, and one mobile viewport when layout could differ.
   - Count CSS animations by computed `animationName`, `animationPlayState`, and visibility. Include `::before` and `::after`.
   - Inspect canvases/WebGL elements separately; CSS profiling does not prove RAF loops have stopped.
   - Record which animation names are running offscreen and the DOM owners responsible.
   - For memory/leak asks, also record element/canvas/image/iframe counts, exposed JS heap metrics when available, an idle sample after 10-30 seconds, and a short route-cycle sample.
   - Keep stress tests bounded.

3. Patch the smallest owner that controls the motion.
   - Prefer an existing page reveal/visibility hook if the app has one.
   - Otherwise add an `IntersectionObserver` that toggles a stable class such as `is-offscreen` on sections and animated child elements.
   - Pause CSS animations with targeted rules:

```css
main > section.is-offscreen .expensive-animation,
.expensive-animation.is-offscreen {
  animation-play-state: paused !important;
}
```

   - For marquee/ticker tracks, pause the track when its section is offscreen.
   - For skeleton loaders and pseudo-element glimmers, include `::before` and `::after` pause selectors where needed.
   - For canvas/WebGL/physics loops, gate the RAF loop directly:
     - Start when the canvas/container intersects.
     - Cancel `requestAnimationFrame` when offscreen.
     - Resume on re-entry.
     - Disconnect observers and cancel frames on cleanup.
   - Respect `prefers-reduced-motion` if the component already does, and avoid introducing render loops for scroll/animation state.
   - For leak hardening:
     - Clear every timeout/interval created by the effect.
     - Cancel RAF before unmount and before restarting a loop.
     - Disconnect `IntersectionObserver`, `ResizeObserver`, `MutationObserver`, and custom subscriptions.
     - Remove global/window/document listeners with the same handler reference.
     - Dispose Three/WebGL textures, materials, geometries, renderers, and remove renderer DOM nodes.
     - Kill GSAP tweens/timelines for DOM nodes and mutable objects such as shader uniforms.
     - Stop media streams and pause detached video/audio sources.
     - Guard async loaders with an `isDisposed` flag and dispose loaded resources if they resolve after unmount.
     - Cap physics or simulation frame deltas after visibility pauses so delayed frames do not run oversized updates.

4. Verify behavior, not just builds.
   - Reload the route and rerun the same top/mid/footer/mobile profiles.
   - Target result: `offscreenRunningCount: 0` for the page sections under test.
   - Confirm visible animations still run or resume when scrolled into view.
   - For leak audits, compare before/after route cycles and idle samples.
   - Exercise a normal page interaction so the observer does not break dynamic content.
   - Check fresh-tab console warnings/errors.

5. Run local checks.
   - Use the repo's normal gates (lint, build, `git diff --check`).

6. Commit narrowly. Never stage broad files from a dirty worktree unless every hunk belongs to the task.

7. Report with evidence.
   - Lead with findings: what was still running, what looked leak-prone, and what could not be measured.
   - Separate source-audit risks from live measurements.
   - State limitations plainly.

## Good Fix Patterns

- Section-level `is-offscreen` plus element-level `is-offscreen` for long sections.
- `IntersectionObserver` thresholds around `0.01` for animation gating.
- Direct RAF loop control for WebGL/canvas effects; CSS `animation-play-state` cannot pause JavaScript render loops.
- Frame delta caps for physics loops that resume after a paused or delayed frame.
- `isDisposed` guards for image/video/texture/data loaders that may resolve after unmount.
- Short idle and route-cycle probes to catch accumulating DOM nodes, canvases, iframes, or unreleased media.

## Avoid

- Removing all animations to make the profile pass.
- Pausing visible hero motion because an ancestor selector is too broad.
- Assuming `animation-play-state` covers pseudo-elements or JavaScript RAF loops.
- Trusting a single top-of-page measurement on long pages.
- Treating unavailable heap counters as proof there is no memory leak.
- Using screenshots alone as performance proof.
- Letting unrelated local hunks ride along in the commit.
