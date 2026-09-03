# MDN JavaScript Coverage Audit

Unbiased audit of this repository against [MDN JavaScript documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript) coverage. Scope: `src/`, `utils/`, `tests/`, `kata/` — language features only (not browser/Web APIs, Node APIs, or frameworks).

**Last reviewed:** 2026-09-03

---

## Overall score

| Lens | Coverage |
|------|----------|
| Full MDN JS corpus (~500–700 topics) | **~12–19%** *(see methodology — denominator matters)* |
| Production-core JS (~150 topics) | **~30%** *(subjective; no fixed topic list)* |
| Feed-console foundations (what this app needs) | **~38%** *(domain model + pipeline yes; I/O layer missing)* |

---

## Mega-boundaries (rollup)

MDN JavaScript topics grouped into top-level zones:

```
MDN JS 100%
│
├── SYNC (~78% of MDN corpus)          ████░░░░░░░░  24%
├── ASYNC (~8%)                        █░░░░░░░░░░░   2%
├── META (~5%)                         █░░░░░░░░░░░   7%
├── ITERATION PROTOCOL (~4%)           █░░░░░░░░░░░   4%
└── SPECIALIZED (~5%)                  ░░░░░░░░░░░░   0%
```

| Mega-boundary | % of MDN corpus | Coverage | Verdict |
|---------------|-----------------|----------|---------|
| **Sync** | ~78% | **24%** | Strongest area; FP + classes carry it |
| **Async** | ~8% | **2%** | Almost untouched (`Promise.resolve` in one test stub) |
| **Meta** | ~5% | **7%** | Kata only (`valueOf`, incomplete `Symbol` stub) |
| **Iteration protocol** | ~4% | **~0%** | No `Symbol.iterator`, `for...of`, or generators (`forEach`/`reduce` are array callbacks, not the protocol) |
| **Specialized** | ~5% | **0%** | RegExp, Intl, TypedArrays, WeakRef untouched |

---

## Full boundary breakdown

Percentages = topics **meaningfully used** / total MDN topics in that boundary (approximate, consistent methodology).

### Sync boundaries

| # | Boundary | MDN topics (≈) | Used | Coverage |
|---|----------|----------------|------|----------|
| 1 | Statements & control flow | 18 | 4 | **22%** |
| 2 | Operators & expressions | 35 | 10 | **29%** |
| 3 | Primitives & coercion | 20 | 7 | **35%** |
| 4 | Functions & closures | 22 | 13 | **59%** |
| 5 | Scope / `this` / binding | 12 | 2 | **17%** |
| 6 | Objects & properties | 25 | 6 | **24%** |
| 7 | Arrays | 30 | 6 | **20%** |
| 8 | Keyed collections | 16 | 2 | **13%** |
| 9 | Classes & OOP | 18 | 9 | **50%** |
| 10 | Prototypes & inheritance | 10 | 1.5 | **15%** |
| 11 | Iteration & loops | 14 | 1 | **7%** |
| 12 | Strings & text | 20 | 4 | **20%** |
| 13 | Numbers & Math | 15 | 2 | **13%** |
| 14 | Dates & time | 12 | 3 | **25%** |
| 15 | JSON | 5 | 2 | **40%** |
| 16 | Errors & exceptions | 12 | 5 | **42%** |
| 17 | Modules (ESM) | 8 | 3 | **38%** |
| 18 | Modern syntax sugar | 12 | 3 | **25%** |

**Sync subtotal (weighted): ~24%**

#### Sync detail — what is covered vs missing

| Boundary | Covered | Missing |
|----------|---------|---------|
| Statements & control flow | `if`, `throw`, `return` | `for`, `while`, `switch`, `break`, `continue` |
| Operators & expressions | `typeof`, `===`, `!`, `? :`, `+`, `<` | `??`, `?.`, bitwise, `in`, `delete` |
| Primitives & coercion | `string`, `number`, `null`, `undefined` | `BigInt`, `Symbol` (prod), explicit casts |
| Functions & closures | `pipe`, `compose`, curry, HOFs, rest/spread, defaults | `bind`/`call`/`apply`, generators, `async` fns |
| Scope / `this` | Closures, module scope | `this`, `bind`/`call`/`apply` |
| Objects | Literals, spread clone, computed keys, getters | `Object.assign`, `freeze`, descriptors, `keys` |
| Arrays | `forEach`, `reduce`, `reduceRight`, `some`, `push` | `map`, `filter`, `find`, `slice`, `sort`, `flat` |
| Keyed collections | `Set` | `Map`, `WeakMap`, `WeakSet` |
| Classes & OOP | `#private`, getters, `extends`, `new.target`, abstract base | `static`, private methods, static blocks |
| Prototypes | `instanceof`, implicit via `extends` | `Object.create`, direct prototype work |
| Iteration & loops | `forEach` | `for`, `for...of`, `for...in`, `while` |
| Strings | Template literals, `charAt`, `slice`, `trim` | `split`, `replace`, `padStart`, Unicode APIs |
| Numbers & Math | `Number.isNaN`, arithmetic | `Math.*`, `BigInt`, `parseInt`/`parseFloat` |
| Dates | `Date.now()`, `Date.parse()` | `new Date()`, instance getters, formatting |
| JSON | `JSON.parse`, `JSON.stringify` | — (small API; mostly covered) |
| Errors | Custom hierarchy, `try/catch`, `TypeError`, `RangeError` | `finally`, `cause`, `AggregateError` |
| Modules | `import`/`export` (named + default) | Dynamic `import()`, `import.meta`, re-exports |
| Modern syntax | spread/rest, destructuring params, `#private` | `?.`, `??`, top-level await, `using` |

---

### Async boundaries

| # | Boundary | MDN topics (≈) | Used | Coverage |
|---|----------|----------------|------|----------|
| 19 | Promises | 15 | 0.5 | **3%** |
| 20 | async / await | 8 | 0 | **0%** |
| 21 | Timers & task queue | 10 | 0 | **0%** |
| 22 | Fetch / network (lang-adjacent) | 6 | 0 | **0%** |

**Async subtotal: ~2%**

Only async touchpoint: `Promise.resolve([])` in `tests/src/feeds/Feed.test.js` as a fetch stub.

---

### Meta boundaries

| # | Boundary | MDN topics (≈) | Used | Coverage |
|---|----------|----------------|------|----------|
| 23 | Proxy & Reflect | 8 | 0 | **0%** |
| 24 | Symbol (advanced) | 5 | 0.5 | **10%** |
| 25 | Coercion hooks | 4 | 1 | **25%** |
| 26 | Function introspection | 3 | 1 | **33%** |

**Meta subtotal: ~7%**

Evidence: `kata/curry.js` (`valueOf`, `fn.length`, incomplete `Symbol` placeholder curry).

---

### Iteration protocol boundaries

| # | Boundary | MDN topics (≈) | Used | Coverage |
|---|----------|----------------|------|----------|
| 27 | Iterator protocol | 6 | 0 | **0%** |
| 28 | Generators | 6 | 0 | **0%** |
| 29 | Async iterators | 4 | 0 | **0%** |

**Iteration protocol subtotal: ~0%** — array callback methods (`forEach`/`reduce`) are not the iterator protocol.

---

### Specialized boundaries

| # | Boundary | MDN topics (≈) | Used | Coverage |
|---|----------|----------------|------|----------|
| 30 | RegExp | 25 | 0 | **0%** |
| 31 | Intl (i18n) | 20 | 0 | **0%** |
| 32 | Binary data / TypedArrays | 20 | 0 | **0%** |
| 33 | Memory & resources | 10 | 0 | **0%** |
| 34 | Strict mode & directives | 4 | 0.5 | **13%** |

**Specialized subtotal: ~0%**

Strict mode: implicit via ESM modules (`"type": "module"` in `package.json`).

---

## Coverage heatmap

```
BOUNDARY                          COVERAGE
─────────────────────────────────────────────
Functions & closures              ████████████░░░░░░░░  59%
Classes & OOP                     ██████████░░░░░░░░░░  50%
Errors & exceptions               ████████░░░░░░░░░░░░  42%
JSON                              ████████░░░░░░░░░░░░  40%
Modules (ESM)                     ███████░░░░░░░░░░░░░  38%
Primitives & coercion             ███████░░░░░░░░░░░░░  35%
Operators & expressions           ██████░░░░░░░░░░░░░░  29%
Dates & time                      █████░░░░░░░░░░░░░░░  25%
Modern syntax                     █████░░░░░░░░░░░░░░░  25%
Objects & properties              █████░░░░░░░░░░░░░░░  24%
Statements & control flow         ████░░░░░░░░░░░░░░░░  22%
Arrays                            ████░░░░░░░░░░░░░░░░  20%
Strings & text                    ████░░░░░░░░░░░░░░░░  20%
Scope / this / binding            ███░░░░░░░░░░░░░░░░░  17%
Prototypes                        ███░░░░░░░░░░░░░░░░░  15%
Keyed collections (Map/Set)       ███░░░░░░░░░░░░░░░░░  13%
Numbers & Math                    ███░░░░░░░░░░░░░░░░░  13%
Meta-programming                  ██░░░░░░░░░░░░░░░░░░   7%
Iteration & loops                 █░░░░░░░░░░░░░░░░░░░   7%
Iteration protocol                █░░░░░░░░░░░░░░░░░░░   4%
Promises                          █░░░░░░░░░░░░░░░░░░░   3%
async/await                       ░░░░░░░░░░░░░░░░░░░░   0%
Timers & scheduling               ░░░░░░░░░░░░░░░░░░░░   0%
RegExp                            ░░░░░░░░░░░░░░░░░░░░   0%
Intl                              ░░░░░░░░░░░░░░░░░░░░   0%
Binary / TypedArrays              ░░░░░░░░░░░░░░░░░░░░   0%
Memory / WeakRef / using          ░░░░░░░░░░░░░░░░░░░░   0%
```

---

## Code evidence (strongest areas)

### Classes & OOP — `src/feeds/Feed.js`

- Private fields (`#id`, `#name`, …)
- Read-only getters
- `new.target` abstract-base guard
- Defensive copying (`[...endpoints]`)
- Subclass extension (`PollingFeed extends Feed`)

### Functions & closures — `utils/helpers.js`, `src/feeds/pipeline.js`

- `pipe` / `compose` combinators
- Curried pipeline stages (`validateSchema`, `normalizeTimestamps`, `enrichFeedMetadata`)
- `reduce` / `reduceRight`
- Rest/spread in function signatures and calls

### Errors — `src/feeds/errors.js`

- Custom error hierarchy (`FeedError` → `NetworkError`, `ParseError`)
- `super()`, `instanceof` checks in tests

---

## Architecture vs coverage gaps

```
SYNC (24%)          ASYNC (2%)           META (7%)
├── Feed.js ✅       ├── PollingFeed ❌    └── kata/curry.js
├── pipeline.js ✅   ├── fetch ❌
├── helpers.js ✅    ├── setInterval ❌
├── errors.js ✅     └── Promise chains ❌
└── validators.js ✅
```

`src/feeds/PollingFeed.js` is the primary cliff: implementing it should move **Async** from ~2% toward ~40%+ and unlock **Timers**, **Promises**, and **async/await**.

---

## Highest-ROI boundaries to close next

| Priority | Boundary | Expected jump | Where to implement |
|----------|----------|---------------|-------------------|
| 1 | Promises + async/await | 2% → ~40% | `PollingFeed.fetch()` |
| 2 | Timers & scheduling | 0% → ~50% | `PollingFeed.start()` / `stop()` |
| 3 | Iteration & loops | 7% → ~35% | Endpoint fan-out |
| 4 | Arrays (`map`/`filter`) | 20% → ~40% | Response normalization |
| 5 | Modern syntax (`?.`/`??`) | 25% → ~50% | Pipeline null-safety |

---

## Methodology notes

- **"Meaningfully used"** = appears in production or test code with real behavior, not just a comment or unused import.
- **MDN topic counts** are approximate buckets aligned to MDN guide + reference sections, not an exact page count.
- **Percentages are not additive** across rows; mega-boundary rollups are weighted by relative MDN corpus size.
- **Headline % vs boundary tables:** boundary rows sum to ~448 topic-slots with ~87 touched (**~19%**). The **~12%** headline uses a ~700-topic MDN denominator. Both are defensible; they are not the same calculation — do not compare them as if they were.
- **Subjective rows** (production-core, feed-console foundations) have no enumerated topic checklist; treat as directional estimates only.
- Re-run this audit when `PollingFeed`, network I/O, or React integration land — async coverage will shift fastest.

---

## Revision log

| Date | Change |
|------|--------|
| 2026-09-03 | Initial audit — Phase 1 codebase (Feed, pipeline, utils, kata) |
| 2026-09-03 | Adversarial review — fixed iteration-protocol credit, clarified 12% vs 19% denominator, adjusted subjective scores |
