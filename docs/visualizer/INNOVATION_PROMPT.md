# SYSTEM INNOVATION PROMPT & SPECIFICATION SPEC: LIVE FEED CONSOLE 3D ARCHITECTURAL VISUALIZER

> **Target Model:** Frontier AI Architect / System Engineer (GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro/Ultra)  
> **Repository:** `live_feed_console` (`/Users/devang/Desktop/live_feed_console`)  
> **Role:** Staff Frontend Systems Architect & Creative Technologist  
> **Objective:** Recreate, maintain, and innovate upon the 3D Concept Cloud and Live Ingestion Architecture Visualizer.

---

## 1. EXECUTIVE CONTEXT & PRODUCT IDENTITY

### The Problem Being Solved
In standard JavaScript frontend development, real-time streaming data architectures (financial tickers, seismic monitors, IoT sensors) suffer from critical failure modes:
1. **Dirty Data at Boundaries:** APIs return unexpected `null`s, stringified numbers, or malformed JSON, crashing React render trees.
2. **Main-Thread Saturation:** Heavy JSON transformations on the UI thread cause frame drops and stuttering.
3. **Memory Leaks & Interval Hell:** Improperly managed `setInterval` loops retain references to dead component instances in closures, preventing V8 Mark-and-Sweep garbage collection.
4. **State Chaos & Reactivity Regressions:** Mutating state arrays in-place breaks React's shallow referential equality checks (`prev !== next`), causing missed renders.

### The Solution: Live Feed Console Engine
A zero-dependency, mathematically proven, high-frequency ingestion engine built in native ECMA-262 ES6+:
- **Boundary Pipeline:** Curried higher-order pure functions (`pipe` ➔ `parseJson` ➔ `validateSchema` ➔ `normalizeTimestamps` ➔ `enrichFeedMetadata`).
- **Resilient Motor:** Asynchronous polling motor (`PollingFeed`) with cooperative `AbortController` cancellation and non-overlapping recursive `setTimeout` scheduling.
- **Encapsulated State Machine:** Abstract base class (`Feed`) guarding private slots (`#id`, `#status`, `#endpoints`, `#consecutiveFailures`, `#lastLatencyMs`) with native `new.target` and defensive copying.
- **Telemetry Hierarchy:** Custom error inheritance tree (`FeedError` ➔ `NetworkError`, `ParseError`) tagging `feedId` and HTTP `statusCode` directly onto native errors.

---

## 2. THE VISUALIZER'S PURPOSE & INVARIANTS

The visualizer is **not** a documentation site. It is an **interactive, living 3D architectural cockpit** running at `http://localhost:8088` that renders the codebase as a physical computing universe.

### Immutable Design Invariants:
1. **Separation of Concerns:** 
   - **Main Map (`index.html`)**: Focuses exclusively on the **actual project dataflow**. Katas must **never** be mixed into this runtime pipeline.
   - **Kata Crucible (`katas.html`)**: Dedicated environment for language drills (Currying L1–L5, arity traps, coercion puzzles, Mettl/FAANG interview banks).
2. **Start-to-End Directionality:**
   - Visual layout flows linearly from **Left to Right**:
     - **Stage 1 (Left, Neon Green `#00ff66`)**: `PollingFeed.js` (Ingestion & Polling Motor).
     - **Stage 2 (Center, Deep Violet `#9d4edd`)**: `pipeline.js` (Pure Data Cleansing Pipeline).
     - **Stage 3 (Right, Electric Cyan `#00f0ff`)**: `Feed.js` (Encapsulated Domain Base & Circuit Breaker).
     - **Foundations (Bottom Ground Plane, Gold `#ffb700`)**: `helpers.js`, `assertions.js`, `validators.js`, `errors.js`.
3. **Physical Container Containment (The Verification Dock):**
   - Test suites (`Feed.test.js`, `pipeline.test.js`, `errors.test.js`) are housed inside a **floating 3D wireframe docking container** suspended above the pipeline.
   - Dotted vertical verification lines connect the tests directly downward into the runtime files they mathematically prove.
4. **Volumetric Cloud Representation:**
   - Files are rendered as **physical cumulus clouds** using dual-layer meshes: an emissive icosahedron core surrounded by procedural radial-gradient particle billows and rotating quantum rings.
5. **Live Disk Synchronization (Zero-Code Evolution):**
   - The visualizer server polls the repository disk every 5 seconds.
   - New files created in `src/`, `utils/`, or `tests/` are automatically discovered, introspected for imports/metrics, and spawned as 3D nodes without manual code changes.
6. **Total Semantic Transparency:**
   - Clicking any cloud exposes:
     - **Execution Lifecycle & State Machine Transitions** (e.g. `IDLE` ➔ `FETCHING` ➔ `CONNECTED` / `DEGRADED`).
     - **Step-by-Step Data Mutation Traces** (showing exact before/after JSON at every pipe stage).
     - **V8 Memory & GC Profiles** (explaining closure retention and private brand checks).
     - **Why It Was Invented / What It Solves** (deep historical engineering context).
     - **Contract & Pseudocode** (interfaces, getters, private fields).
     - **Live Raw Code** (fetched directly from disk).

---

## 3. FILE SYSTEM & CODEBASE TOPOLOGY

```
live_feed_console/
├── package.json               # ESM ("type": "module"), scripts: test, test:watch, visualizer
├── docs/
│   ├── vision.md              # Core engineering philosophy & zero-trust architecture
│   ├── live_console_plan.md   # Master multi-engine curriculum & roadmap (Phases 1 - 6)
│   └── visualizer/
│       ├── index.html         # 3D Main Architecture Cockpit (Three.js WebGL)
│       ├── katas.html         # Dedicated Currying Crucible Lab
│       ├── server.py          # Zero-dependency Python HTTP API server (port 8088)
│       ├── pipeline_graph.json# Directed graph schema with containment zones & semantics
│       └── kata_graph.json    # Language mechanics & arity challenge schema
├── src/
│   └── feeds/
│       ├── Feed.js            # Abstract base class with #private fields & circuit breaker
│       ├── PollingFeed.js     # Concrete async poller with recursive setTimeout & abort
│       ├── pipeline.js        # Pure curried stages (validateSchema, normalizeTimestamps, etc.)
│       └── errors.js          # Telemetry error hierarchy (FeedError, NetworkError, ParseError)
├── utils/
│   ├── helpers.js             # Combinators: pipe, compose, parseJson, capitalize
│   ├── assertions.js          # Invariant guard: assertValid
│   └── validators.js          # Strategy dictionary: VALIDATORS for string, number, array
├── kata/
│   ├── curry.js               # L1–L5 Currying drills (fixed, infinite, valueOf, universal, placeholder)
│   ├── partial_application.js # Partial application vs currying comparison
│   └── test_curry.mjs         # Standalone test runner
└── tests/
    ├── src/feeds/
    │   ├── Feed.test.js       # Vitest BDD tests for Feed abstract invariants & copying
    │   ├── pipeline.test.js   # Vitest tests for pipeline stages & epoch thresholding
    │   └── errors.test.js     # Vitest tests for Error prototype inheritance
    └── utils/
        ├── helpers.test.js    # Tests for pipe, compose, parseJson
        ├── assertions.test.js # Tests for assertValid
        └── validators.test.js # Tests for VALIDATORS rules
```

---

## 4. DEEP SEMANTIC CONCEPTS & HISTORICAL GROUNDING

Any AI interacting with this system must know the deep conceptual rationale behind every component:

### A. Abstract Feed Base (`src/feeds/Feed.js`)
- **`new.target` Guard:**
  - *Why Invented:* JavaScript lacked an `abstract` keyword. ES6 introduced `new.target` to inspect constructor origins.
  - *What It Solves:* Halts direct instantiation `new Feed(...)` with a `TypeError`, guaranteeing only specialized pollers run.
- **Hard Encapsulation (`#private` fields):**
  - *Why Invented:* Replacing leaky `_underscore` conventions with lexical brand checks in V8.
  - *What It Solves:* Complete immutability from outside. Rogue UI code cannot mutate `#status` or wipe `#endpoints`.
- **Defensive Copying at Boundaries:**
  - *Why Invented:* Eliminates array reference aliasing bugs.
  - *What It Solves:* Constructing with `[...endpoints]` and getting with `return [...this.#endpoints]` ensures external mutations never pollute internal state.
- **Circuit Breaker Telemetry:**
  - *Why Invented:* Michael Nygard's *Release It!* (2007).
  - *What It Solves:* Tracks consecutive failure streaks in-place with zero GC allocations, shifting state to `DEGRADED` on threshold breach.

### B. Pure Pipeline Engine (`src/feeds/pipeline.js`)
- **Currying & Unary Composition:**
  - *Why Invented:* Schönfinkel (1924) & Haskell Curry (1930) in combinatory logic.
  - *What It Solves:* Pre-configures validation schemas and feed IDs once, yielding unary functions compatible with `pipe()`.
- **Point-Free Unix Pipes:**
  - *Why Invented:* Ken Thompson & Doug McIlroy (1973 Unix pipes).
  - *What It Solves:* Linear stream processing `parseJson` ➔ `validateSchema` ➔ `normalizeTimestamps` ➔ `enrichFeedMetadata` without temporary variables.
- **Epoch Thresholding Heuristic:**
  - *Why Invented:* Disambiguating POSIX seconds (~1.7e9) from JavaScript milliseconds (~1.7e12).
  - *What It Solves:* Inspects `raw < 10,000,000,000 ? raw * 1000 : raw` to seamlessly normalize heterogeneous APIs.
- **Referential Immutability for React 60 FPS:**
  - *Why Invented:* React's `O(1)` shallow referential comparison (`prevProps !== nextProps`).
  - *What It Solves:* Every stage returns a new shallow copy `{ ...data }`, guaranteeing React hooks (`useSyncExternalStore`, `useMemo`) trigger without deep diffing.

### C. Asynchronous Motor (`src/feeds/PollingFeed.js`)
- **Recursive `setTimeout` vs. `setInterval`:**
  - *Why Invented:* `setInterval` fires blindly on clock ticks, creating request pile-ups when networks lag.
  - *What It Solves:* Recursive `setTimeout` schedules the next poll only *after* the previous request settles, ensuring natural backpressure.
- **Cooperative Cancellation (`AbortController`):**
  - *Why Invented:* WHATWG standard (2017) to cancel in-flight HTTP sockets.
  - *What It Solves:* Calling `stop()` immediately drops open TCP sockets, preventing stale responses from updating state out of order.
- **GC-Safe Interval Identity:**
  - *Why Invented:* Closure leaks in Single Page Applications pinning dead objects in V8 memory.
  - *What It Solves:* Storing `#timerId` directly on the instance and clearing it on `stop()` allows V8 Mark-and-Sweep to reclaim the feed.

---

## 5. COMPLETE REPLICATION & INNOVATION INSTRUCTIONS FOR AI

When another AI model is prompted to work on this visualizer, it should follow this exact execution protocol:

1. **Verify Server & Ports:**
   - The visualizer runs via `python3 docs/visualizer/server.py` on port `8088`.
   - Ensure routes `/` (main pipeline), `/katas.html` (kata lab), and `/api/file-content?path=...` respond with HTTP 200.
2. **Preserve Spatial Architecture:**
   - Always keep the **Left-to-Right linear flow** in `index.html`: `PollingFeed.js` (Left) ➔ `pipeline.js` (Center) ➔ `Feed.js` (Right).
   - Keep the **Verification Dock** suspended in the upper bounding box, and **Foundations** on the lower ground plane.
   - Keep **Katas** strictly on `/katas.html`.
3. **Extend Without Regressions:**
   - As new files are added to `live_feed_console` (e.g. `FeedEventBus.js`, `USGSAdapter.js`, `ReduxStoreEngine.js`):
     - Add them to the corresponding architectural zone in `pipeline_graph.json`.
     - Document their formal contract, pseudocode, state machine transitions, and enabling concepts.
     - Add directional Bezier connection beams to dependent nodes.
4. **Ensure BDD Verification Integrity:**
   - Always run `npx vitest run` in the project root to guarantee all 48+ tests pass with zero errors before concluding any work.
