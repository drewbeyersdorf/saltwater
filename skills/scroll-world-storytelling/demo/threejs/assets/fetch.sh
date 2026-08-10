#!/usr/bin/env bash
# Fetch the pinned Three.js split-build for the scroll-world threejs demo.
set -euo pipefail
cd "$(dirname "$0")"
curl -fsSLO https://unpkg.com/three@0.167.1/build/three.module.min.js
curl -fsSLO https://unpkg.com/three@0.167.1/build/three.core.min.js
echo "Pinned three@0.167.1 fetched. Serve the demo over http, e.g.:"
echo "  cd .. && python3 -m http.server 8000"
