# The Master Plan: Live Feed Console (0 to End)

*A comprehensive map of every technical concept required to build the Tier-1 Live Feed Console — aligned with [vision.md](./vision.md), [practical_cov.md](./mdn_cov/practical_cov.md), and [post_sync_coverage_prompt.md](./mdn_cov/post_sync_coverage_prompt.md).*

**Legend:** `[x]` done · `[~]` partial (exists but incomplete / not wired) · `[ ]` not started

---

## 🔭 Vision alignment (read first)

Every phase must advance one of these pillars from [vision.md](./vision.md):

| Pillar | What it means in this repo |
|--------|----------------------------|
| **Bulletproof pipeline** | Raw API data never touches UI — only `normalizerFactory` output |
| **Asynchronous motor** | `PollingFeed` owns intervals, abort signals, `recordSuccess` / `recordFailure` |
| **Decoupled UI** | Engine emits events; DOM/React subscribes — no fetch logic in components |
| **Zero trust** | `validateSchema`, `ParseError`, `NetworkError` at every boundary |
| **Immutability** | Defensive copies, pure pipeline stages, no in-place mutation |
| **Mathematical proof** | Vitest for every module; katas exported + tested |
| **No magic** | Native JS — no Redux, no lodash, no data-fetch libraries |

**Target data sources (from pipeline design):** USGS Earthquake · Open-Meteo Weather · CoinGecko Crypto

---

## 🟢 PHASE 1: The Core Data Engine (JS Sync Foundations)
*Building the hyper-optimized, mathematically proven backend logic.*

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
- [ ] **Feed-specific normalizers:** Per-source configs for USGS, Open-Meteo, CoinGecko (`normalizerFactory` instances + tests).

---

## 🟡 PHASE 1.5: FAANG Sync Mastery Sprint (JS)
*Closing the ~53% sync interview gap. Complete before Phase 2. Detail: [post_sync_coverage_prompt.md](./mdn_cov/post_sync_coverage_prompt.md) Part 0.*

### Tier A — Critical

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

### Tier B — Important

- [ ] **Type Coercion & Equality:** `==` vs `===`, `Object.is`, falsy/truthy, `ToPrimitive` / `valueOf` MCQs (`kata/coercion_mcq.js`).
- [ ] **Modern ES6+ Syntax:** `?.`, `??`, assignment destructuring (array + object + rest) in pipeline.
- [ ] **Advanced Objects:** `Map` for endpoint dedup / event frequency; `Object.keys/values/entries`, `Object.assign`.
- [ ] **Copy utilities:** `utils/clone.js` — shallow vs deep (`structuredClone` comparison).
- [ ] **Strings (practical):** `split`, `join`, `replace`, `startsWith`/`endsWith`, basic `RegExp.test()` for URL sanity.
- [ ] **Numbers (practical):** `parseInt(s, 10)`, `parseFloat`, `Math.floor/max/min`; float precision MCQ.
- [ ] **Design pattern — Observer:** `FeedEventBus` or `Feed.subscribe` / `emit` — **required for vision “decoupled UI”**.
- [ ] **Design pattern — Strategy:** Pluggable normalizer per feed type (stretch).
- [ ] **`PollingFeed` sync shell:** Constructor, validation, `setStatus` — **no `fetch` yet**; Vitest sync tests.

### Tier C — Polish

- [ ] **Static class methods:** e.g. `Feed.isValidStatus(status)`.
- [ ] **Private methods:** `#helper()` syntax on `Feed` (know + one use).
- [ ] **JSON depth:** `JSON.stringify` replacer for debug logging (optional).
- [ ] **fn.length MCQs:** Default params and rest param arity traps (in `kata/curry.js` comments → tested).
- [ ] **Errors — `finally`:** Cleanup in `parseJson` or sync status checker.
- [ ] **Sync `NetworkError` path:** Throw from HTTP status checker on mock response object (pre-`fetch`).

---

## 🔴 PHASE 2: The Asynchronous Bridge (JS Async)
*Connecting the engine to the outside world via `PollingFeed.js`. Detail: [post_sync_coverage_prompt.md](./mdn_cov/post_sync_coverage_prompt.md) Part 1.*

### Event loop & promises (interview + correctness)

- [ ] **The Event Loop:** Call stack, Web APIs, microtask vs macrotask queues.
- [ ] **Event Loop MCQs:** 15+ ordering puzzles (`kata/event_loop_mcq.js`).
- [ ] **Promises — core:** States, `.then`/`.catch`/`.finally`, chaining, error propagation.
- [ ] **Promises — static:** `Promise.all`, `allSettled`, `race`, `resolve`, `reject`.
- [ ] **Promise katas:** `myPromiseAll`, `promiseSleep` + Vitest.
- [ ] **Async / Await:** Sequential vs parallel `await`, `try/catch/finally` around `await`.
- [ ] **Unhandled rejections:** Every async path caught — no leaks from `start()`.

### Polling motor (vision: memory-safe async)

- [ ] **Timers:** `setInterval` or recursive `setTimeout`; store timer id on instance.
- [ ] **Timer cleanup:** `clearInterval` / `clearTimeout` in `stop()` — **GC-safe interval identity**.
- [ ] **Vitest fake timers:** `vi.useFakeTimers()` + `advanceTimersByTimeAsync` in tests.
- [ ] **Garbage Collection awareness:** Mark-and-sweep; no orphaned intervals or closures holding dead feeds.
- [ ] **AbortController:** Cancel in-flight `fetch` on `stop()` / unmount; `signal` passed to `fetch`.
- [ ] **Fetch timeout:** `AbortSignal.timeout(ms)` or manual abort pattern.
- [ ] **No overlapping polls:** Schedule next fetch after previous completes (avoid pile-up).

### Network & feed lifecycle

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

## 🟠 PHASE 2.5: Domain Feed Adapters (Engine Completion)
*Vision: multi-source ingestion with one unified internal event shape.*

- [ ] **Unified event contract:** Document `NormalizedMetricEvent` fields (`id`, `value`, `status`, `timestamp`, `feedId`, `ingestedAt`).
- [ ] **USGS Earthquake adapter:** `normalizerFactory` config + fixture JSON + tests.
- [ ] **Open-Meteo Weather adapter:** Config + fixture + tests.
- [ ] **CoinGecko Crypto adapter:** Config + tests.
- [ ] **Feed registry:** Map of feed id → `PollingFeed` instance (uses `Map` from Phase 1.5).
- [ ] **Registry API:** `startAll()`, `stopAll()`, per-feed status snapshot (immutable copy).
- [ ] **Error telemetry log:** In-memory ring buffer of `{ feedId, error, timestamp }` for UI (no PII).

---

## 🟣 PHASE 3: The Dashboard (HTML, CSS, Vanilla DOM)
*Rendering the engine before React. Detail: [post_sync_coverage_prompt.md](./mdn_cov/post_sync_coverage_prompt.md) Part 2.*

### HTML & accessibility

- [ ] **Semantic HTML5:** `main`, `section`, `article`, `header`, live region for feed updates.
- [ ] **Accessibility (a11y):** `aria-live="polite"` for status changes, focus order, contrast basics.
- [ ] **Security — XSS:** Never `innerHTML` with API/feed payload; use `textContent`.

### DOM engine binding (vision: dumb UI)

- [ ] **DOM Manipulation:** `createElement`, `appendChild`, `textContent`, `classList`, `dataset`.
- [ ] **DOM queries:** `querySelector`, `querySelectorAll`, `closest`.
- [ ] **Subscribe to engine:** UI listens to `FeedEventBus` — **no fetch in DOM layer**.
- [ ] **Feed card component (vanilla):** Status badge, latency ms, last error, endpoint count.
- [ ] **Error telemetry panel:** Renders ring buffer from registry.

### Events & input

- [ ] **DOM Event Architecture:** Capturing, targeting, bubbling phases.
- [ ] **Event Delegation:** One listener on feed list parent (`eventDelegation.js` + tests).
- [ ] **Debounced search/filter:** Wire `kata/debounce.js` to filter feed list.
- [ ] **Forms:** Add-feed form, `preventDefault`, disable submit during async.

### CSS & layout

- [ ] **CSS Box Model:** `box-sizing: border-box`, margin collapse awareness.
- [ ] **Flexbox:** Feed toolbar, card rows (1D).
- [ ] **CSS Grid:** Dashboard grid for multi-feed layout (2D).
- [ ] **CSS Architecture:** BEM or consistent naming; specificity discipline.
- [ ] **Stacking Contexts:** `z-index`, `isolation` for modals/toasts.
- [ ] **Status semantics:** Color + icon + text (not color alone — a11y).
- [ ] **Dark console theme:** High-contrast terminal aesthetic (product identity).
- [ ] **Responsive layout:** Collapse grid on narrow viewports.

### Browser APIs (light)

- [ ] **localStorage:** Persist feed configs (JSON.stringify); validate on load through pipeline.
- [ ] **requestAnimationFrame:** Know vs `setTimeout` for visual updates (interview + perf).

---

## 🔵 PHASE 4: The Automated UI (React)
*State-driven UI subscribed to the engine — **never raw API in `useState`**. Detail: [post_sync_coverage_prompt.md](./mdn_cov/post_sync_coverage_prompt.md) Part 3.*

### React fundamentals

- [ ] **React Fiber / reconciliation:** Verbal mastery — virtual DOM diff, keys, why lists need stable ids.
- [ ] **Component model:** Function components only; props down, events up.
- [ ] **JSX:** Expressions, fragments, conditional render, list `key={item.id}`.

### Hooks — core

- [ ] **useState:** Functional updates; store **normalized events only**, not raw `fetch` responses.
- [ ] **useEffect:** Mount → `feed.start()`, cleanup → `feed.stop()` + abort; correct deps array.
- [ ] **Stale closure / race fixes:** AbortController when deps change; mounted flag.
- [ ] **useRef:** Hold `PollingFeed` instance; DOM focus refs.
- [ ] **useCallback / useMemo:** Debounced handlers; memoized filtered lists — know when **not** to use.
- [ ] **useContext:** Feed registry context — avoid prop drilling.
- [ ] **useReducer (stretch):** Feed status machine mirroring `Feed` states.

### Custom hooks & components

- [ ] **`usePollingFeed(feed)`:** Encapsulates start/stop, normalized data, error, latency.
- [ ] **`useFeedRegistry()`:** Context consumer for all feeds.
- [ ] **`FeedCard`:** Status, latency, consecutive failures, last error message.
- [ ] **`FeedList`:** Maps registry; empty state.
- [ ] **`TelemetryLog`:** Recent errors from ring buffer.
- [ ] **`ErrorBoundary`:** Class boundary — know it won't catch async/event errors.

### Performance & testing

- [ ] **React.memo:** Memoized `FeedCard` with stable callback props.
- [ ] **List virtualization (know):** `react-window` for 1000+ events — mention, don't require.
- [ ] **RTL tests:** `render`, `screen`, `userEvent`, `waitFor`, mock `fetch` / mock feed.
- [ ] **Test:** loading → connected → error UI states.

---

## 💀 PHASE 5: Staff-Engineer Ceiling (Advanced Architectures)
*Vision endgame from [vision.md](./vision.md) — after Phase 4 ships.*

- [ ] **Web Workers:** Run `pipeline.js` normalization off main thread; postMessage protocol.
- [ ] **Metaprogramming (Proxies):** Reactive store — UI updates on normalized state mutations without manual `setState`.
- [ ] **WeakMap / WeakRef:** Attach metadata to feed instances without preventing GC.
- [ ] **BroadcastChannel:** Cross-tab feed sync.
- [ ] **React Concurrent Mode:** `useTransition` for heavy list updates.
- [ ] **useSyncExternalStore:** Subscribe React to Proxy/Worker-backed external store (no tearing).
- [ ] **CSS `@layer`:** Layered stylesheet architecture for the console theme.
- [ ] **Performance profiling:** Measure main-thread time before/after Worker split.

---

## 📊 Cross-cutting (every phase)

- [ ] **Coverage audits:** Update [practical_cov.md](./mdn_cov/practical_cov.md) after each phase.
- [ ] **No regression:** `npm test` green before merging any phase.
- [ ] **Kata discipline:** Every `kata/*.js` exported + `tests/kata/*.test.js`.
- [ ] **ESM rule:** All relative imports include `.js` extension.
- [ ] **Live acceptance criteria:**
  - [ ] App runs 1+ hour without memory growth from intervals
  - [ ] Malformed JSON never crashes UI
  - [ ] Invalid feed config rejected at construction
  - [ ] Stop/unmount cleans timers and aborts fetch

---

## 🗺️ Phase dependency graph

```
PHASE 1 (engine core) ──► PHASE 1.5 (sync sprint) ──► PHASE 2 (async / PollingFeed)
                                                              │
                                                              ▼
                                                       PHASE 2.5 (adapters)
                                                              │
                         ┌────────────────────────────────────┘
                         ▼
                  PHASE 3 (vanilla DOM dashboard)
                         │
                         ▼
                  PHASE 4 (React UI)
                         │
                         ▼
                  PHASE 5 (Workers, Proxies, concurrent React)
```

**Do not start Phase 2 until Phase 1.5 Tier A is complete.**  
**Do not put `fetch` in React components — only in `PollingFeed`.**

---

## 📅 Suggested timeline

| Weeks | Phase | Outcome |
|-------|-------|---------|
| 1–2 | 1.5 Tier A | `this`, loops, arrays, katas wired |
| 3 | 1.5 Tier B+C + 2.5 start | Observer bus, `PollingFeed` sync, first adapter |
| 4 | 2 | `PollingFeed` async, fake timer tests |
| 5 | 2.5 + 3 | All adapters, vanilla dashboard |
| 6–7 | 4 | React UI + RTL tests |
| 8+ | 5 | Workers + Proxy store (vision finale) |

---

## Revision log

| Date | Change |
|------|--------|
| 2026-09-03 | Initial master plan |
| 2026-09-03 | Aligned with vision.md + coverage prompts; added Phase 2.5, honest partials, missing sync/async/DOM/React items |
