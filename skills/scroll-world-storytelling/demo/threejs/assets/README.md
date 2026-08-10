# assets/ — pinned Three.js runtime (fetch at build time, not vendored)

The upstream demo pins a local Three.js split-build (r167-style: `three.module.min.js` + `three.core.min.js`).
The minified binaries (~736 KB total) are intentionally NOT vendored in git. Fetch them pinned:

```bash
cd skills/scroll-world-storytelling/demo/threejs/assets
curl -fsSLO https://unpkg.com/three@0.167.1/build/three.module.min.js
curl -fsSLO https://unpkg.com/three@0.167.1/build/three.core.min.js
```

(or run `fetch.sh` in this directory)

License: Three.js is MIT — see THREE-LICENSE.txt upstream. Keep the pin exact; do not
upgrade casually — the demo was tuned against this build.

`index.html` imports `./assets/three.module.min.js`, which internally imports
`./three.core.min.js` — both files must be present.
