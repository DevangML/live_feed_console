import json, os

BASE_DIR = '/Users/devang/Desktop/live_feed_console'

# 1. CORE PIPELINE & ARCHITECTURE GRAPH (index.html)
# Linear, crystal-clear start-to-end data pipeline flow with directional stages and containment bounding zones
pipeline_graph = {
  "zones": [
    {
      "id": "zone-input",
      "name": "Stage 1: Ingestion & Polling Motor",
      "color": "#00ff66",
      "bounds": {"x": -60, "y": 0, "z": 0, "width": 30, "height": 35, "depth": 30},
      "description": "Where external network polling begins, manages timers, abort signals, and HTTP dispatch."
    },
    {
      "id": "zone-pipeline",
      "name": "Stage 2: Pure Functional Transformation Pipeline",
      "color": "#9d4edd",
      "bounds": {"x": 0, "y": 0, "z": 0, "width": 45, "height": 35, "depth": 30},
      "description": "Zero-trust boundary: parses raw JSON, validates schema, normalizes epoch timestamps, enriches telemetry."
    },
    {
      "id": "zone-domain",
      "name": "Stage 3: Encapsulated Domain & State Machine",
      "color": "#00f0ff",
      "bounds": {"x": 60, "y": 0, "z": 0, "width": 35, "height": 35, "depth": 30},
      "description": "Abstract Feed base class, circuit breaker telemetry, status state transitions, and defensive copies."
    },
    {
      "id": "zone-foundations",
      "name": "Cross-Cutting Foundations & Guards",
      "color": "#ffb700",
      "bounds": {"x": 0, "y": -45, "z": 0, "width": 80, "height": 25, "depth": 30},
      "description": "Underlying combinators (pipe, parseJson), invariant assertions, strategy validators, and error hierarchy."
    },
    {
      "id": "zone-tests",
      "name": "Verification Dock: Vitest BDD Test Suite Container",
      "color": "#1dd1a1",
      "bounds": {"x": 0, "y": 48, "z": -25, "width": 95, "height": 26, "depth": 25},
      "description": "Isolated test harness dock proving mathematical correctness and boundaries for all runtime modules."
    }
  ],
  "nodes": [
    # STAGE 1: INGESTION MOTOR
    {
      "id": "PollingFeed.js",
      "path": "src/feeds/PollingFeed.js",
      "name": "PollingFeed.js",
      "type": "src",
      "cluster": "ingestion",
      "stage": "1. Ingestion Motor",
      "color": "#00ff66",
      "pos": [-60, 5, 0],
      "contract": {
        "kind": "Asynchronous Motor Subclass",
        "inherits": "Feed",
        "constructor": "constructor(id, name, endpoints, intervalMs = 5000, normalizer)",
        "internalState": ["#intervalMs", "#timerId", "#abortController", "#normalizer"],
        "methods": [
          "start(): Initiates non-overlapping recursive setTimeout loop",
          "fetch(): Dispatches HTTP GET with AbortSignal, pipes to normalizer, records telemetry",
          "stop(): Cancels active timer and calls abortController.abort()"
        ]
      },
      "semanticsAndFlow": {
        "executionRole": "ENTRY POINT OF DATA INGESTION",
        "flow": "Wakes on recursive timer -> fetch() -> passes raw text into pipeline.js -> records latency on Feed.js -> schedules next poll."
      },
      "pseudocode": """// Polling Motor: Ingestion Origin
class PollingFeed extends Feed {
  async fetch() {
    this.#abortController = new AbortController();
    const start = performance.now();
    try {
      this.setStatus('FETCHING');
      const res = await fetch(this.endpoints[0], { signal: this.#abortController.signal });
      if (!res.ok) throw new NetworkError(`HTTP ${res.status}`, this.id, res.status);
      const rawText = await res.text();
      const normalized = this.#normalizer(rawText);
      this.recordSuccess(performance.now() - start);
      this.setStatus('CONNECTED');
      return normalized;
    } catch (err) {
      this.recordFailure(err);
      this.setStatus(this.consecutiveFailures >= 3 ? 'DEGRADED' : 'ERROR');
      throw err;
    }
  }
}""",
      "enablingConcepts": [
        {
          "name": "Recursive setTimeout (Overlapping Poll Elimination)",
          "inventedFor": "setInterval triggers on clock ticks even if network requests stall, causing socket pile-ups and memory lockup.",
          "solvesForUs": "Guarantees next poll only schedules after the previous request settles, providing automatic backpressure.",
          "details": "Executes next poll in 'finally' handler of the settled promise."
        },
        {
          "name": "AbortController Cooperative Cancellation",
          "inventedFor": "WHATWG standard to cancel in-flight HTTP requests and DOM listeners on teardown.",
          "solvesForUs": "Immediately aborts socket connections when feed is stopped, preventing out-of-order state mutations.",
          "details": "Signal passed to fetch(); abort() triggers an AbortError DOMException."
        }
      ]
    },

    # STAGE 2: PURE FUNCTIONAL TRANSFORMATION PIPELINE
    {
      "id": "pipeline.js",
      "path": "src/feeds/pipeline.js",
      "name": "pipeline.js",
      "type": "src",
      "cluster": "pipeline",
      "stage": "2. Data Cleansing Pipeline",
      "color": "#9d4edd",
      "pos": [0, 5, 0],
      "contract": {
        "kind": "Curried Functional Pipeline (Pure)",
        "exports": [
          "validateSchema(requiredFields)(data)",
          "normalizeTimestamps(timestampField)(data)",
          "enrichFeedMetadata(feedId)(data)",
          "normalizerFactory({ feedId, requiredFields, timestampField })"
        ],
        "invariants": [
          "Zero mutation: returns new shallow copy at each stage ({ ...data })",
          "Unary functions: every stage takes exactly 1 parameter for pipe() compatibility"
        ]
      },
      "semanticsAndFlow": {
        "executionRole": "PURE BOUNDARY TRANSFORM ENGINE",
        "flow": "raw text -> parseJson -> validateSchema -> normalizeTimestamps -> enrichFeedMetadata -> Clean NormalizedMetricEvent"
      },
      "pseudocode": """// Curried Pipeline Stages
export const normalizerFactory = ({ feedId, requiredFields, timestampField }) =>
  pipe(
    parseJson,
    validateSchema(requiredFields),
    normalizeTimestamps(timestampField),
    enrichFeedMetadata(feedId)
  );""",
      "enablingConcepts": [
        {
          "name": "Currying & Partial Application for Function Composition",
          "inventedFor": "Haskell Curry & Moses Schönfinkel in combinatory logic to convert f(a,b) to f(a)(b).",
          "solvesForUs": "Pre-configures schema validation rules and feed IDs at startup, returning pure unary functions ready for streaming.",
          "details": "The outer function captures configuration in closure; inner function receives live incoming data."
        },
        {
          "name": "Point-Free Style & Unix Pipe Architecture",
          "inventedFor": "Unix pipes (1973): small composable programs linked linearly without intermediate file mutations.",
          "solvesForUs": "Transforms raw text to validated event without creating mutable temporary variables.",
          "details": "Implemented via Array.prototype.reduce in pipe()."
        },
        {
          "name": "Epoch Thresholding (Seconds vs Milliseconds Normalization)",
          "inventedFor": "Standardizing POSIX seconds (Unix ~1.7e9) with JavaScript milliseconds (~1.7e12).",
          "solvesForUs": "Math heuristic: timestamps < 10 billion are seconds (*1000); above are milliseconds.",
          "details": "Handles ISO-8601 strings via Date.parse() with fallback to Date.now()."
        }
      ]
    },

    # STAGE 3: DOMAIN BASE & STATE MACHINE
    {
      "id": "Feed.js",
      "path": "src/feeds/Feed.js",
      "name": "Feed.js",
      "type": "src",
      "cluster": "domain",
      "stage": "3. Encapsulated State Machine",
      "color": "#00f0ff",
      "pos": [60, 5, 0],
      "contract": {
        "kind": "Abstract Domain Class",
        "guard": "if (new.target === Feed) throw TypeError",
        "privateFields": ["#id", "#name", "#endpoints", "#status", "#lastFetchedAt", "#lastLatencyMs", "#consecutiveFailures", "#lastError"],
        "methods": ["setStatus(s)", "recordSuccess(latency)", "recordFailure(err)", "start()", "stop()", "fetch()"]
      },
      "semanticsAndFlow": {
        "executionRole": "STATE MACHINE & TELEMETRY INVARIANT GUARD",
        "flow": "Tracks feed status (IDLE -> FETCHING -> CONNECTED / DEGRADED / ERROR) and latency telemetry."
      },
      "pseudocode": """class Feed {
  #id; #name; #endpoints; #status = 'IDLE';
  #lastFetchedAt; #lastLatencyMs; #consecutiveFailures = 0;

  constructor(id, name, endpoints) {
    if (new.target === Feed) throw TypeError("Cannot construct Feed directly");
    this.#endpoints = [...endpoints]; // defensive copy
  }

  get endpoints() { return [...this.#endpoints]; } // defensive getter

  recordSuccess(latency) {
    this.#lastFetchedAt = Date.now();
    this.#lastLatencyMs = latency;
    this.#consecutiveFailures = 0;
  }
}""",
      "enablingConcepts": [
        {
          "name": "Abstract Base Class via new.target Guard",
          "inventedFor": "Enforces abstract inheritance in JavaScript without language-level abstract keyword.",
          "solvesForUs": "Prevents incomplete generic feeds from ever being instantiated directly.",
          "details": "new.target resolves to the constructor invoked by 'new'."
        },
        {
          "name": "Hard Encapsulation (#private fields)",
          "inventedFor": "V8 lexical private brand checks replacing leaky _prefix conventions.",
          "solvesForUs": "Rogue UI components or external scripts cannot corrupt failure counters, status, or endpoints.",
          "details": "Private fields are invisible to Object.keys() and JSON.stringify()."
        },
        {
          "name": "Defensive Copying at Boundaries",
          "inventedFor": "Array reference aliasing bug prevention.",
          "solvesForUs": "Prevents consumers from mutating the internal endpoints array.",
          "details": "[...endpoints] clones array in constructor and getter."
        },
        {
          "name": "Circuit Breaker Telemetry Tracking",
          "inventedFor": "Michael Nygard's 'Release It!' for distributed system resilience.",
          "solvesForUs": "Detects 3 consecutive failures to degrade feed gracefully before memory or network crashes.",
          "details": "Primitive numeric counters updated in-place with zero GC overhead."
        }
      ]
    },

    # FOUNDATIONS LAYER (BOTTOM)
    {
      "id": "helpers.js",
      "path": "utils/helpers.js",
      "name": "helpers.js",
      "type": "utils",
      "cluster": "foundations",
      "stage": "Foundation: Combinators",
      "color": "#ffb700",
      "pos": [-25, -42, 0],
      "contract": {
        "exports": ["pipe(...funcs)", "compose(...funcs)", "parseJson(raw)", "capitalize(s)"]
      },
      "semanticsAndFlow": {
        "executionRole": "FUNCTIONAL PLUMBING & SAFE SHIELD",
        "flow": "pipe() runs reduce; parseJson shields native SyntaxErrors as domain ParseErrors."
      },
      "pseudocode": """export const pipe = (...funcs) => (val) =>
  funcs.reduce((prev, fn) => fn(prev), val);

export const parseJson = (raw) => {
  if (typeof raw !== 'string') return raw;
  try { return JSON.parse(raw); }
  catch (e) { throw new ParseError(e.message, 'unknown'); }
};""",
      "enablingConcepts": [
        {
          "name": "Left-to-Right Function Composition (pipe)",
          "inventedFor": "Category theory composition implemented via Array.prototype.reduce.",
          "solvesForUs": "Readable linear transformation flow pipe(f, g, h)(x) === h(g(f(x))).",
          "details": "Executes synchronously, passing accumulator output to next stage."
        },
        {
          "name": "Boundary Exception Shielding",
          "inventedFor": "Defensive programming around native JSON.parse.",
          "solvesForUs": "Intercepts SyntaxError and stamps with telemetry-aware ParseError.",
          "details": "Passthrough if input is already parsed object."
        }
      ]
    },
    {
      "id": "assertions.js",
      "path": "utils/assertions.js",
      "name": "assertions.js",
      "type": "utils",
      "cluster": "foundations",
      "stage": "Foundation: Invariant Guard",
      "color": "#ff5500",
      "pos": [10, -42, 0],
      "contract": {
        "exports": ["assertValid(value, label, type)"]
      },
      "semanticsAndFlow": {
        "executionRole": "FAIL-FAST INVARIANT CHECKER",
        "flow": "Queries VALIDATORS[type] -> checkType -> isEmpty -> throws TypeError / RangeError."
      },
      "pseudocode": """export function assertValid(value, label, type) {
  const rules = VALIDATORS[type];
  if (!rules) throw new TypeError(`Unknown validation type: ${type}`);
  if (!rules.checkType(value)) throw new TypeError(`${label} has invalid type`);
  if (rules.isEmpty(value)) throw new RangeError(`${label} cannot be empty`);
}""",
      "enablingConcepts": [
        {
          "name": "Fail-Fast Invariant Enforcement",
          "inventedFor": "Jim Gray (Turing Award). Halts execution at the exact point of invalid input.",
          "solvesForUs": "Ensures no Feed can be created with corrupt ID or empty endpoints.",
          "details": "Distinguishes TypeError (wrong primitive) from RangeError (empty bounds)."
        }
      ]
    },
    {
      "id": "validators.js",
      "path": "utils/validators.js",
      "name": "validators.js",
      "type": "utils",
      "cluster": "foundations",
      "stage": "Foundation: Strategy Predicates",
      "color": "#e056fd",
      "pos": [45, -42, 0],
      "contract": {
        "exports": ["VALIDATORS (string, number, array rules)"]
      },
      "semanticsAndFlow": {
        "executionRole": "PREDICATE RULEBOOK",
        "flow": "Supplies type and bounds checking logic to assertions.js."
      },
      "pseudocode": """export const VALIDATORS = {
  string: { checkType: (v) => typeof v === 'string', isEmpty: (v) => v.trim() === '' },
  number: { checkType: (v) => typeof v === 'number' && !Number.isNaN(v), isEmpty: () => false },
  array: { checkType: (v) => Array.isArray(v), isEmpty: (v) => v.length === 0 || v.some(e => typeof e === 'string' && e.trim() === '') }
};""",
      "enablingConcepts": [
        {
          "name": "Data-Driven Strategy Pattern",
          "inventedFor": "GoF Strategy Pattern to decouple rule logic from assertion mechanisms.",
          "solvesForUs": "Extensible validation predicates without modifying constructor code.",
          "details": "Uses Array.isArray and Number.isNaN to defend against JS type coercion flaws."
        }
      ]
    },
    {
      "id": "errors.js",
      "path": "src/feeds/errors.js",
      "name": "errors.js",
      "type": "src",
      "cluster": "foundations",
      "stage": "Foundation: Error Telemetry",
      "color": "#ff007f",
      "pos": [-60, -42, 0],
      "contract": {
        "classes": ["FeedError extends Error", "NetworkError extends FeedError", "ParseError extends FeedError"]
      },
      "semanticsAndFlow": {
        "executionRole": "TELEMETRY EXCEPTION HIERARCHY",
        "flow": "Carries feedId and HTTP statusCode across system boundaries for automated triage."
      },
      "pseudocode": """class FeedError extends Error {
  constructor(message, feedId) {
    super(message);
    this.feedId = feedId;
    this.name = 'FeedError';
  }
}
class NetworkError extends FeedError {
  constructor(message, feedId, statusCode) {
    super(message, feedId);
    this.statusCode = statusCode;
    this.name = 'NetworkError';
  }
}
class ParseError extends FeedError {
  constructor(message, feedId) {
    super(message, feedId);
    this.name = 'ParseError';
  }
}""",
      "enablingConcepts": [
        {
          "name": "Prototypal Error Hierarchy & Telemetry Tagging",
          "inventedFor": "Enables instanceof discrimination in catch blocks without string parsing.",
          "solvesForUs": "Downstream catch triage: retry NetworkError vs quarantine ParseError.",
          "details": "Inherits V8 stack trace capture while stamping feedId and statusCode."
        }
      ]
    },

    # VERIFICATION DOCK (TOP DOCKING ZONE)
    {
      "id": "Feed.test.js",
      "path": "tests/src/feeds/Feed.test.js",
      "name": "Feed.test.js",
      "type": "test",
      "cluster": "test-dock",
      "stage": "Verification Dock",
      "color": "#1dd1a1",
      "pos": [35, 48, -25],
      "contract": {"kind": "Vitest Behavioral Test Suite", "target": "Feed.js"},
      "semanticsAndFlow": {"executionRole": "BDD INVARIANT PROOF", "flow": "Verifies new.target guard, defensive copying, and status transitions."},
      "pseudocode": """describe('Feed.js', () => {
  it('rejects direct instantiation', () => expect(() => new Feed('id','name',['url'])).toThrow(TypeError));
  it('guarantees defensive copying', () => { ... });
});""",
      "enablingConcepts": [{
        "name": "Automated BDD Invariant Proof",
        "inventedFor": "Dan North / Kent Beck. Proves boundaries remain intact during refactoring.",
        "solvesForUs": "Mathematically proves Feed encapsulation.",
        "details": "Sub-millisecond Vitest isolate execution."
      }]
    },
    {
      "id": "pipeline.test.js",
      "path": "tests/src/feeds/pipeline.test.js",
      "name": "pipeline.test.js",
      "type": "test",
      "cluster": "test-dock",
      "stage": "Verification Dock",
      "color": "#54a0ff",
      "pos": [0, 48, -25],
      "contract": {"kind": "Vitest Pipeline Test Suite", "target": "pipeline.js"},
      "semanticsAndFlow": {"executionRole": "PIPELINE FUZZING & PROOF", "flow": "Verifies schema validation, timestamp normalization, and metadata injection."},
      "pseudocode": """describe('pipeline.js', () => {
  it('normalizes seconds to milliseconds', () => { ... });
  it('enriches metadata', () => { ... });
});""",
      "enablingConcepts": [{
        "name": "Boundary Fuzzing Proof",
        "inventedFor": "Validates every branch of pure transformations under dirty data.",
        "solvesForUs": "Guarantees zero dirty data reaches application state.",
        "details": "Tests against JSON strings, plain objects, nulls, and corrupt inputs."
      }]
    },
    {
      "id": "errors.test.js",
      "path": "tests/src/feeds/errors.test.js",
      "name": "errors.test.js",
      "type": "test",
      "cluster": "test-dock",
      "stage": "Verification Dock",
      "color": "#ff6b6b",
      "pos": [-35, 48, -25],
      "contract": {"kind": "Vitest Inheritance Test Suite", "target": "errors.js"},
      "semanticsAndFlow": {"executionRole": "PROTOTYPE CHAIN PROOF", "flow": "Asserts instanceof prototype integrity across FeedError subclasses."},
      "pseudocode": """it('verifies prototype inheritance chain', () => {
  const err = new NetworkError('timeout', 'feed-1', 504);
  expect(err instanceof NetworkError).toBe(true);
});""",
      "enablingConcepts": [{
        "name": "Prototype Chain Verification",
        "inventedFor": "Ensures transpilation or class inheritance retains native instanceof.",
        "solvesForUs": "Verifies catch handlers will function deterministically.",
        "details": "Tests Error -> FeedError -> NetworkError prototype walk."
      }]
    }
  ],
  "edges": [
    # MAIN START-TO-END PIPELINE FLOW
    {
      "source": "PollingFeed.js",
      "target": "pipeline.js",
      "type": "primary-pipeline",
      "label": "1. Ingestion Dispatch ➔ Pipeline Ingestion",
      "concept": "PollingFeed passes raw HTTP response text into normalizerFactory to initiate pure transformation"
    },
    {
      "source": "pipeline.js",
      "target": "Feed.js",
      "type": "primary-pipeline",
      "label": "2. Normalized Event ➔ Domain Telemetry",
      "concept": "Successful normalized event updates Feed latency metrics, resets circuit breaker, and shifts status to CONNECTED"
    },
    {
      "source": "PollingFeed.js",
      "target": "Feed.js",
      "type": "extends",
      "label": "Inherits Abstract Base Class",
      "concept": "PollingFeed inherits private slots, status state machine, and telemetry methods via super()"
    },
    # FOUNDATIONAL SUPPORT EDGES
    {
      "source": "pipeline.js",
      "target": "helpers.js",
      "type": "imports",
      "label": "Uses pipe() & parseJson()",
      "concept": "Composes curried stages and shields JSON.parse SyntaxErrors"
    },
    {
      "source": "pipeline.js",
      "target": "errors.js",
      "type": "throws",
      "label": "Throws ParseError",
      "concept": "Raises domain ParseError when schema validation fails or payload is malformed"
    },
    {
      "source": "PollingFeed.js",
      "target": "errors.js",
      "type": "throws",
      "label": "Throws NetworkError",
      "concept": "Raises NetworkError with HTTP statusCode when remote server returns non-200"
    },
    {
      "source": "Feed.js",
      "target": "assertions.js",
      "type": "imports",
      "label": "Constructor Boundary Guard",
      "concept": "assertValid enforces non-empty string and array types in Feed constructor"
    },
    {
      "source": "assertions.js",
      "target": "validators.js",
      "type": "delegates",
      "label": "Predicate Rule Lookup",
      "concept": "VALIDATORS strategy dictionary defines checkType and isEmpty predicates"
    },
    # VERIFICATION EDGES
    {
      "source": "Feed.test.js",
      "target": "Feed.js",
      "type": "tests",
      "label": "Verifies Feed Invariants",
      "concept": "Proves new.target guard, defensive copying, and state machine transitions"
    },
    {
      "source": "pipeline.test.js",
      "target": "pipeline.js",
      "type": "tests",
      "label": "Verifies Pipeline Invariants",
      "concept": "Proves schema validation, epoch thresholding, and metadata enrichment"
    },
    {
      "source": "errors.test.js",
      "target": "errors.js",
      "type": "tests",
      "label": "Verifies Error Hierarchy",
      "concept": "Proves prototype chain integrity for instanceof discrimination"
    }
  ]
}

# 2. SEPARATE KATA CRUCIBLE GRAPH (katas.html)
kata_graph = {
  "nodes": [
    {
      "id": "curry.js",
      "path": "kata/curry.js",
      "name": "curry.js",
      "type": "kata",
      "category": "The Currying Crucible: L1 to L5 Mastery",
      "color": "#00d2d3",
      "pos": [0, 0, 0],
      "levels": [
        {"level": 1, "title": "Fixed 3-Arity Sum (Warmup)", "example": "sum3(1)(2)(3) === 6", "concept": "Nested lexical closures returning functions until arity reached."},
        {"level": 2, "title": "Infinite Sum with Empty Terminator", "example": "infiniteSum(1)(2)(3)() === 6", "concept": "Checking args.length === 0 in recursive closure to terminate."},
        {"level": 3, "title": "Coercion Trap via valueOf", "example": "add(1)(2)(3) + 4 === 10", "concept": "Overriding Function.prototype.valueOf / Symbol.toPrimitive to intercept numeric coercion."},
        {"level": 4, "title": "Universal curry(fn) Machine Coding", "example": "curry(fn)(1, 2)(3) === fn(1,2,3)", "concept": "Inspecting fn.length arity and accumulating arguments recursively."},
        {"level": 5, "title": "Placeholder Curry (Lodash _ Style)", "example": "curriedSub(_, 2)(5, 1) === 2", "concept": "Staff-level out-of-order argument accumulation using Symbol tokens."}
      ],
      "mcqBank": [
        {"q": "function f1(a, b = 2, c) {}; console.log(f1.length);", "ans": "1", "why": "fn.length stops at the first default parameter."},
        {"q": "function f2(a, ...rest) {}; console.log(f2.length);", "ans": "1", "why": "Rest parameters (...rest) are never counted in fn.length."}
      ]
    },
    {
      "id": "partial_application.js",
      "path": "kata/partial_application.js",
      "name": "partial_application.js",
      "type": "kata",
      "category": "Partial Application vs Currying",
      "color": "#ffb700",
      "pos": [-30, -15, 0],
      "details": "Fixing a subset of arguments now, returning a function accepting the remaining arguments in a single call."
    },
    {
      "id": "currying.js",
      "path": "kata/currying.js",
      "name": "currying.js",
      "type": "kata",
      "category": "Unary Decomposition",
      "color": "#9d4edd",
      "pos": [30, -15, 0],
      "details": "Transforming f(a,b,c) strictly into unary chains f(a)(b)(c)."
    }
  ]
}

with open(os.path.join(BASE_DIR, 'docs/visualizer/pipeline_graph.json'), 'w', encoding='utf-8') as f:
  json.dump(pipeline_graph, f, indent=2)

with open(os.path.join(BASE_DIR, 'docs/visualizer/kata_graph.json'), 'w', encoding='utf-8') as f:
  json.dump(kata_graph, f, indent=2)

print("Generated pipeline_graph.json and kata_graph.json successfully.")
