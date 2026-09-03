# Practical Interview JS Coverage

Interview-focused audit of this repository. Derived from [`README.md`](./README.md) (full MDN audit) by **removing boundaries and subtopics that essentially never appear** in JavaScript interviews for 0–5 YOE frontend / fullstack roles (product companies, FAANG screens, Indian OA — Mettl, TCS, Accenture).

**Scope:** `src/`, `utils/`, `tests/`, `kata/`  
**Last reviewed:** 2026-09-03  
**Ground-truth check:** 2026-09-03 (codebase + 2026 interview sources)

### Score definitions (read before comparing numbers)

| Score | What it measures |
|-------|------------------|
| **~41%** | Weighted average of 10 JS mega-boundaries (DOM excluded from weight denominator) |
| **~38%** | Same boundaries but DOM row included at 0% coverage (8% weight) |
| **~26%** | Full **frontend interview loop** estimate: ~65% of the loop is React/DOM (0% in repo) + ~35% JS fundamentals (~41%) |
| **~48% Mettl** | OA/FP subset only — not full interview loop |

---

## Overall score (pruned corpus)

| Lens | Coverage |
|------|----------|
| Full MDN JS corpus | ~12–19% *(see README — not the target here)* |
| **Practical interview JS corpus (~110 topic-slots)** | **~41%** |
| Mettl / OA-style FP rounds | **~48%** *(code exists; harness not wired)* |
| FAANG JS screen + machine coding | **~30%** |
| Frontend React interview (full loop) | **~26%** *(see score definitions below)* |
| JS-only corpus incl. DOM row at 0% | **~38%** |

---

## What was eliminated (and why)

High-discernment cuts only. If something appears even occasionally in OA trick questions, it was kept.

### Whole boundaries removed

| Removed boundary | Reason |
|------------------|--------|
| **Intl (i18n)** | Role-specific; never in general JS rounds |
| **Binary data / TypedArrays** | Canvas, WASM, low-level roles only |
| **Memory / WeakRef / `using` / FinalizationRegistry** | Senior systems niche; not 3 YOE screen material |
| **Proxy & Reflect** | Rare except staff+ meta-programming rounds |
| **Async iterators / `for await...of`** | Niche; `async/await` covers 99% of interview async |
| **Web Workers / Atomics / SharedArrayBuffer** | Specialized; not standard FE loop |
| **Strict mode directives** | Implicit in modules; never asked as standalone |
| **Module internals** (`import.meta`, dynamic `import`, re-export barrels) | Build-tool trivia, not language interviews |
| **RegExp (advanced)** | Lookbehind, named groups, unicode flags — cut entirely; basic `.test()` kept under Strings |

### Subtopics removed from otherwise-kept boundaries

| Boundary | Kept | Eliminated |
|----------|------|------------|
| **Operators** | `===`, `==`, `typeof`, `!`, `? :`, logical | Bitwise, `void`, `delete` deep dives, comma operator |
| **Statements** | `if`, `for`, `while`, `switch`, `return`, `throw` | `with`, labeled statements, `debugger` |
| **Numbers** | `Number.isNaN`, `parseInt`, basic `Math.floor`/`Math.max` | `BigInt`, full `Math.*` catalogue |
| **Dates** | `Date.now()`, `Date.parse()`, `new Date()` basics | Locale formatting, `Intl.DateTimeFormat`, timezone edge cases |
| **Strings** | Template literals, `slice`, `trim`, `split`, basic RegExp `.test()` | Unicode normalization, `codePointAt`, surrogate pairs |
| **Objects** | Literals, spread, shallow copy, property access | `Object.defineProperty`, descriptors, `freeze`/`seal` (unless senior) |
| **Classes** | `class`, `extends`, `super`, getters, `#private` | Static blocks, private methods (low ask rate) |
| **Errors** | `try/catch`, custom `Error` subclasses, `TypeError`/`RangeError` | `AggregateError`, `error.cause`, `finally` as focus |
| **Keyed collections** | `Map`, `Set` (dedup, frequency) | `WeakMap`, `WeakSet` (occasional mention only — not scored) |
| **Meta / tricks** | `fn.length`, `valueOf`, loose `==` coercion | `Symbol` placeholder curry (Lodash `_` — optional stretch) |
| **Generators** | — | Entire sub-boundary cut (Google occasionally; &lt;5% of 3 YOE loops) |
| **Iteration protocol** | `for...of` over arrays (merged into Loops) | `Symbol.iterator`, custom iterables |

### Explicitly out of scope (not JS language)

DOM APIs, React, CSS, Node internals, bundler config — tracked separately if this repo grows a `src/ui/` layer.

---

## Pruned mega-boundaries

```
INTERVIEW JS 100% (~110 topic-slots in Tier 1+2 tables)
│
├── CLOSURES & FP              ████████████████░░░░  82%  ← blend of HOF 90% + currying 78%
├── OOP / CLASSES              ██████████████░░░░░░  70%
├── ES6+ SYNTAX                █████████████░░░░░░░  68%
├── TYPE SYSTEM / COERCION     █████████░░░░░░░░░░░  45%
├── ARRAYS & COLLECTIONS       ████████░░░░░░░░░░░░  40%
├── CONTROL FLOW               █████░░░░░░░░░░░░░░░  25%
├── PROTOTYPES                 ████░░░░░░░░░░░░░░░░  20%
├── IMPLEMENTATION KATAS       █░░░░░░░░░░░░░░░░░░░   8%
├── ASYNC & EVENT LOOP         █░░░░░░░░░░░░░░░░░░░   5%
├── THIS & BINDING             █░░░░░░░░░░░░░░░░░░░   5%
└── DOM & BROWSER (FE roles)   ░░░░░░░░░░░░░░░░░░░░   0%
```

| Mega-boundary | Interview weight | Your coverage |
|---------------|-------------------|---------------|
| Closures & FP | 17% | **82%** |
| OOP / Classes | 11% | **70%** |
| ES6+ syntax | 11% | **68%** |
| Type system / coercion | 8% | **45%** |
| Arrays & collections | 10% | **40%** |
| Control flow & loops | 6% | **25%** |
| Prototypes | 8% | **20%** |
| Implementation katas | 8% | **8%** |
| Async & event loop | 13% | **5%** |
| `this` & binding | 8% | **5%** |
| DOM & browser *(FE only)* | 8% | **0%** |

**Weighted overall (excl. DOM): ~41%** — weights sum to 100%. DOM row excluded from headline; include it and the score drops to **~38%** for FE-targeted roles.

---

## Boundary breakdown (interview corpus only)

### Tier 1 — asked in most loops

| Boundary | Topics (≈) | Coverage | Covered in repo | Still missing |
|----------|------------|----------|---------------|---------------|
| **Closures & HOF** | 12 | **90%** | `pipe`, `compose`, pipeline factories, nested returns | Closure-in-loop MCQ drills |
| **Currying / partial application** | 8 | **78%** | `kata/curry.js` L1–L4, `kata/partial_application.js`, curried pipeline | L5 stub; `infiniteSum2` not exported as `add`; `kata/curry.js` has **no exports** |
| **Classes & OOP** | 10 | **70%** | `Feed`, `#private`, getters, `extends`, `new.target` | `PollingFeed` is an empty shell; no `static` |
| **ES6+ syntax** | 10 | **68%** | spread/rest, arrows, templates, `const`/`let`, default params, **object destructuring** in `normalizerFactory` | `?.`, `??`; no assignment destructuring |
| **Array methods** | 12 | **40%** | `reduce`, `reduceRight`, `forEach`, `some`, `push` | `map`, `filter`, `find`, `flat` |
| **Type coercion & equality** | 8 | **45%** | `===` in prod; `==`, `valueOf` in kata | `Object.is`, abstract equality MCQs |
| **Error handling** | 6 | **70%** | Custom hierarchy, `try/catch`, `instanceof` | Retry / `finally` patterns |
| **JSON** | 3 | **80%** | `parseJson`, `JSON.stringify` in tests | — |
| **Promises** | 10 | **5%** | `Promise.resolve` stub only | `.then`/`.catch`, chaining, `Promise.all` |
| **async / await** | 6 | **0%** | — | Entire boundary |
| **Event loop** | 8 | **0%** | — | Microtasks vs macrotasks, ordering MCQs |
| **`this` / bind / call / apply** | 8 | **5%** | — | Entire boundary (critical gap) |
| **Prototypes & inheritance** | 8 | **20%** | `extends`, `instanceof`, `super` | `Object.create`, manual chain, `prototype` |

**Tier 1 topic-weighted average: ~44%** *(not ~38%; async/`this`/event-loop zeros drag headline, not this tier's mean)*

---

### Tier 2 — common in machine coding & OA

| Boundary | Topics (≈) | Coverage | Covered | Missing |
|----------|------------|----------|---------|---------|
| **Scope / hoisting / TDZ** | 8 | **10%** | `const`/`let` usage | `var` hoisting MCQs, TDZ |
| **Control flow & loops** | 8 | **25%** | `if`, `throw`, `return`; `forEach` | `for`, `while`, `switch`, `for...of` |
| **Objects & copying** | 8 | **55%** | Literals, spread clone, computed keys | Deep clone, `structuredClone` |
| **Map / Set** | 5 | **25%** | `Set` for status enum | `Map` for dedup / frequency |
| **Strings (practical)** | 6 | **50%** | Templates, `charAt`, `slice`, `trim` | `split`, basic `.test()` |
| **Implementation katas** | 8 | **8%** | `curry(fn)` body written | Not exported; no `debounce`, `throttle`, `bind`, `Promise.all` |
| **Timers** | 4 | **0%** | — | `setTimeout`, `setInterval`, cleanup |
| **fetch & HTTP errors** | 4 | **0%** | — | `fetch`, status codes → `NetworkError` |
| **Design patterns** | 5 | **40%** | Factory pipeline, abstract base | Observer / pub-sub not started |
| **fn.length / coercion tricks** | 4 | **60%** | `fn.length` in `curry()`; `valueOf` on `infiniteSum2` | Not exported; `kata/test_curry.mjs` imports missing `add` — harness is broken |
| **Modules (ESM basics)** | 4 | **60%** | `import`/`export` | — |
| **Numbers (practical)** | 4 | **35%** | `Number.isNaN`, arithmetic | `parseInt`, `Math.floor` |

**Tier 2 average: ~32%**

---

### Tier 3 — frontend-only (included for FE interviews, not weighted in backend score)

| Boundary | Topics (≈) | Coverage | Notes |
|----------|------------|----------|-------|
| **DOM & events** | 6 | **0%** | Delegation, bubbling, `addEventListener` |
| **React patterns** | 8 | **0%** | Hooks, `useEffect` polling — deps in `package.json`, no code |

Excluded from the **~41%** headline. For the **~38%** JS+DOM lens, add the DOM row (8% weight, 0% coverage). For a **full FE interview loop**, use **~26%** — React/DOM are a large slice of what interviewers ask.

---

## Coverage heatmap (interview corpus)

```
BOUNDARY                          COVERAGE
─────────────────────────────────────────────
Closures & HOF                    ██████████████████░░  90%
Currying / partial application    ███████████████░░░░░  78%
JSON                              ████████████████░░░░  80%
Classes & OOP                     ██████████████░░░░░░  70%
Error handling                    ██████████████░░░░░░  70%
ES6+ syntax                       █████████████░░░░░░░  68%
fn.length / coercion tricks       ████████████░░░░░░░░  60%
Modules (ESM basics)              ████████████░░░░░░░░  60%
Objects & copying                 ███████████░░░░░░░░░  55%
Strings (practical)               ██████████░░░░░░░░░░  50%
Type coercion & equality          █████████░░░░░░░░░░░  45%
Array methods                     ████████░░░░░░░░░░░░  40%
Design patterns                   ████████░░░░░░░░░░░░  40%
Numbers (practical)               ███████░░░░░░░░░░░░░  35%
Map / Set                         █████░░░░░░░░░░░░░░░  25%
Control flow & loops              █████░░░░░░░░░░░░░░░  25%
Prototypes & inheritance          ████░░░░░░░░░░░░░░░░  20%
Scope / hoisting / TDZ            ██░░░░░░░░░░░░░░░░░░  10%
Implementation katas              █░░░░░░░░░░░░░░░░░░░   8%
Promises                          █░░░░░░░░░░░░░░░░░░░░░   5%
this / bind / call / apply        █░░░░░░░░░░░░░░░░░░░░░   5%
Async & event loop                █░░░░░░░░░░░░░░░░░░░░░   5%
Timers / fetch                    ░░░░░░░░░░░░░░░░░░░░░░   0%
DOM & React (FE)                  ░░░░░░░░░░░░░░░░░░░░░░   0%
```

---

## By interview type

### Mettl / TCS / Accenture OA — **~48%**

| OA staple | Status |
|-----------|--------|
| Currying (`sum3`, infinite sum, `curry(fn)`) | Implemented in `kata/curry.js` but **not exported** — not runnable via `test_curry.mjs` without fixes |
| `fn.length` parameter traps | Documented in comments; `fn.length` used inside `curry()` |
| `valueOf` / loose `==` coercion | `infiniteSum2` implements it; imported as `add` in test harness — **broken** |
| Output prediction (closure, coercion) | Partial |
| Async / Promise output ordering | Missing |
| `var` hoisting traps | Missing |

### FAANG / product JS screen — **~30%**

| Screen staple | Status |
|---------------|--------|
| Closure + scope puzzles | Strong |
| Implement `debounce` / `bind` / `Promise.all` | Missing |
| Event loop ordering | Missing |
| `this` in callbacks / lost context | Missing |
| Clean OOP + error design | Strong |

### Machine coding (90 min) — **~38%**

| Expectation | Status |
|-------------|--------|
| Class design + validation | `Feed.js` — ready |
| Data transformation pipeline | `pipeline.js` — ready |
| Live polling + API | `PollingFeed.js` — empty |
| Tests | Vitest — good |

### Frontend React — **~26%**

Pure JS fundamentals partial; no React/DOM code yet.

---

## Superpowers vs blind spots

```
INTERVIEW-READY                    WILL GET ASKED — WILL HURT
────────────────                   ────────────────────────────
Closures & HOF           90%       Event loop               0%
Currying                 78%       async/await              0%
pipe / compose / FP      88%       this / bind / apply      5%
Classes & inheritance    70%       Promises (deep)          5%
Custom errors            70%       debounce / throttle      0%
JSON / parse safety      80%       map / filter idioms     40%
OA coercion tricks       60%       Hoisting MCQs           10%
                              Kata harness integration   broken
```

---

## Highest-ROI next steps

| Action | Practical % gain | Ties to repo |
|--------|------------------|--------------|
| Fix kata exports + wire Vitest | **+3%** | `kata/curry.js` |
| Implement `PollingFeed` (`fetch`, `async/await`, timers) | **+12–15%** | `src/feeds/PollingFeed.js` |
| Kata: `debounce` + `throttle` | **+5–8%** | `kata/` |
| Kata: implement `bind` or `Promise.all` | **+5–7%** | `kata/` |
| Event-loop ordering drill sheet (10 MCQs) | **+5%** | `docs/` or `kata/` |
| Use `map`/`filter` in pipeline | **+3%** | `src/feeds/pipeline.js` |
| `this` / `call` / `apply` kata | **+5%** | `kata/` |

**Target:** `PollingFeed` + fix kata exports + 3 katas → **~41% → ~63%** on this pruned corpus.

---

## Code evidence (what interviewers would praise)

| Pattern | File | Interview signal |
|---------|------|------------------|
| Abstract base + `new.target` | `src/feeds/Feed.js` | OOP design maturity |
| Private fields + defensive copy | `src/feeds/Feed.js` | Encapsulation |
| Curried pure pipeline | `src/feeds/pipeline.js` | FP + immutability |
| `pipe` / `compose` | `utils/helpers.js` | HOF fluency |
| Custom error taxonomy | `src/feeds/errors.js` | Production error modeling |
| Universal `curry(fn)` | `kata/curry.js` | Written but **not exported**; not in Vitest suite |

---

## 2026 interview-source alignment (trimming audit)

Cross-checked against current interview guides ([InterviewChamp 2026](https://interviewchamp.ai/learn/javascript-interview-questions-2026), [Playcode 2026](https://playcode.io/blog/javascript-technical-interview-guide), [StackInterview 2026](https://stackinterview.dev/guides/javascript-interview-questions-and-answers-2026)).

### What the pruned corpus gets right for 2026

| 2026 interview bucket (typical weight) | In pruned corpus? | Repo coverage |
|----------------------------------------|---------------------|---------------|
| Language internals — closures, `this`, hoisting, prototypes (40–50%) | Yes | Partial — strong closures, weak `this`/hoisting/prototypes |
| Async — promises, `async`/`await`, event loop (20–30%) | Yes | **~5%** — critical gap |
| Live coding — debounce, throttle, clone, array utils (20–30%) | Yes | **~8%** — critical gap |
| Framework / DOM / ecosystem (5–10%+) | Tier 3 only | **0%** |

### Trimming decisions — verdict

| Removed | 2026 verdict | Notes |
|---------|--------------|-------|
| Intl, TypedArrays, WeakRef, Workers | **Correct cut** | Not in standard 3 YOE JS loops |
| Proxy & Reflect | **Correct cut** | Staff+ niche |
| Advanced RegExp | **Correct cut** | Basic `.test()` kept as a string subtopic (not implemented in repo) |
| Generators | **Borderline cut** | Rare in OA; still appears at some senior screens — footnoted, not scored |
| `import.meta`, dynamic `import` | **Correct cut** | Build trivia, not language fluency |
| DOM / React in headline score | **Correct separation** | But **must not** be read as "irrelevant" — FE loops weight them heavily |

### Topics the doc should not have cut (already kept)

- `debounce` / `throttle` — top live-coding asks in 2026
- Event-loop ordering MCQs — 20–30% of async bucket
- `map` / `filter` — live-coding + practical coding
- `?.` / `??` — increasingly default in modern codebases (listed as missing — correct)

---

## Adversarial audit notes (2026-09-03)

Findings from a skeptical re-read of the repo **and** this document's internal consistency:

1. **Mega-boundary weights originally summed to 110%** — corrected to 100% for headline; DOM row is an **overlay** (+8%) for FE lens → **~38%**.
2. **`kata/curry.js` has no `export` statements** — `kata/test_curry.mjs` cannot run as-is; Level 3 imports `add` but the function is named `infiniteSum2`.
3. **Iteration protocol was credited at 4% in README** — `forEach`/`reduce` are not the iterator protocol; corrected to **~0%** in README.
4. **MDN headline 12% vs boundary-table math ~19%** — same numerator, different denominators (~700 vs ~448 topics); documented in README.
5. **ES6 destructuring was under-credited** — `normalizerFactory({ feedId, requiredFields = [], timestampField })` is real object destructuring with defaults.
6. **Design patterns at 55% was generous** — only factory + abstract base exist; revised to **40%**.
7. **`PollingFeed` is syntactic coverage only** — `extends Feed` with no methods does not demonstrate polling competence.
8. **Subjective scores** (production-core, feed-console foundations) have no enumerated checklists — directional only.
9. **Generators elimination is borderline** — still omitted from pruned corpus; Google-style loops occasionally ask them.
10. **`NetworkError` is defined but never thrown** in production code — error taxonomy is tested, not exercised at runtime.
11. **"~95 topics" understated the tier tables** — Tier 1+2 sum to **~177 topic-slots**; headline **~41%** uses weighted mega-boundaries. Corrected to **~110 topic-slots** (deduplicated estimate).
12. **Tier 1 "average ~38%" was wrong** — topic-weighted Tier 1 mean is **~44%**; headline **~41%** is lower because async/`this`/event-loop weights sit in mega-boundaries.
13. **FE "~26%" vs "~38%" looked contradictory** — they measure different things; score definitions table added at top.
14. **`VALIDATORS.number` exists but has no tests** — number validation is implemented, not verified.
15. **Mega "Closures & FP 82%" ≠ tier "Closures 90%"** — mega row blends HOF + currying; documented in diagram, not an error.

---

## Methodology

- **Pruned corpus ≈ 110 topic-slots** in Tier 1+2 tables (~177 raw slots; ~110 after boundary deduplication). See README for full MDN audit.
- Elimination bar: *"Would a reasonable 3 YOE FE/FS interviewer ask this in &gt;10% of loops?"* If no → cut.
- **"Meaningfully used"** = real code or kata implementation, not comments alone.
- **DOM/React** scored separately — included for FE targeting, not in core **~41%**.
- Re-run when `PollingFeed`, `kata/debounce.js`, or UI layer lands.
- **Kata integration gap:** interview FP code in `kata/curry.js` is not exported or covered by Vitest — scores reflect *code written*, not *verified runnable* until exports are fixed.

---

## Revision log

| Date | Change |
|------|--------|
| 2026-09-03 | Initial practical corpus — pruned from MDN audit |
| 2026-09-03 | Adversarial review — weights fixed, scores revised, kata export gap documented |
| 2026-09-03 | 2026 interview-source alignment + ground-truth fixes (topic count, tier average, FE score definitions) |
