# The Master Plan: Live Feed Console (0 to End)

*Hour-estimated, multi-engine learning lab — aligned with [vision.md](./vision.md), [practical_cov.md](./mdn_cov/practical_cov.md), [post_sync_coverage_prompt.md](./mdn_cov/post_sync_coverage_prompt.md).*

**Legend:** `[x]` done · `[~]` partial · `[ ]` not started  
**Estimation basis:** Solo dev, **8 h focused coding/day**, includes tests + docs per item.  
**Schedule unit:** **hours** and **days** (÷ 8) — not calendar weeks.

---

## 🧠 Design philosophy (updated)

Vision said *"No magic — native JS first."* That still holds as the **default path**.

This project is also a **staff-engineering comparative lab**: the same `NormalizedMetricEvent` contract, multiple **pluggable engines** behind stable ports. You learn native internals *and* industry stacks (Redux, TanStack Query, etc.) without forking the repo.

```
                    ┌─────────────────────────────────────┐
                    │     NormalizedMetricEvent (contract) │
                    └──────────────────┬──────────────────┘
                                       │
              ┌────────────────────────┼────────────────────────┐
              ▼                        ▼                        ▼
     ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
     │ Pipeline (pure) │    │  Polling motor  │    │   State engine   │
     │  always shared  │    │  (swappable)    │    │   (swappable)    │
     └─────────────────┘    └─────────────────┘    └─────────────────┘
              │                        │                        │
              │            native fetch │ RTK Query │ TanStack Q   │
              │                        │                        │
              └────────────────────────┴────────────────────────┘
                                       │
                         ┌─────────────┴─────────────┐
                         ▼                           ▼
                  Vanilla DOM UI              React 19 UI
                  (Phase 3)                   (Phase 4)
```

**Invariant (never swap):** `pipe` → `normalizerFactory` → validated immutable events.  
**Swappable (lab switches):** how polls run, how state is stored, how UI subscribes.

---

## 🔀 Engine matrix & routes

| Switch | Options | What you learn | Route / selector |
|--------|---------|----------------|------------------|
| **STATE_ENGINE** | `native` · `context` · `zustand` · `redux` | External store vs Redux patterns | `?state=native` or `/lab/state/:engine` |
| **ASYNC_ENGINE** | `polling-feed` · `tanstack-query` · `rtk-query` | Manual polling vs cache libraries | `?async=polling-feed` |
| **UI_RENDERER** | `vanilla` · `react` | DOM vs React 19 | `/` vanilla Phase 3 · `/app` React Phase 4 |
| **PIPELINE_EXEC** | `main` · `worker` | Main thread vs Worker | `?pipeline=worker` (Phase 5) |
| **REACTIVITY** | `subscribe` · `proxy` | EventBus vs Proxy store | Phase 5 |

**Staff pattern:** `src/engines/contracts/` defines ports; each implementation lives in `src/engines/{native,redux,react-query,...}/`.  
**Lab shell:** `src/lab/EngineSwitcher.jsx` + `localStorage` persistence + query-param override.  
**Tests:** contract tests run against **every** engine implementation (same inputs → same `NormalizedMetricEvent`).

### Why Redux / React Query were "deferred" before — and why they're back

| Library | Was deferred because | Now included as |
|---------|---------------------|-----------------|
| **Redux / RTK** | Vision "no magic"; interview needs native store understanding first | **Alternate STATE_ENGINE** — implements same `StateEnginePort` |
| **TanStack Query** | Polling must be understood via `setInterval` + `fetch` first | **Alternate ASYNC_ENGINE** — `refetchInterval` wraps same pipeline |
| **RTK Query** | Same as above | **Alternate ASYNC_ENGINE** — compare to TanStack |
| **Zustand** | Lighter Redux alternative | **Alternate STATE_ENGINE** — minimal compare |

Native path remains **default** and **must ship first**. Alternates are **Phase 4B+** after native React UI works.

---

## 🔭 Vision alignment

Every phase advances one pillar from [vision.md](./vision.md):

| Pillar | What it means in this repo |
|--------|----------------------------|
| **Bulletproof pipeline** | Raw API data never touches UI — only `normalizerFactory` output |
| **Asynchronous motor** | `PollingFeed` (native) or async engine port owns intervals, abort, telemetry |
| **Decoupled UI** | Engine emits events; DOM/React subscribes — no fetch in components |
| **Zero trust** | `validateSchema`, `ParseError`, `NetworkError` at every boundary |
| **Immutability** | Defensive copies, pure pipeline stages, no in-place mutation |
| **Mathematical proof** | Vitest for every module; katas exported + tested |
| **Pluggable proof** | Redux / TanStack Query as alternate engines — native path stays default |

**Target data sources:** USGS Earthquake · Open-Meteo Weather · CoinGecko Crypto

---

## 📊 Master estimate summary

| Phase | Focus | Remaining h | Days @ 8h | Cumulative days |
|-------|--------|-------------|-----------|-----------------|
| **1** | Engine core (finish partials) | **10** | 1.3 | 1.3 |
| **1.5** | Sync mastery sprint | **68** | 8.5 | 9.8 |
| **2** | Async + PollingFeed | **40** | 5.0 | 14.8 |
| **2.5** | Domain adapters + registry | **21** | 2.6 | 17.4 |
| **3** | Vanilla DOM dashboard | **44** | 5.5 | 22.9 |
| **4A** | React 19 native engine UI | **64** | 8.0 | 30.9 |
| **4B** | Alternate engines lab | **52** | 6.5 | 37.4 |
| **5** | Workers, Proxy, staff ceiling | **36** | 4.5 | 41.9 |
| **6** | Production hardening | **22** | 2.8 | **44.7** |
| | **TOTAL (core + all alternates)** | **~357** | **~45 days** | |

**Already invested (Phase 1 ~70% done):** ~30 h counted separately — not double-counted above.  
**Core path only (skip 4B alternates):** **~305 h → ~38 days @ 8h.**  
**Minimum viable demo (1.5A + 2 + 2.5 + 4A skeleton):** **~158 h → ~20 days.**

---

## 🟢 PHASE 1: Core Data Engine — **10 h remaining**

*~30 h already done. Finish partials + adapters entry.*

| Item | Status | Est. |
|------|--------|------|
| Curry kata export + Vitest | [~] | 2 h |
| Number validator tests complete | [~] | 1 h |
| Map usage (prep for registry) | [~] | 1 h |
| Error `finally` + sync NetworkError path | [~] | 2 h |
| **Engine contracts scaffold** (`StateEnginePort`, `AsyncEnginePort`, `NormalizedMetricEvent` type) | [ ] | 3 h |
| Feed normalizer stubs (USGS/weather/crypto configs started) | [ ] | 1 h |

**Exit criteria:** contracts folder exists; all tests green; partials closed.

### Topics & subtopics

- [x] **Project Scaffolding:** Node modules, `package.json`, ESM (`"type": "module"`), explicit `.js` import paths.
- [x] **Testing Architecture:** Vitest, isolated test suites under `tests/`.
- [x] **Pure Functions & Immutability:** `pipe`, `compose`, no shared mutation in pipeline stages.
- [x] **Higher-Order Functions (HOFs):** Unary stages (`validateSchema`, `normalizeTimestamps`, `enrichFeedMetadata`).
- [~] **Currying & Partial Application:** Pipeline is curried; `kata/curry.js` L1–L4 written but **not exported / not in Vitest**; `partial_application.js` is a stub.
- [x] **Object-Oriented Programming:** ES6 classes, getters, `extends` / `super` in error hierarchy.
- [x] **Encapsulation:** Private fields (`#id`) and defensive copying (`[...endpoints]`).
- [x] **Abstract Classes:** `new.target` guard on `Feed` — cannot instantiate base directly.
- [x] **Custom Error Telemetry:** `FeedError` → `NetworkError`, `ParseError`; `instanceof` in tests.
- [~] **Error handling depth:** `try/catch` in `parseJson` only — no `finally`, no runtime `NetworkError` throws yet.
- [x] **JSON Serialization:** `parseJson`, `JSON.stringify` in tests.
- [~] **Keyed Collections:** `Set` for `VALID_STATUSES` — **`Map` not used yet**.
- [x] **Validation layer:** `VALIDATORS` + `assertValid` for string/array types.
- [~] **Number validation:** `VALIDATORS.number` exists — tests may be incomplete.
- [x] **Date normalization:** `Date.now()`, `Date.parse()`, seconds vs ms in `normalizeTimestamps`.
- [x] **ESM modules:** Named + default `import`/`export` across `src/` and `utils/`.
- [~] **Object destructuring:** Used in `normalizerFactory` params — assignment destructuring not used elsewhere.
- [ ] **Engine contracts scaffold:** `StateEnginePort`, `AsyncEnginePort`, `NormalizedMetricEvent` type in `src/contracts/`.
- [ ] **Feed-specific normalizers:** Per-source configs for USGS, Open-Meteo, CoinGecko (`normalizerFactory` instances + tests).

---

## 🟡 PHASE 1.5: Sync Mastery — **68 h**

*Detail: [post_sync_coverage_prompt.md](./mdn_cov/post_sync_coverage_prompt.md) Part 0.*

### Tier A — **36 h**

| Block | Est. |
|-------|------|
| `this` / bind / call / apply + `myBind` + tests | 8 h |
| Hoisting / TDZ + 10 MCQs | 4 h |
| Prototypes + tests | 6 h |
| Control flow & loops (use in repo) | 4 h |
| Array methods + `myMap`/`myFilter` + pipeline refactor | 6 h |
| Utility katas: debounce, throttle, deepClone, memoize, once | 8 h |

### Tier B — **24 h**

| Block | Est. |
|-------|------|
| Coercion MCQs + `Object.is` | 4 h |
| `?.` / `??` / destructuring in pipeline | 3 h |
| Map + `utils/clone.js` | 4 h |
| Strings + numbers practical | 4 h |
| **Observer `FeedEventBus`** (native engine backbone) | 5 h |
| **`PollingFeed` sync shell** + tests | 4 h |

### Tier C — **8 h**

| Block | Est. |
|-------|------|
| Static methods, `#private` method, curry Vitest, `finally` | 8 h |

**Exit criteria:** Sync interview coverage ≥ 70%; EventBus emits; PollingFeed constructable.

### Topics & subtopics — Tier A (Critical)

- [ ] **Execution Context (`this`):** Implicit, explicit, arrow lexical `this`, lost-`this` traps, `new` binding.
- [ ] **Context Binding:** `call`, `apply`, `bind`; method borrowing (`Array.prototype.slice.call`).
- [ ] **Polyfills (Part 1):** Custom `myBind` + Vitest (`kata/myBind.js`).
- [ ] **Scope Mechanics:** Hoisting, TDZ, `var` vs `let`/`const`, block vs module scope.
- [ ] **Hoisting MCQs:** 10 output-prediction drills (`kata/hoisting_mcq.js`).
- [ ] **Control Flow & Loops:** `for`, `while`, `do...while`, `switch`, `break`/`continue`, `for...of`, `for...in` (objects).
- [ ] **Advanced Array Iteration:** `map`, `filter`, `find`, `findIndex`, `every`, `flat`, `flatMap`, `slice`, `sort`, `includes`.
- [ ] **Array Polyfills:** `myMap`, `myFilter` + refactor `pipeline.js` to use `map`/`filter` where idiomatic.
- [ ] **Prototypes:** `[[Prototype]]`, `Object.create`, `instanceof` walk, manual inheritance, `Object.hasOwn`.
- [ ] **Utility Katas:** `deepClone`, `debounce`, `throttle`, `memoize`, `once` — all exported + Vitest.
- [ ] **Curry kata wiring:** Export `sum3`, `infiniteSum`, `add`, `curry`; fix `test_curry.mjs`; add `tests/kata/curry.test.js`.

### Topics & subtopics — Tier B (Important)

- [ ] **Type Coercion & Equality:** `==` vs `===`, `Object.is`, falsy/truthy, `ToPrimitive` / `valueOf` MCQs (`kata/coercion_mcq.js`).
- [ ] **Modern ES6+ Syntax:** `?.`, `??`, assignment destructuring (array + object + rest) in pipeline.
- [ ] **Advanced Objects:** `Map` for endpoint dedup / event frequency; `Object.keys/values/entries`, `Object.assign`.
- [ ] **Copy utilities:** `utils/clone.js` — shallow vs deep (`structuredClone` comparison).
- [ ] **Strings (practical):** `split`, `join`, `replace`, `startsWith`/`endsWith`, basic `RegExp.test()` for URL sanity.
- [ ] **Numbers (practical):** `parseInt(s, 10)`, `parseFloat`, `Math.floor/max/min`; float precision MCQ.
- [ ] **Design pattern — Observer:** `FeedEventBus` or `Feed.subscribe` / `emit` — **required for decoupled UI**.
- [ ] **Design pattern — Strategy:** Pluggable normalizer per feed type (stretch).
- [ ] **`PollingFeed` sync shell:** Constructor, validation, `setStatus` — **no `fetch` yet**; Vitest sync tests.

### Topics & subtopics — Tier C (Polish)

- [ ] **Static class methods:** e.g. `Feed.isValidStatus(status)`.
- [ ] **Private methods:** `#helper()` syntax on `Feed` (know + one use).
- [ ] **JSON depth:** `JSON.stringify` replacer for debug logging (optional).
- [ ] **fn.length MCQs:** Default params and rest param arity traps (in `kata/curry.js` comments → tested).
- [ ] **Errors — `finally`:** Cleanup in `parseJson` or sync status checker.
- [ ] **Sync `NetworkError` path:** Throw from HTTP status checker on mock response object (pre-`fetch`).

---

## 🔴 PHASE 2: Async Bridge — **40 h**

| Block | Est. |
|-------|------|
| Event loop theory + 15 MCQ puzzles | 6 h |
| Promise katas (`myPromiseAll`, `promiseSleep`) | 4 h |
| **Native `PollingFeed`**: timers, abort, fetch, normalize | 14 h |
| State machine + telemetry + degraded threshold | 4 h |
| Vitest fake timers + mock fetch suite | 8 h |
| Integration test: full poll cycle | 4 h |

**Exit criteria:** `PollingFeed` is reference **ASYNC_ENGINE=native** implementation.

### Topics & subtopics — Event loop & promises

- [ ] **The Event Loop:** Call stack, Web APIs, microtask vs macrotask queues.
- [ ] **Event Loop MCQs:** 15+ ordering puzzles (`kata/event_loop_mcq.js`).
- [ ] **Promises — core:** States, `.then`/`.catch`/`.finally`, chaining, error propagation.
- [ ] **Promises — static:** `Promise.all`, `allSettled`, `race`, `resolve`, `reject`.
- [ ] **Promise katas:** `myPromiseAll`, `promiseSleep` + Vitest.
- [ ] **Async / Await:** Sequential vs parallel `await`, `try/catch/finally` around `await`.
- [ ] **Unhandled rejections:** Every async path caught — no leaks from `start()`.

### Topics & subtopics — Polling motor (native async engine)

- [ ] **Timers:** `setInterval` or recursive `setTimeout`; store timer id on instance.
- [ ] **Timer cleanup:** `clearInterval` / `clearTimeout` in `stop()` — **GC-safe interval identity**.
- [ ] **Vitest fake timers:** `vi.useFakeTimers()` + `advanceTimersByTimeAsync` in tests.
- [ ] **Garbage Collection awareness:** Mark-and-sweep; no orphaned intervals or closures holding dead feeds.
- [ ] **AbortController:** Cancel in-flight `fetch` on `stop()` / unmount; `signal` passed to `fetch`.
- [ ] **Fetch timeout:** `AbortSignal.timeout(ms)` or manual abort pattern.
- [ ] **No overlapping polls:** Schedule next fetch after previous completes (avoid pile-up).

### Topics & subtopics — Network & feed lifecycle

- [ ] **Network — `fetch`:** GET per endpoint, `response.ok`, `response.json()` / `response.text()`.
- [ ] **HTTP → `NetworkError`:** Map status codes with `feedId` + `statusCode` at runtime.
- [ ] **Multi-endpoint concurrency:** `Promise.all` over `feed.endpoints`.
- [ ] **Retry with backoff:** 3 attempts on transient failure (stretch).
- [ ] **`PollingFeed.fetch()`:** Wire `normalizerFactory` on success; never return raw API shape.
- [ ] **State machine:** `IDLE` → `FETCHING` → `CONNECTED` / `DEGRADED` / `ERROR` via `setStatus`.
- [ ] **Telemetry hooks:** `recordSuccess(latencyMs)`, `recordFailure(error)`, `consecutiveFailures` threshold → `DEGRADED`.
- [ ] **Mock `fetch` in Vitest:** `vi.stubGlobal('fetch', ...)` — 200, 500, invalid JSON cases.
- [ ] **Integration tests:** Full poll cycle with fake timers + mock network.

---

## 🟠 PHASE 2.5: Domain Adapters — **21 h**

| Block | Est. |
|-------|------|
| `NormalizedMetricEvent` doc + contract tests | 3 h |
| USGS + Open-Meteo + CoinGecko adapters + fixtures | 12 h |
| Feed registry (`Map`) + `startAll`/`stopAll` + snapshots | 4 h |
| Error telemetry ring buffer | 2 h |

### Topics & subtopics

- [ ] **Unified event contract:** Document `NormalizedMetricEvent` fields (`id`, `value`, `status`, `timestamp`, `feedId`, `ingestedAt`).
- [ ] **USGS Earthquake adapter:** `normalizerFactory` config + fixture JSON + tests.
- [ ] **Open-Meteo Weather adapter:** Config + fixture + tests.
- [ ] **CoinGecko Crypto adapter:** Config + tests.
- [ ] **Feed registry:** Map of feed id → `PollingFeed` instance (uses `Map` from Phase 1.5).
- [ ] **Registry API:** `startAll()`, `stopAll()`, per-feed status snapshot (immutable copy).
- [ ] **Error telemetry log:** In-memory ring buffer of `{ feedId, error, timestamp }` for UI (no PII).

---

## 🟣 PHASE 3: Vanilla DOM Dashboard — **44 h**

| Block | Est. |
|-------|------|
| Semantic HTML + a11y live regions + XSS discipline | 6 h |
| DOM feed cards + telemetry panel via **EventBus** | 12 h |
| Event delegation + debounced filter + forms | 8 h |
| CSS grid/flex + dark theme + tokens + motion | 14 h |
| localStorage persist + container queries + focus styles | 4 h |

**UI_RENDERER=vanilla** — shares same engine ports as React later.

### Topics & subtopics — HTML & accessibility

- [ ] **Semantic HTML5:** `main`, `section`, `article`, `header`, live region for feed updates.
- [ ] **Accessibility (a11y):** `aria-live="polite"` for status changes, focus order, contrast basics.
- [ ] **Security — XSS:** Never `innerHTML` with API/feed payload; use `textContent`.

### Topics & subtopics — DOM engine binding

- [ ] **DOM Manipulation:** `createElement`, `appendChild`, `textContent`, `classList`, `dataset`.
- [ ] **DOM queries:** `querySelector`, `querySelectorAll`, `closest`.
- [ ] **Subscribe to engine:** UI listens to `FeedEventBus` — **no fetch in DOM layer**.
- [ ] **Feed card component (vanilla):** Status badge, latency ms, last error, endpoint count.
- [ ] **Error telemetry panel:** Renders ring buffer from registry.

### Topics & subtopics — Events & input

- [ ] **DOM Event Architecture:** Capturing, targeting, bubbling phases.
- [ ] **Event Delegation:** One listener on feed list parent (`eventDelegation.js` + tests).
- [ ] **Debounced search/filter:** Wire `kata/debounce.js` to filter feed list.
- [ ] **Forms:** Add-feed form, `preventDefault`, disable submit during async.

### Topics & subtopics — CSS & layout

- [ ] **CSS Box Model:** `box-sizing: border-box`, margin collapse awareness.
- [ ] **Flexbox:** Feed toolbar, card rows (1D).
- [ ] **CSS Grid:** Dashboard grid for multi-feed layout (2D).
- [ ] **CSS Architecture:** BEM or consistent naming; specificity discipline.
- [ ] **Stacking Contexts:** `z-index`, `isolation` for modals/toasts.
- [ ] **Status semantics:** Color + icon + text (not color alone — a11y).
- [ ] **Dark console theme:** High-contrast terminal aesthetic (product identity).
- [ ] **Responsive layout:** Collapse grid on narrow viewports.

### Topics & subtopics — Browser APIs (light)

- [ ] **localStorage:** Persist feed configs (`JSON.stringify`); validate on load through pipeline.
- [ ] **requestAnimationFrame:** Know vs `setTimeout` for visual updates (interview + perf).

---

## 🔵 PHASE 4A: React 19 — Native Engine (default) — **64 h**

| Block | Est. |
|-------|------|
| Vite + React 19 + Vitest JSX + scripts | 4 h |
| Fundamentals: JSX, controlled forms, portals, refs | 8 h |
| Hooks: state, effect, ref, context, reducer, useId | 12 h |
| Concurrent: useTransition, useDeferredValue, Suspense, lazy | 6 h |
| React 19: useActionState, useOptimistic, useFormStatus, `use()`, metadata | 8 h |
| Components: FeedCard, FeedList, AddFeedForm, TelemetryLog, Dashboard | 16 h |
| **useSyncExternalStore** → native EventBus/registry | 4 h |
| RTL tests (all status paths) | 6 h |

**STATE_ENGINE=native · ASYNC_ENGINE=polling-feed**

### Topics & subtopics — React fundamentals

- [ ] **Vite + React 19 scaffold:** `vite`, `@vitejs/plugin-react`, Vitest JSX, npm scripts.
- [ ] **React Fiber / reconciliation:** Verbal mastery — virtual DOM diff, keys, why lists need stable ids.
- [ ] **Component model:** Function components only; props down, events up.
- [ ] **JSX:** Expressions, fragments, conditional render, list `key={item.id}`.
- [ ] **Controlled forms, portals, refs:** Add-feed form, modal portal, focus refs.

### Topics & subtopics — Hooks (core)

- [ ] **useState:** Functional updates; store **normalized events only**, not raw `fetch` responses.
- [ ] **useEffect:** Mount → `feed.start()`, cleanup → `feed.stop()` + abort; correct deps array.
- [ ] **Stale closure / race fixes:** AbortController when deps change; mounted flag.
- [ ] **useRef:** Hold `PollingFeed` instance; DOM focus refs.
- [ ] **useCallback / useMemo:** Debounced handlers; memoized filtered lists — know when **not** to use.
- [ ] **useContext:** Feed registry context — avoid prop drilling.
- [ ] **useReducer:** Feed status machine mirroring `Feed` states.
- [ ] **useId:** Stable ids for a11y labels.

### Topics & subtopics — Concurrent & React 19

- [ ] **useTransition / useDeferredValue:** Heavy list filter without blocking input.
- [ ] **Suspense + lazy:** Code-split `TelemetryLog` or chart panel.
- [ ] **useActionState / useFormStatus:** Add-feed form submission state.
- [ ] **useOptimistic:** Optimistic feed status before poll confirms.
- [ ] **`use()`:** Read promise/context in render (React 19).
- [ ] **Document metadata API:** Know-only for SPA (title/description via `react-helmet-async` or similar).

### Topics & subtopics — Components & native engine binding

- [ ] **`usePollingFeed(feed)`:** Encapsulates start/stop, normalized data, error, latency.
- [ ] **`useFeedRegistry()`:** Context consumer for all feeds.
- [ ] **`useSyncExternalStore`:** Subscribe React to native `FeedEventBus` / registry — no tearing.
- [ ] **`FeedCard`:** Status, latency, consecutive failures, last error message.
- [ ] **`FeedList`:** Maps registry; empty state.
- [ ] **`TelemetryLog`:** Recent errors from ring buffer.
- [ ] **`ErrorBoundary`:** Class boundary — know it won't catch async/event errors.
- [ ] **React.memo:** Memoized `FeedCard` with stable callback props.
- [ ] **RTL tests:** `render`, `screen`, `userEvent`, `waitFor`, mock feed — loading → connected → error.

---

## 🔵 PHASE 4B: Alternate Engines Lab — **52 h**

*Build only after 4A ships. Each alternate implements the same ports.*

### 4B.1 State engine alternates — **26 h**

| Engine | Work | Est. |
|--------|------|------|
| **Context + useReducer** | `STATE_ENGINE=context` | 6 h |
| **Zustand** | store slice mirroring registry; selector subscriptions | 8 h |
| **Redux Toolkit** | `feedsSlice`, `configureStore`, typed hooks | 12 h |

### 4B.2 Async engine alternates — **18 h**

| Engine | Work | Est. |
|--------|------|------|
| **TanStack Query** | `useQuery` + `refetchInterval`; pipeline in `queryFn` | 10 h |
| **RTK Query** | `createApi` + polling pattern; compare cache behavior | 8 h |

*Note: RTK Query overlaps RTK state — can share store from 4B.1.*

### 4B.3 Lab shell + comparison — **8 h**

| Item | Est. |
|------|------|
| `EngineSwitcher` UI + query params + localStorage | 3 h |
| `/lab` route: side-by-side metrics (re-renders, memory, latency) | 3 h |
| Contract test suite parametrized over all engines | 2 h |

**Interview payoff:** You can explain *when* to use native vs Redux vs React Query with **this repo as evidence**.

### Topics & subtopics — State engine alternates

- [ ] **Context + useReducer:** `STATE_ENGINE=context` — registry in context, dispatch actions for add/remove/start/stop.
- [ ] **Zustand:** Store slice mirroring registry; selector subscriptions; compare re-render count vs context.
- [ ] **Redux Toolkit:** `feedsSlice`, `configureStore`, typed `useAppDispatch` / `useAppSelector`.
- [ ] **Contract tests:** Same registry operations produce identical snapshots across all state engines.

### Topics & subtopics — Async engine alternates

- [ ] **TanStack Query:** `useQuery` + `refetchInterval`; `queryFn` calls `normalizerFactory` only.
- [ ] **RTK Query:** `createApi` + polling; share store with Redux state engine where applicable.
- [ ] **Cache behavior comparison:** Stale time, refetch on focus, deduping — document in `/lab`.

### Topics & subtopics — Lab shell

- [ ] **`EngineSwitcher`:** Query params (`?state=redux&async=tanstack-query`) + `localStorage` persistence.
- [ ] **`/lab` route:** Side-by-side metrics — re-renders, memory, latency per engine.
- [ ] **Parametrized contract suite:** Run all engine pairs against same fixture feeds.

---

## 💀 PHASE 5: Staff Ceiling — **36 h**

| Block | Est. |
|-------|------|
| Web Worker pipeline (`PIPELINE_EXEC=worker`) | 12 h |
| Proxy reactive store (`REACTIVITY=proxy`) | 10 h |
| BroadcastChannel cross-tab sync | 4 h |
| useSyncExternalStore + Worker/Proxy unified | 6 h |
| CSS `@layer` + performance profiling report | 4 h |

### Topics & subtopics

- [ ] **Web Workers:** Run `pipeline.js` normalization off main thread; `postMessage` protocol (`PIPELINE_EXEC=worker`).
- [ ] **Metaprogramming (Proxies):** Reactive store — UI updates on normalized state mutations (`REACTIVITY=proxy`).
- [ ] **WeakMap / WeakRef:** Attach metadata to feed instances without preventing GC.
- [ ] **BroadcastChannel:** Cross-tab feed sync.
- [ ] **useSyncExternalStore:** Subscribe React to Worker/Proxy-backed external store (no tearing).
- [ ] **CSS `@layer`:** Layered stylesheet architecture for the console theme.
- [ ] **Performance profiling:** Measure main-thread time before/after Worker split; document in README.

---

## 🧪 PHASE 6: Production Hardening — **22 h**

| Block | Est. |
|-------|------|
| Keyboard a11y, skip link, screen reader polish | 6 h |
| ESLint + hooks exhaustive-deps + CI | 4 h |
| Lighthouse + documented scores | 4 h |
| Playwright E2E (native + one alternate engine) | 6 h |
| Optional: React Router `/feeds` `/telemetry` `/lab` | 2 h |

### Topics & subtopics

- [ ] **Keyboard a11y:** Skip link, focus trap in modals, screen reader labels on status badges.
- [ ] **ESLint:** `eslint-plugin-react-hooks` exhaustive-deps; CI gate on `npm test` + lint.
- [ ] **Lighthouse:** Document performance, a11y, best-practices scores.
- [ ] **Playwright E2E:** Native engine path + one alternate (e.g. Redux + TanStack Query).
- [ ] **React Router (optional):** `/feeds`, `/telemetry`, `/lab` routes.

---

## 📊 Cross-cutting (every phase)

- [ ] **Coverage audits:** Update [practical_cov.md](./mdn_cov/practical_cov.md) after each phase.
- [ ] **No regression:** `npm test` green before merging any phase.
- [ ] **Kata discipline:** Every `kata/*.js` exported + `tests/kata/*.test.js`.
- [ ] **ESM rule:** All relative imports include `.js` extension.
- [ ] **Engine contract rule:** Alternates implement ports — never bypass `normalizerFactory`.
- [ ] **Live acceptance criteria:**
  - [ ] App runs 1+ hour without memory growth from intervals
  - [ ] Malformed JSON never crashes UI
  - [ ] Invalid feed config rejected at construction
  - [ ] Stop/unmount cleans timers and aborts fetch

---

## 🗺️ Dependency graph (restructured)

```
PHASE 1 ──► 1.5 ──► 2 ──► 2.5 ──► 3 (vanilla)
                              │
                              └──► 4A (React native) ──► 4B (engine lab)
                                        │
                                        └──► 5 ──► 6
```

**Hard rules:**
1. **Pipeline contract is frozen** before 4B.
2. **Native engines** before alternates.
3. **No `fetch` in React** — async engines call pipeline boundary only.
4. Alternates **cannot** bypass `normalizerFactory`.

---

## 📁 Target folder structure (engines)

```
src/
  contracts/
    NormalizedMetricEvent.js
    StateEnginePort.js      # subscribe, getSnapshot, dispatch
    AsyncEnginePort.js      # start, stop, poll, onEvent
  engines/
    native/                 # EventBus + PollingFeed (default)
    context/
    zustand/
    redux/
    tanstack-query/
    rtk-query/
  lab/
    EngineSwitcher.jsx
    EngineComparisonPanel.jsx
  feeds/                    # existing Feed, pipeline, PollingFeed
  ui/
    vanilla/
    react/
```

---

## ✅ Coverage map (topic rollup)

*Baseline scores from [practical_cov.md](./mdn_cov/practical_cov.md) — update after each phase.*

| Corpus | Current | Target after Track B | Target after Track C |
|--------|---------|----------------------|----------------------|
| Practical interview JS (~110 topic-slots) | **~41%** | **~75%** | **~85%** |
| Sync interview boundary | **~47%** | **≥70%** (Phase 1.5 exit) | **≥80%** |
| Async / event loop | **~5%** | **≥70%** (Phase 2 exit) | **≥80%** |
| DOM / vanilla FE | **~0%** | **≥60%** (Phase 3 exit) | **≥70%** |
| React 19 FE | **~0%** | **≥65%** (Phase 4A exit) | **≥75%** |
| Redux / React Query (know + build) | **0%** | know-only | **built** (Phase 4B) |

### Always implemented (by phase)

| Area | Phase |
|------|-------|
| JS sync + async native | 1–2 |
| Multi-engine ports + lab | 1, 4B |
| Vanilla + React 19 UI | 3, 4A |
| Redux + TanStack Query + Zustand | 4B |
| Workers + Proxy | 5 |

### Know-only (no second app)

| Topic | Reason |
|-------|--------|
| RSC / Server Actions | No server in Vite SPA — document in README |
| Next.js App Router | Different deployment model |
| Micro-frontends | Out of scope |

---

## 📅 Your schedule @ 8 h/day (pick a track)

| Track | Phases | Hours | **Days** |
|-------|--------|-------|----------|
| **A — Interview sync+async fast** | 1 → 1.5 → 2 → 2.5 | 139 | **17** |
| **B — MVP console (native only)** | A + 3 + 4A | 247 | **31** |
| **C — Full staff lab (everything)** | B + 4B + 5 + 6 | 357 | **45** |

**If you code 8 h/day without breaks:** Track C ≈ **9 calendar weeks** at 5 days/week — but think in **45 working days**, not "week 10" fluff.

**Suggested day blocks (Track C example):**

| Days | Phase | Deliverable |
|------|-------|-------------|
| 1–10 | 1.5 | Sync katas + EventBus + PollingFeed sync |
| 11–15 | 2 | Live polling native async |
| 16–18 | 2.5 | 3 feed adapters |
| 19–24 | 3 | Vanilla dashboard |
| 25–32 | 4A | React 19 native UI |
| 33–39 | 4B | Redux + React Query + lab switcher |
| 40–44 | 5 | Worker + Proxy |
| 45 | 6 | Lighthouse + E2E |

---

## Revision log

| Date | Change |
|------|--------|
| 2026-09-03 | Initial master plan |
| 2026-09-03 | Vision + coverage alignment; Complete FE + React 19 |
| 2026-09-03 | **Restructure:** hour estimates @ 8h/day, pluggable engine matrix, Phase 4B alternates, lab routes, folder structure |
| 2026-09-03 | **Restore:** per-phase topic & subtopic checklists + coverage rollup table |
