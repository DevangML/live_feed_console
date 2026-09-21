# Option A: live_feed_console → Full 1,175-Row Interview System

**Decision:** Expand the existing polling project to cover ALL concepts through 7 integrated layers.

**Scope:** 247 → ~3,500 lines (React UI, mock server, vanilla widget, tooling, docs)

---

## Current State

```
live_feed_console/
  ├── src/feeds/          (247 LOC — polling engine)
  ├── tests/              (452 LOC — vitest)
  ├── kata/               (practice code)
  ├── docs/               (vision + plan)
  └── utils/              (helpers)
```

**Covers:** Part 3 (JS), Part 5 (Async), Part 11 (Testing), Part 15-16 (Architecture)  
**Missing:** Parts 0-2 (Web/HTML/CSS), Part 6 (Tooling), Part 7-10 (TS/React/a11y/Perf)

---

## 7 Layers to Add (Each ~400-600 LOC)

### Layer 1: React Dashboard UI (Parts 0, 2, 7, 8, 9, 10)

**What:** A real observability dashboard showing live feed events

**Files to create:**
- `src/ui/` — React components (Button, Table, Card, Modal, etc.)
- `src/pages/` — Routes (Dashboard, Events, Alerts, Settings)
- `src/styles/` — CSS (reset, tokens, layout, responsive)
- `src/hooks/` — Custom hooks (useFetch, useLocalStorage, useMediaQuery)

**Concepts:** 
- Parts 0-1: HTML semantic structure
- Part 2: CSS cascade, layout (flexbox/grid), responsive, animations
- Part 7: TypeScript (Props, State, Generics)
- Part 8: React (components, hooks, state, effects, context)
- Part 9: a11y (ARIA, keyboard nav, screen reader)
- Part 10: Performance (memo, lazy, profiler)

**Gate:** App renders events in real time from the feed engine

---

### Layer 2: Mock Server (Part 5, Part 6)

**What:** A Node server that can fail on demand (slow, flaky, 429, CORS errors, malformed)

**Files to create:**
- `mock-server/server.js` — Express setup, routes
- `mock-server/handlers.js` — REST + SSE + WebSocket endpoints
- `mock-server/scenarios/` — Slow, flaky, rate-limited, CORS-hostile modes
- `mock-server/README.md` — How to run different failure modes

**Concepts:**
- Part 5: HTTP status codes, CORS, caching, retries, rate limiting, auth flows
- Part 6: API design, error handling
- Node.js, Express, middleware

**Gate:** Dashboard gracefully handles server in "429 Overload" mode

---

### Layer 3: Vanilla Widget (Parts 1, 3, 4)

**What:** Framework-free embed (like `packages/embed/` in the spec)

**Files to create:**
- `packages/embed/src/` — Vanilla TS widget
- `packages/embed/src/index.ts` — Main export
- `packages/embed/src/ui/` — DOM manipulation, event delegation
- `packages/embed/src/styles/` — BEM, Sass
- `packages/embed/examples/embed.html` — How to include it

**Concepts:**
- Part 1: HTML (semantic, valid structure, accessibility)
- Part 3: JavaScript (closures, event listeners, mutation, patterns)
- Part 4: DOM, Web APIs (querySelector, event delegation, fetch)

**Gate:** The widget tails a live feed on a plain HTML page, no React

---

### Layer 4: TypeScript Depth (Part 7, Part 8)

**What:** Convert + deepen the codebase with TypeScript mastery

**Files to create:**
- Migrate `src/` → strict TypeScript
- `src/types/` — Domain types (Event, Feed, Alert, Metric)
- `src/schema/` — Zod validators
- `src/lib/` — Generic utilities
- `docs/typescript-decisions.md` — ADR 0001: Why strict mode, generics, etc.

**Concepts:**
- Part 7: Strict mode, inference, union/intersection, generics, const assertions
- Part 8: Type-safe React props, custom hooks, context types

**Gate:** Type safety enabled end-to-end

---

### Layer 5: Tooling & Build (Part 6)

**What:** Hand-written, explained build pipeline

**Files to update/create:**
- `package.json` — semver, dev/prod deps (rewrite from scratch, not generated)
- `vite.config.ts` — entry points, plugins, optimization
- `tsconfig.json` — strict, incremental, path aliases
- `.eslintrc.js` — rules with rationale
- `.github/workflows/ci.yml` — GitHub Actions (lint, test, build)
- `docs/build-decisions.md` — Why Vite? Why this tsconfig?

**Concepts:**
- Part 6: Package.json, semver, lockfiles, build tools, linting, CI/CD

**Gate:** `npm run build` produces a deployable artifact under budget

---

### Layer 6: Documentation & ADRs (Parts 15-16)

**What:** The narrative of every design choice

**Files to create:**
- `docs/adr/0001-feed-engine.md` — Why the polling architecture
- `docs/adr/0002-react-choice.md` — Why React for the dashboard
- `docs/adr/0003-typescript.md` — Why strict TypeScript
- `docs/feature-briefs/` — 4 features (live tail, alerts, replay, settings) with system design
- `docs/interview/` — Walkthroughs, debugging method, collaboration stories
- `docs/evidence/` — Performance traces, a11y audits, heap snapshots

**Concepts:**
- Part 15: Design principles (modularity, testability, maintainability)
- Part 16: Feature system design (acceptance criteria, state ownership, error paths)

**Gate:** Every major choice is documented and defensible

---

### Layer 7: Advanced Features (Part 8, Part 10, Part 16)

**What:** Ceiling-test features (view transitions, streaming UI, state sync)

**Optional extensions:**
- Session replay (store events, replay timeline)
- Live filtering + search (lazy evaluation, memoization)
- Multi-tab sync (SharedWorker or BroadcastChannel)
- View transitions (CSS animations on route change)
- Streaming response handling (async generators)

**Gate:** The product feels like a real SPA

---

## Roadmap (7 Sprints × ~1 week each = 7-8 weeks)

| Sprint | Layer | Goal | Rows |
|--------|-------|------|------|
| 0 | Tooling | Hand-written package.json, vite.config, tsconfig | 72 |
| 1 | Vanilla | Framework-free widget, vanilla TS, DOM APIs | 350 |
| 2 | Backend | Mock server, failure modes, HTTP concepts | 180 |
| 3 | React Engine | Components, hooks, routing, basic state | 267 |
| 4 | Machine Coding | Primitives (Button, Table, Modal, etc.), a11y | 180 |
| 5 | TypeScript & Perf | Type safety, React.memo, code splitting, optimization | 120 |
| 6 | ADRs & Narrative | Every design choice documented and defended | 80 |
| 7 | Polish | View transitions, streaming UI, unit + integration tests | 80 |

**Total:** 1,125 rows in code + architecture + design  
**Coverage:** 1,175 syllabus rows (core 1,113 + drills 62)

---

## How the Vault Tracks All This

The Obsidian vault maps every row to a file:

```
Concept row 8 (async/defer) → proves → src/lib/script-loading.ts
Concept row 77 (viewport) → proves → src/pages/index.html + src/styles/responsive.scss
Concept row 267 (React) → proves → src/ui/components/ + docs/adr/0002-react-choice.md
```

At the end of Sprint 7:

```bash
python3 scripts/coverage/build_matrix.py --paths
```

Should report: **578 cited artefacts, 578 present** (every concept row has a file)

---

## Why This Works

1. **Real code:** Not toy examples — a working observability system
2. **Deep concepts:** Each concept is used, not mentioned
3. **Progression:** Vanilla first (Parts 0-4), then React (Parts 7-10)
4. **Architecture:** Designed to teach system design (Parts 15-16)
5. **Defense:** Every decision documented, so you can explain it

---

## Starting Point

1. **Read** `OPTION_A_EXPANSION_PLAN.md` (this file)
2. **Open** your Proton Drive Obsidian vault
3. **Run** `/teach-me console` to get the first playlist brief (Stage 0 = Tooling)
4. **Expand** `package.json` hand-written, learning every dependency
5. **Then** build Layer by Layer

**Time estimate:** 7-8 weeks @ 27 h/week = honest

**Outcome:** A defensible product + evidence of every concept + a narrative

