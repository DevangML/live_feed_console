# Live Feed simulation and architecture explorer

Run `npm run visualizer` from the project root, then open http://localhost:8088.
The server binds to loopback. `VISUALIZER_PORT` optionally changes the port.
The landing page is the simulation. `/architecture.html` is the secondary file
and relationship explorer; `/katas.html` remains a separate language lab.

## The simulation

The single **Play system** action replays one payload across eight deliberately
slow stops: the request boundary, response text, `parseJson`, schema validation,
timestamp normalization, metadata enrichment, explicit Feed telemetry, and the
UI preview. Each stop shows the exact input, operation, reason, and output.
**Pause**, **Next step**, the step markers, and the file cards are the only
controls needed for normal use. The valid, missing-field, and malformed fixtures
make the failure boundary visible without pretending that the unfinished
`PollingFeed` or production UI already exists.

## Working with the view

- Select a cloud, stage button, or searchable file entry to open its inspector.
- `/` focuses file search; Escape closes the inspector. Orbit is opt-in.
- The simulation imports and executes the actual pipeline functions and Feed
  methods. Transport and UI are explicit replay boundaries. The harness does not
  claim to run a network poller or mutate a production store.
- Modules are loaded for the current page session. Reload after source edits to
  run a fresh version of the trace functions.
- The page requests `/api/graph` every five seconds while visible. The server scans
  `src`, `utils`, and `tests` on each request. Unchanged revisions do not rebuild
  the WebGL scene. Changed graphs release old GPU geometry/materials/textures.
- New JS/TS-family files appear automatically. Literal relative imports are
  inferred with a lightweight scan, not a full parser. Unknown runtime files go
  into foundations pending role review; tests go into the verification dock.
  File identities use full relative paths for automatically discovered files.
- Test connections represent source references, not passing results, complete
  coverage, or mathematical proof. Historical curated text is not a live audit.

## Color and HDR

The light layer is a separate WebGPU presentation path. When the browser accepts
it, the canvas requests `rgba16float`, `display-p3`, and extended tone mapping.
The page checks the accepted canvas configuration and samples one GPU highlight;
it labels that value against SDR white. This is an actual extended-range render
signal, not a CSS glow or an ACES-looking screenshot. The browser still reports
physical display capability rather than the page proving panel luminance,
calibration, or peak nits. If WebGPU, HDR, or the requested format is unavailable,
the simulation stays usable and the display note identifies the SDR/P3 fallback.

## Contracts and boundaries

Existing node/edge/zone fields in `pipeline_graph.json` are retained. `/api/graph`
adds `revision`, `discovery`, and source metadata (`metrics`, `imports`,
`sourceHash`, `evidence`). Existing static graph URLs and the raw-code endpoint
remain available. Missing/invalid paths now return 404 instead of the main HTML.
Resolved paths and symlink targets must remain inside the repository.

`pipeline_graph.json` owns curated layout and explanations; the server overlays
source discovery in memory and does not rewrite it. The older `build_*` and
`generate_visualizer.py` scripts are one-time legacy generators: running them may
replace hand-edited UI/semantics. They are not part of startup or synchronization.

The 3D view still uses the existing externally hosted Three.js/OrbitControls and
fonts, so rendering requires those resources. The Python server adds no packages.

## Validation, 2026-09-10

- Baseline and final `npx vitest run`: 6 suites, 48 tests passing.
- `python3 -m unittest discover -s docs/visualizer/tests -v`: 3 checks passing,
  covering add/change/delete discovery, unique identities/import links, stable
  revisions, path containment/symlinks, and dock capacity.
- HTTP checks: main page, kata page, graph, source and trace module return 200;
  missing files and traversal requests return 404.
- Browser: desktop and 390px viewport inspected; valid, missing-field and malformed
  JSON traces exercised; search and live code checked. No browser warnings/errors
  observed during these checks.
- Actual source inspection found PollingFeed is an empty subclass and Feed has no
  automatic circuit breaker. The view now labels intended flow and avoids
  claiming automatic status transitions or purity for clock-dependent stages.

## Requested orchestration evidence

- Route: Ruflo `hooks_route` recommended coder for this visualizer change.
- Learn/store: source and server findings stored in `knowledge` under
  `live-feed-visualizer-inspection-20260910`.
- Recall: `memory_search` returned that entry before implementation (0.885 similarity).
- Applied paths: `docs/visualizer/index.html`, `server.py`, `pipeline_graph.json`,
  `trace.js`, and `tests/test_server.py`.
- Skill: ARGUS Contract Preserving Change, from
  `/Users/devang/.codex/skills/ruflo-shared/argus/contract-preserving-change/SKILL.md`.
- ARGUS MCP and repo `.argus` metadata were unavailable. No ARGUS validation pass
  is claimed; repo-native checks and browser validation are the evidence above.
