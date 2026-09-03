# Prompt: Complete Practical Interview Coverage (Sync + Async + FE)

Use this as a **copy-paste agent / study brief** to cover **every interview-relevant sync, async, and frontend topic and subtopic** in the `live_feed_console` repo.

**Goal:** Raise **practical interview coverage from ~41% → ~65%+** (headline) and **FE interview loop from ~26% → ~60%+**.

**Current gaps:** Sync **~53% pending** · Async **~95% pending** · DOM/React **100% pending**

**Scope:** `src/`, `utils/`, `kata/`, `tests/`, and (when ready) `src/ui/` or equivalent.

**Out of scope (do not spend time):** Intl, TypedArrays, Proxy/Reflect, WeakRef, Web Workers, Atomics, generators (unless Google-targeted), advanced RegExp, `import.meta`, decorators, BigInt internals.

**Rules:**
1. Every subtopic → code in repo **or** documented MCQ drill in `kata/`.
2. Every `kata/` implementation → `export` + Vitest in `tests/kata/`.
3. Domain features → wire into `Feed`, `PollingFeed`, pipeline, or UI — not orphan demos.
4. Mark progress: `[ ]` not started · `[~]` partial · `[x]` done.
5. Run `npm test` after each boundary.
6. **Complete Part 0 (Sync) before Part 1 (Async).**

---

## Part 0 — Sync JavaScript (~87% weight, ~53% pending → target ~70%+)

Sync boundaries: closures, OOP, ES6+, coercion, arrays, control flow, prototypes, `this`, katas, strings, numbers, errors, modules, patterns.

**Already strong in repo (reinforce, don't skip):** `pipe`/`compose`, curried `pipeline.js`, `Feed` + `#private` + `new.target`, custom errors, `Set`, `parseJson`, Vitest on `src/` + `utils/`.

---

### Tier A — Critical sync gaps (do first)

#### 0.1 `this` binding & method context *(currently ~5%)*

- [ ] `this` in a regular function vs arrow function (lexical `this`)
- [ ] Implicit binding — method call: `obj.fn()`
- [ ] Explicit binding: `fn.call(ctx, ...args)`
- [ ] Explicit binding: `fn.apply(ctx, [args])`
- [ ] `fn.bind(ctx)` and partial application via `bind`
- [ ] `new` binding — `new` creates new `this` (know for interviews)
- [ ] Lost `this` in callbacks (e.g. `const fn = obj.method; fn()`)
- [ ] `this` in nested functions
- [ ] Method borrowing: `Array.prototype.slice.call(arguments)`
- [ ] Implement **`myBind(fn, ctx, ...partialArgs)`** polyfill
- [ ] 5 output-prediction snippets with `this` + arrows

**Deliverables:** `kata/bind_call_apply.js`, `kata/myBind.js`, `tests/kata/myBind.test.js`

---

#### 0.2 Scope, hoisting & TDZ *(currently ~10%)*

- [ ] `var` function-scoped hoisting (declaration hoisted, `undefined` until assignment)
- [ ] `let` / `const` block scope
- [ ] Temporal Dead Zone — access before `let`/`const` declaration
- [ ] Function declaration hoisting vs function expression
- [ ] Hoisting order: `var` vs `function` in same scope
- [ ] Closure + `var` in loop (classic trap) — fix with IIFE or `let`
- [ ] Closure + `let` in loop (correct behavior)
- [ ] Module scope (ESM) vs script scope vs block scope
- [ ] 10 MCQ output-prediction drills (hoisting + closure)

**Deliverables:** `kata/hoisting_mcq.js`, `tests/kata/hoisting.test.js` (for any runnable snippets)

---

#### 0.3 Prototypes & inheritance *(currently ~20%)*

- [ ] Prototype chain concept (`[[Prototype]]`)
- [ ] `obj.__proto__` vs `Constructor.prototype` (know the difference)
- [ ] `Object.create(proto)` for delegation
- [ ] `Object.getPrototypeOf()` / `Object.setPrototypeOf()` (know, don't overuse)
- [ ] `instanceof` and how it walks the chain
- [ ] Manual inheritance: `Child.prototype = Object.create(Parent.prototype)`
- [ ] `super` in classes (done — relate to prototype equivalent)
- [ ] Property shadowing on prototype vs own properties
- [ ] `hasOwnProperty` / `Object.hasOwn`
- [ ] When to use class vs prototype (interview talking points)

**Deliverables:** `kata/prototypes.js`, `tests/kata/prototypes.test.js`

---

#### 0.4 Control flow & loops *(currently ~25%)*

- [ ] `for` (classic indexed loop)
- [ ] `while` / `do...while`
- [ ] `switch` / `case` / `break` / fall-through behavior
- [ ] `break` and `continue` in loops
- [ ] `for...of` over arrays and strings
- [ ] `for...in` on objects (and why not on arrays)
- [ ] `forEach` vs `for...of` (when each applies — `forEach` done)
- [ ] Early `return` from functions inside loops
- [ ] Use `for...of` in `src/feeds/` or `pipeline.js` where idiomatic

**Deliverables:** use loops in production code + tests

---

#### 0.5 Array methods *(currently ~40%)*

**Done:** `reduce`, `reduceRight`, `forEach`, `some`, `push`

**Still cover:**

- [ ] `map` — transform list
- [ ] `filter` — select subset
- [ ] `find` / `findIndex` — first match
- [ ] `every` — all match predicate
- [ ] `flat` / `flatMap` — nested arrays
- [ ] `slice` — non-mutating extract (vs `splice`)
- [ ] `sort` — comparator `(a, b) => a - b`
- [ ] `includes` / `indexOf`
- [ ] Chaining: `.filter().map()`
- [ ] Implement **`myMap`** and **`myFilter`** polyfills

**Deliverables:** refactor `pipeline.js` to use `map`/`filter` where idiomatic; `kata/array_methods.js`, `tests/kata/array_methods.test.js`

---

#### 0.6 Implementation katas — sync utilities *(currently ~8%)*

- [ ] **`debounce(fn, delay)`** — trailing edge
- [ ] **`throttle(fn, limit)`** — leading or trailing
- [ ] **`myBind(fn, ctx, ...partialArgs)`** (see 0.1)
- [ ] **`deepClone(obj)`** — recursive; compare with `structuredClone()`
- [ ] **`deepEqual(a, b)`** — shallow first, then deep (stretch)
- [ ] Export all kata functions; wire Vitest
- [ ] Fix `kata/curry.js`: export `sum3`, `infiniteSum`, `add` (alias `infiniteSum2`), `curry`
- [ ] `tests/kata/curry.test.js`

**Deliverables:** `kata/debounce.js`, `kata/throttle.js`, `kata/deepClone.js`, tests for each

---

### Tier B — Important sync gaps (do second)

#### 0.7 Type coercion & equality *(currently ~45%)*

**Done:** `===`, `typeof`, loose `==` in kata, `valueOf` on `infiniteSum2`

**Still cover:**

- [ ] `==` abstract equality rules (null/undefined, string/number, boolean coercion)
- [ ] `===` strict equality
- [ ] `Object.is()` — `NaN`, `+0` vs `-0`
- [ ] Falsy values: `false`, `0`, `''`, `null`, `undefined`, `NaN`
- [ ] Truthy gotchas: `[]`, `{}`, `'0'`
- [ ] `Symbol.toPrimitive` / `valueOf` / `toString` order (interview MCQ)
- [ ] `Number()` / `String()` / `Boolean()` explicit conversion
- [ ] 10 output-prediction MCQs (coercion)

**Deliverables:** `kata/coercion_mcq.js`

---

#### 0.8 ES6+ syntax *(currently ~68%)*

**Done:** spread/rest, arrow functions, template literals, `const`/`let`, default params, object destructuring in `normalizerFactory` params

**Still cover:**

- [ ] Assignment destructuring — array: `const [a, b] = arr`
- [ ] Assignment destructuring — object: `const { x, y = 2 } = obj`
- [ ] Nested destructuring
- [ ] Rest in destructuring: `const { a, ...rest } = obj`
- [ ] Optional chaining `?.` — property, method, bracket access
- [ ] Nullish coalescing `??` — vs `||`
- [ ] Spread in object merge (reinforce)
- [ ] Computed property names (reinforce — done in pipeline)
- [ ] Short-circuit `&&` / `||` for defaults (and how `??` differs)

**Deliverables:** use `?.` and `??` in `pipeline.js`; destructuring in consumers of `normalizerFactory`

---

#### 0.9 Keyed collections — Map & Set *(currently ~25%)*

**Done:** `Set` for `VALID_STATUSES` in `Feed.js`

**Still cover:**

- [ ] `Map` — `set`, `get`, `has`, `delete`, `size`
- [ ] `Map` vs plain object (keys, iteration, when to use each)
- [ ] `Map` for deduplication / frequency count
- [ ] Iterate `Map` with `for...of` (`.entries()`, `.keys()`, `.values()`)
- [ ] `Set` for unique values — second use case beyond statuses
- [ ] `Array → Set → Array` dedup pattern

**Deliverables:** `Map` in a feed utility (e.g. endpoint dedup) + tests

---

#### 0.10 Objects & copying *(currently ~55%)*

**Done:** literals, spread shallow clone, computed keys, getters in `Feed`

**Still cover:**

- [ ] Shallow copy: `{ ...obj }`, `Object.assign({}, obj)`
- [ ] Deep copy: recursive vs `structuredClone()` (Node 17+)
- [ ] Mutability vs immutability in pipeline (reinforce)
- [ ] `Object.keys`, `Object.values`, `Object.entries`
- [ ] `Object.hasOwn(obj, key)` vs `in` operator
- [ ] Read-only surface via getters (reinforce `Feed` pattern)
- [ ] Optional: `Object.freeze` for config objects (low priority)

**Deliverables:** `utils/clone.js` with `shallowClone` / `deepClone` + tests

---

#### 0.11 Strings — practical *(currently ~50%)*

**Done:** template literals, `charAt`, `slice`, `trim` in `helpers.js` / `validators.js`

**Still cover:**

- [ ] `split(sep)` and `join(sep)`
- [ ] `replace` / `replaceAll` (basic)
- [ ] `startsWith` / `endsWith` / `includes`
- [ ] `toLowerCase` / `toUpperCase`
- [ ] Basic `RegExp.test()` for simple validation (not advanced regex)
- [ ] Template literal expressions (reinforce)

**Deliverables:** `split`/`replace` in a validator or parser helper + tests

---

#### 0.12 Numbers — practical *(currently ~35%)*

**Done:** `Number.isNaN`, arithmetic, `VALIDATORS.number` in `validators.js`

**Still cover:**

- [ ] `parseInt(str, radix)` — always specify radix `10`
- [ ] `parseFloat(str)`
- [ ] `Math.floor`, `Math.ceil`, `Math.round`, `Math.max`, `Math.min`, `Math.abs`
- [ ] `isFinite`, `Number.isFinite`
- [ ] Floating-point gotcha: `0.1 + 0.2 !== 0.3` (interview talking point)
- [ ] Complete `tests/utils/validators.test.js` for number type

**Deliverables:** number validator tests; use `parseInt`/`Math.floor` in `normalizeTimestamps` if relevant

---

#### 0.13 Design patterns — sync *(currently ~40%)*

**Done:** factory (`normalizerFactory`), abstract base (`Feed` + `new.target`)

**Still cover:**

- [ ] **Observer / pub-sub** — `subscribe`, `unsubscribe`, `emit` for feed events
- [ ] **Strategy** — pluggable normalizer per feed type (stretch)
- [ ] **Singleton** — know the pattern; avoid overuse (interview Q&A)
- [ ] Composition over inheritance (talking point with `pipe`)

**Deliverables:** `src/feeds/FeedEventBus.js` or observer on `Feed` + tests

---

### Tier C — Reinforce / polish (already strong, close last gaps)

#### 0.14 Closures & HOF *(currently ~90%)*

**Done:** `pipe`, `compose`, curried pipeline, nested returns in `kata/curry.js`

**Still cover:**

- [ ] Closure-in-loop fix patterns (IIFE, `let`, `forEach` with index)
- [ ] Memoization with closure: `memoize(fn)`
- [ ] Once pattern: `once(fn)`
- [ ] Compose vs pipe order (reinforce with one more multi-step example)

**Deliverables:** `kata/memoize.js`, `kata/once.js`, `tests/kata/memoize.test.js`

---

#### 0.15 Currying & partial application *(currently ~78%)*

**Done:** L1–L4 in `kata/curry.js`, `kata/partial_application.js`, curried pipeline stages

**Still cover:**

- [ ] Export all curry kata functions; fix `test_curry.mjs` / add Vitest
- [ ] Rename or alias `infiniteSum2` → `add`
- [ ] L5 placeholder curry (`curryWithPlaceholder`) — stretch
- [ ] Interview explanation: currying vs partial application
- [ ] `fn.length` arity traps — default params, rest params (MCQ drills in comments)

**Deliverables:** `tests/kata/curry.test.js`

---

#### 0.16 Classes & OOP *(currently ~70%)*

**Done:** `#private`, getters, `extends`, `super`, `new.target`, defensive copy in `Feed.js`

**Still cover:**

- [ ] `static` methods (e.g. `Feed.isValidStatus(status)`)
- [ ] `static` fields (know syntax)
- [ ] `PollingFeed` **sync** surface: constructor, validation, `setStatus` — no `fetch` yet
- [ ] Private methods `#helper()` (know syntax)
- [ ] Abstract method pattern (reinforce — implement `start`/`stop`/`fetch` stubs properly)

**Deliverables:** flesh out `src/feeds/PollingFeed.js` sync API + `tests/src/feeds/PollingFeed.test.js` (sync only)

---

#### 0.17 Error handling *(currently ~70%)*

**Done:** custom hierarchy (`FeedError` → `NetworkError`, `ParseError`), `try/catch` in `parseJson`, `TypeError`/`RangeError`, `instanceof` in tests

**Still cover:**

- [ ] `try` / `catch` / `finally` — cleanup in `finally`
- [ ] Re-throwing: `catch (e) { throw new ParseError(e.message, feedId) }`
- [ ] Throw `NetworkError` from sync HTTP-status checker (mock response object)
- [ ] `feedId` propagation at runtime (not just in tests)

**Deliverables:** `finally` in `parseJson`; sync status checker utility + tests

---

#### 0.18 JSON *(currently ~80%)*

**Done:** `JSON.parse`, `JSON.stringify`, `parseJson` wrapper with `ParseError`

**Still cover:**

- [ ] `JSON.parse` reviver (know signature — optional)
- [ ] `JSON.stringify` replacer + spacing (know for debugging)
- [ ] Safe parse boundary pattern (document — done in `helpers.js`)

**Deliverables:** minimal — mostly complete

---

#### 0.19 Modules — ESM basics *(currently ~60%)*

**Done:** `import` / `export` named + default, `.js` extensions, `"type": "module"`

**Still cover:**

- [ ] Named vs default export conventions (reinforce)
- [ ] Re-export barrel: `export { x } from './x.js'` (know, optional)
- [ ] Cyclic import awareness (talking point)

**Deliverables:** optional `utils/index.js` barrel — low priority

---

#### 0.20 fn.length & coercion tricks *(currently ~60%)*

**Done:** `fn.length` in `curry()`, `valueOf` on `infiniteSum2`, MCQ comments in `kata/curry.js`

**Still cover:**

- [ ] MCQ: `function f(a, b = 2, c) {}` → `f.length === 1`
- [ ] MCQ: `function f(a, ...rest) {}` → `f.length === 1`
- [ ] `add(1)(2)(3) == 6` via `valueOf` (export + test)
- [ ] `Symbol.toPrimitive` variant (stretch)

**Deliverables:** export + fix test harness for Level 3 coercion

---

### Part 0 — Explicitly excluded from sync (do not implement)

- Intl, TypedArrays, ArrayBuffer, WeakRef, Proxy/Reflect
- Generators, `Symbol.iterator`, custom iterables
- Bitwise operators, `void`, `with`, labeled statements
- `Object.defineProperty`, descriptors, `freeze`/`seal` (unless senior prep)
- Advanced RegExp (lookbehind, named groups)
- `import.meta`, dynamic `import`, top-level await
- BigInt, Unicode string internals

---

### Part 0 — Sync completion criteria

| Metric | Target |
|--------|--------|
| Practical interview **sync** coverage | **≥ 70%** (from ~47%) |
| Tier A sync boundaries | all subtopics checked |
| Every `kata/` file | exported + Vitest tests |
| `PollingFeed` | sync API complete (no async required yet) |
| `this`, prototypes, loops, `map`/`filter` | implemented + tested |

### Part 0 — Suggested sync order

```
1. this/bind/call/apply → hoisting MCQs → prototypes
2. loops + map/filter/find → debounce/throttle/deepClone katas
3. Map, ?./??, deepClone utils → observer pattern → PollingFeed sync
4. coercion MCQs → memoize/once → fix curry exports → polish tests
```

---

## Part 1 — Async & event loop (~13% weight, ~95% pending)

**Primary repo deliverable:** `PollingFeed` with `start()`, `stop()`, `fetch()` + full test suite with mocks.

### 1.1 Promise fundamentals
- [ ] Promise states: pending → fulfilled / rejected (settled = either)
- [ ] Executor runs synchronously; `resolve`/`reject` are microtask schedulers
- [ ] `.then(onFulfilled, onRejected)` — both optional; returns new Promise
- [ ] `.catch(onRejected)` — sugar for `.then(null, onRejected)`
- [ ] `.finally(onFinally)` — runs on settle; value passes through
- [ ] Chaining: return value from `then` vs return Promise (adoption)
- [ ] Error propagation down the chain until `catch`
- [ ] Throwing inside `then` → rejected next promise
- [ ] `Promise.resolve(value)` — assimilates thenables
- [ ] `Promise.reject(reason)`
- [ ] `Promise.all(iterable)` — fail-fast; array of results in order
- [ ] `Promise.allSettled(iterable)` — never rejects; `{ status, value|reason }`
- [ ] `Promise.race(iterable)` — first settle wins
- [ ] `Promise.any(iterable)` — first fulfill; `AggregateError` if all reject (know)
- [ ] Anti-pattern: Promise constructor wrapper around already-Promise (know)
- [ ] Implement **`myPromiseAll(tasks)`** kata
- [ ] Implement **`promiseSleep(ms)`** returning Promise

**Deliverables:** `kata/promise_all.js`, `kata/promise_sleep.js`, `tests/kata/promises.test.js`

### 1.2 Callback → Promise → async/await migration
- [ ] Callback hell shape (know why Promises exist)
- [ ] Promise chain equivalent of nested callbacks
- [ ] `async function` always returns a Promise
- [ ] `await` only legal inside `async`
- [ ] `await` on non-Promise wraps with `Promise.resolve`
- [ ] Sequential: `const a = await f(); const b = await g(a);`
- [ ] Parallel: `const [a, b] = await Promise.all([f(), g()])`
- [ ] `try { await ... } catch (e) { ... }` — synchronous catch of rejection
- [ ] `try/finally` with async — `finally` runs before function returns Promise
- [ ] Async arrow functions
- [ ] IIFE: `(async () => { ... })()`
- [ ] Top-level await — know exists in modules (don't need in repo)
- [ ] Unhandled rejection: always `.catch` or `try/catch` on `await`

**Deliverables:** `PollingFeed.fetch()` as `async`; `tests/src/feeds/PollingFeed.test.js`

### 1.3 Event loop (interview MCQ core — 20–30% of async bucket)
- [ ] Call stack — LIFO, one thread
- [ ] Macrotask queue (task queue): `setTimeout`, `setInterval`, I/O, UI events
- [ ] Microtask queue: Promise reactions, `queueMicrotask`, `await` continuations, `MutationObserver` (browser)
- [ ] **Golden rule:** sync to completion → drain **all** microtasks → (optional render) → **one** macrotask → repeat
- [ ] `setTimeout(fn, 0)` is not instant — macrotask after microtasks
- [ ] Microtask queued inside macrotask drains before next macrotask
- [ ] `await null` — code after `await` is microtask
- [ ] `Promise.resolve().then()` vs `setTimeout(0)` ordering
- [ ] Nested `.then` chains scheduling order
- [ ] `queueMicrotask(() => ...)` vs `Promise.resolve().then()`
- [ ] Starvation: infinite microtask loop blocks timers (know)
- [ ] Node vs browser: Node has `process.nextTick` (runs before microtasks — know for fullstack)
- [ ] `requestAnimationFrame` — before next paint, after microtasks (browser — know)

**MCQ drills (implement as commented files with answers):**
- [ ] Puzzle: sync + `setTimeout` + `Promise.then` — 5 variants
- [ ] Puzzle: `async/await` + sync logs — 5 variants
- [ ] Puzzle: microtask inside macrotask — 3 variants
- [ ] Puzzle: `Promise.resolve().then().then()` nesting — 3 variants

**Deliverables:** `kata/event_loop_mcq.js` (15+ puzzles), `docs/mdn_cov/event_loop_answers.md` (optional)

### 1.4 Timers & scheduling
- [ ] `setTimeout(fn, delay, ...args)` — returns timer id
- [ ] `clearTimeout(id)`
- [ ] `setInterval(fn, delay)` — repeating macrotask
- [ ] `clearInterval(id)` on `stop()`
- [ ] Recursive `setTimeout` vs `setInterval` (drift — know)
- [ ] Minimum delay clamping in browsers (~4ms nested — know)
- [ ] Polling pattern: `scheduleNext()` after `await fetch()` completes (not overlapping intervals)
- [ ] Cleanup on unmount / `stop()` — no leaks in tests

**Deliverables:** `PollingFeed.start()` / `stop()` with `setInterval` or recursive `setTimeout`; tests with fake timers (`vi.useFakeTimers()`)

### 1.5 fetch & HTTP (lang-adjacent, universal in FE/FS interviews)
- [ ] `fetch(url, { method, headers, body, signal })` returns Promise
- [ ] `response.ok` (status 200–299)
- [ ] `response.status`, `response.statusText`
- [ ] `await response.json()` — can throw on invalid JSON
- [ ] `await response.text()` for non-JSON error bodies
- [ ] Network failure (offline) vs HTTP 4xx/5xx — different errors
- [ ] Map status → `NetworkError(message, feedId, statusCode)`
- [ ] `AbortController` + `signal` — cancel in-flight on `stop()`
- [ ] Timeout via `AbortSignal.timeout(ms)` or manual `setTimeout` + `abort()` (know both)
- [ ] Multiple endpoints: `Promise.all(endpoints.map(fetchOne))` vs sequential
- [ ] Retry with backoff (stretch): 3 attempts, exponential delay
- [ ] Mock `fetch` in Vitest: `vi.stubGlobal('fetch', ...)`

**Deliverables:** `PollingFeed.fetch()` per endpoint; integration with `normalizerFactory`; `NetworkError` thrown at runtime

### 1.6 Async error handling in feeds
- [ ] `recordFailure(error)` on fetch/parse failure
- [ ] `recordSuccess(latencyMs)` on success — pass real latency
- [ ] `setStatus('FETCHING')` → `'CONNECTED'` / `'DEGRADED'` / `'ERROR'`
- [ ] Consecutive failure threshold → `'DEGRADED'` (design choice)
- [ ] Never let unhandled rejection escape `start()` loop
- [ ] Test: mock 500 → `NetworkError`; mock invalid JSON → `ParseError`

### 1.7 Async testing (Vitest)
- [ ] `await expect(promise).resolves.toBe(x)`
- [ ] `await expect(promise).rejects.toThrow(ErrorClass)`
- [ ] `vi.useFakeTimers()` + `vi.advanceTimersByTimeAsync(ms)`
- [ ] `vi.stubGlobal('fetch', mockFn)`
- [ ] `beforeEach` / `afterEach` restore mocks and timers

**Deliverables:** `tests/src/feeds/PollingFeed.test.js` comprehensive

---

## Part 2 — DOM & browser (~8% weight, 100% pending)

**Prerequisite for Part 3.** Use `jsdom` (already in devDependencies) or minimal HTML fixture.

**Deliverable target:** `src/ui/` or `public/index.html` + `src/ui/dom/` modules.

### 2.1 DOM selection & traversal
- [ ] `document.getElementById(id)`
- [ ] `document.querySelector(css)` — first match
- [ ] `document.querySelectorAll(css)` — NodeList
- [ ] `element.closest(selector)` — up the tree
- [ ] `element.matches(selector)`
- [ ] `parentElement`, `children`, `firstElementChild`, `nextElementSibling`
- [ ] Live vs static NodeList (know difference)

### 2.2 DOM creation & mutation
- [ ] `document.createElement(tag)`
- [ ] `element.textContent` — safe text (prefer over `innerHTML` for user data)
- [ ] `element.innerHTML` — XSS risk (know; don't use for untrusted input)
- [ ] `appendChild`, `removeChild`, `replaceChildren`
- [ ] `element.classList.add/remove/toggle/contains`
- [ ] `element.setAttribute` / `getAttribute` / `dataset` (`data-*`)
- [ ] DocumentFragment for batch inserts (know performance pattern)

### 2.3 Events — core
- [ ] `element.addEventListener(type, handler, options)`
- [ ] `removeEventListener` — same function reference required
- [ ] Options: `{ capture: false, once: true, passive: true }` (know `passive` for scroll)
- [ ] Event object: `event.target` (originating node) vs `event.currentTarget` (listener's node)
- [ ] Bubbling phase: inner → outer
- [ ] Capturing phase: outer → inner (rare; know exists)
- [ ] `event.stopPropagation()` — stop bubble
- [ ] `event.preventDefault()` — e.g. form submit, link navigation
- [ ] `event.stopImmediatePropagation()` (know)

### 2.4 Event delegation (high-frequency interview question)
- [ ] Attach one listener on parent; use `event.target.closest('.item')` to find logical child
- [ ] Why: dynamic lists, fewer listeners, memory
- [ ] Implement: feed list click delegation in UI
- [ ] Test with jsdom: click child, handler on parent fires

**Deliverables:** `src/ui/dom/eventDelegation.js`, `tests/src/ui/eventDelegation.test.js`

### 2.5 Forms & input (common in machine coding)
- [ ] `input.value`, `change` vs `input` events
- [ ] `form.addEventListener('submit', e => { e.preventDefault(); ... })`
- [ ] Basic validation feedback in DOM (error message element)
- [ ] `disabled` attribute on submit during async (tie to fetch)

### 2.6 Browser storage & misc
- [ ] `localStorage.setItem/getItem/removeItem` — string only, JSON.stringify for objects
- [ ] `sessionStorage` — tab-scoped (know difference)
- [ ] `storage` event across tabs (know)
- [ ] `requestAnimationFrame(cb)` vs `setTimeout` for visual updates (know)
- [ ] `window.location` / URL basics (know for redirect errors)

### 2.7 Security & performance (interview talking points)
- [ ] XSS: never `innerHTML` with user/feed payload
- [ ] CSP awareness (know concept)
- [ ] Reflow/repaint — batch DOM writes (DocumentFragment, `display:none` trick — know)
- [ ] Debounce user input handlers (wire `kata/debounce.js`)

---

## Part 3 — React patterns (Tier 3, 100% pending)

**Prerequisite:** Part 1 (async fetch) + Part 2 (DOM basics). `@testing-library/react` in devDependencies.

**Deliverable target:** `src/ui/` React app — live feed console.

### 3.1 React fundamentals (interview verbal)
- [ ] Virtual DOM — declarative UI, diff/reconcile (explain without buzzwords)
- [ ] JSX — expressions in `{}`, one parent, `key` on lists
- [ ] Components: function components only (modern standard)
- [ ] Props — read-only, down only
- [ ] State — `useState`, triggers re-render
- [ ] Unidirectional data flow
- [ ] Controlled vs uncontrolled inputs (know both)

### 3.2 useState
- [ ] `const [state, setState] = useState(initial)`
- [ ] Functional update: `setState(prev => prev + 1)` — stale closure fix
- [ ] State object — spread previous: `setState(s => ({ ...s, field }))`
- [ ] Lazy init: `useState(() => expensive())`
- [ ] Lift state up — feed list state in parent
- [ ] Derive display values in render, don't duplicate state

**Deliverables:** `FeedList` component with feed status state

### 3.3 useEffect — polling lifecycle (project-critical)
- [ ] `useEffect(fn, deps)` — runs after paint
- [ ] `useEffect(fn, [])` — mount only
- [ ] `useEffect(fn, [dep])` — when dep changes
- [ ] Cleanup: `return () => { ... }` — runs before re-run and on unmount
- [ ] Pattern: mount → `feed.start()` → cleanup → `feed.stop()`
- [ ] **Stale closure in effect** — wrong `deps`; fix with deps array or refs
- [ ] **Race condition:** fast dep change → abort previous fetch (`AbortController`)
- [ ] Don't call `setState` on unmounted component — cleanup flag or `AbortController`
- [ ] `useEffect` vs `useLayoutEffect` — know when layout measurement needs sync (rare)

**Deliverables:** `usePollingFeed(feed)` hook; tests with RTL + fake timers

### 3.4 useRef
- [ ] `const ref = useRef(initial)` — `.current` mutable, no re-render
- [ ] DOM ref: `ref={inputRef}` + `inputRef.current.focus()`
- [ ] Instance ref: hold `PollingFeed` instance across renders without re-create
- [ ] `prevValue` pattern with ref
- [ ] Ref vs state — when each applies (interview favorite)

### 3.5 useCallback & useMemo
- [ ] `useCallback(fn, deps)` — stable function reference for child `memo` / effect deps
- [ ] `useMemo(() => compute(), deps)` — cache expensive derive
- [ ] **Don't overuse** — interviewers ask when NOT to use
- [ ] Wire `useCallback` for debounced search handler
- [ ] `useMemo` for filtered/sorted feed list from props

### 3.6 useContext (stretch)
- [ ] `createContext`, `Provider`, `useContext`
- [ ] Feed registry context: multiple feeds without prop drilling
- [ ] Context + `useReducer` for complex state (know pattern)

### 3.7 useReducer (stretch)
- [ ] `useReducer(reducer, initialState)` — `(state, action) => newState`
- [ ] Feed status machine: IDLE → FETCHING → CONNECTED | ERROR
- [ ] When reducer vs `useState` (complex transitions)

### 3.8 List rendering & keys
- [ ] `items.map(item => <Row key={item.id} ... />)`
- [ ] **Key must be stable unique id** — not array index for reorderable lists
- [ ] Key on outermost element in map callback
- [ ] Empty state UI

### 3.9 Conditional rendering
- [ ] `condition && <Component />`
- [ ] Ternary for if/else UI
- [ ] Early return `if (loading) return <Spinner />`
- [ ] Error state: `lastError` display from feed

### 3.10 React performance (interview Q&A)
- [ ] `React.memo(Component)` — shallow prop compare
- [ ] Why inline `onClick={() => ...}` breaks `memo` (new function each render)
- [ ] Virtualization for long feed lists (know `react-window` — don't implement unless asked)
- [ ] Re-render causes: state/props/context change in self or parent

### 3.11 Error boundaries (know — class only)
- [ ] `componentDidCatch` / `getDerivedStateFromError` pattern
- [ ] What error boundaries don't catch (async, event handlers — know)
- [ ] Optional: minimal class error boundary wrapper

### 3.12 Testing React (RTL)
- [ ] `render(<App />)`
- [ ] `screen.getByRole`, `getByText`, `getByLabelText` — query priority
- [ ] `userEvent.click`, `userEvent.type`
- [ ] `waitFor`, `findBy*` for async UI
- [ ] Mock `fetch` / mock `PollingFeed` at module boundary
- [ ] Test: loading → data displayed → error state

**Deliverables:** `src/ui/App.jsx`, `FeedCard.jsx`, `usePollingFeed.js`, `tests/src/ui/*.test.jsx`

---

## Part 4 — Cross-cutting interview drills (all boundaries)

### 4.1 Live coding rapid-fire (implement any on whiteboard timing)
- [ ] Flatten nested array (recursive / `flat(Infinity)`)
- [ ] Group by property (`reduce` or `Map`)
- [ ] Unique values (`Set`)
- [ ] Curry (done)
- [ ] Compose functions (done)
- [ ] Flatten object with dot keys (stretch)
- [ ] LRU cache (stretch senior)

### 4.2 System design verbal (tie to this repo)
- [ ] How polling differs from WebSockets (when each)
- [ ] Idempotent normalization pipeline (done — explain)
- [ ] Immutable state updates for React perf
- [ ] Backoff on repeated `NetworkError`
- [ ] Multi-feed concurrency without blocking UI thread

### 4.3 TypeScript awareness (optional — not scored in JS prompt)
- [ ] Know TS is often expected; JS fundamentals transfer
- [ ] Basic types: `string`, interfaces for `Feed`, `NormalizedEvent`

---

## Part 5 — Repo integration checklist (end-to-end)

Wire every boundary into the **live feed console** vertical slice:

```
[ ] utils/ + kata/     → sync + async primitives tested
[ ] src/feeds/         → Feed, PollingFeed, pipeline, errors, event bus
[ ] tests/src/feeds/   → unit + integration with mock fetch
[ ] src/ui/            → React app consuming feeds
[ ] tests/src/ui/      → RTL tests
[ ] docs/mdn_cov/      → update practical_cov.md scores after each part
```

### Acceptance tests (manual)
- [ ] App loads, shows feed cards
- [ ] Polling updates metrics (`lastLatencyMs`, `status`)
- [ ] Invalid endpoint shows error state
- [ ] Stop/unmount cleans timers and aborts fetch
- [ ] Normalized events pass through `normalizerFactory`

---

## Completion criteria by score

| Milestone | Parts complete | Target practical % | Target FE loop % |
|-----------|----------------|--------------------|------------------|
| Sync complete (Part 0) | Part 0 | ~48–50% | ~28% |
| Async + PollingFeed | Part 1 | ~55–58% | ~35% |
| DOM | Part 2 | ~58% | ~42% |
| React UI | Part 3 | ~60–65% | ~55–65% |
| Drills + integration | Part 4–5 | ~65%+ | ~65%+ |

---

## Suggested schedule

| Week | Focus |
|------|--------|
| 1–2 | **Part 0 Tier A** — `this`/bind, hoisting, prototypes, loops, arrays, sync katas |
| 3 | **Part 0 Tier B+C** — coercion, ES6 gaps, Map, patterns, curry exports, PollingFeed sync |
| 4 | Part 1.1–1.3 Promises + event loop MCQs |
| 5 | Part 1.4–1.7 PollingFeed async + fetch + Vitest mocks |
| 6 | Part 2 DOM + event delegation |
| 7 | Part 3 React hooks + polling UI |
| 8 | Part 4–5 integration, polish, update `practical_cov.md` |

---

## Agent session opener (copy this)

```
Read docs/mdn_cov/practical_cov.md and docs/mdn_cov/post_sync_coverage_prompt.md.

Implement the next unchecked subtopics in order:
1. Part 0 Sync (Tier A → B → C) — complete before any async
2. Part 1 async/event loop — PollingFeed.fetch() + event_loop_mcq.js
3. Part 2 DOM, then Part 3 React

Rules: export all kata, Vitest for everything, wire into live_feed_console domain,
run npm test after each boundary, update practical_cov.md revision log when done.
Do not implement trimmed-out topics (Intl, Proxy, generators, etc.).
```

---

## Revision log

| Date | Change |
|------|--------|
| 2026-09-03 | Initial post-sync + full FE/async interview prompt |
| 2026-09-03 | Merged full Part 0 sync curriculum (Tier A/B/C, 20 sections) |
