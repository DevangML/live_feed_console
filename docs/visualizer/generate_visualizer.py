import os, json, re

BASE_DIR = '/Users/devang/Desktop/live_feed_console'

# Define semantic graph of the files with contract, pseudocode, concepts, real-world rationale, etc.
nodes = [
    {
        "id": "Feed.js",
        "path": "src/feeds/Feed.js",
        "name": "Feed.js",
        "type": "src",
        "cluster": "feeds",
        "category": "Core Domain / Abstract Base",
        "color": "#00f0ff",
        "pos": [-35, 15, 0],
        "contract": {
            "kind": "Abstract Class (ES6)",
            "instantiation": "Guarded by new.target !== Feed (throws TypeError if called directly with new)",
            "constructor": "constructor(id: string, name: string, endpoints: string[])",
            "privateFields": [
                "#id (string)",
                "#name (string)",
                "#endpoints (string[], defensively copied)",
                "#status ('IDLE' | 'FETCHING' | 'CONNECTED' | 'DEGRADED' | 'ERROR')",
                "#lastFetchedAt (number | null, ms)",
                "#lastLatencyMs (number)",
                "#consecutiveFailures (number)",
                "#lastError (Error | null)"
            ],
            "getters": ["id", "name", "status", "endpoints (defensive copy)", "lastFetchedAt", "lastLatencyMs", "consecutiveFailures", "lastError"],
            "methods": [
                "setStatus(newStatus: string): void — validates against VALID_STATUSES Set",
                "recordSuccess(latencyMs: number): void — resets consecutiveFailures & lastError, stamps timestamp",
                "recordFailure(error: Error): void — increments consecutiveFailures, stores lastError"
            ],
            "abstractMethods": ["start(): void", "stop(): void", "fetch(): Promise<any>"]
        },
        "pseudocode": """// Abstract Base Feed Contract
class Feed {
  #id; #name; #endpoints; #status;
  #lastFetchedAt; #lastLatencyMs; #consecutiveFailures; #lastError;

  constructor(id, name, endpoints) {
    if (new.target === Feed) throw TypeError("Cannot construct Feed directly");
    assertValid(id, 'Id', 'string');
    assertValid(name, 'Name', 'string');
    assertValid(endpoints, 'Endpoints', 'array');
    this.#id = id; this.#name = name;
    this.#endpoints = [...endpoints]; // defensive clone
    this.#status = 'IDLE';
  }

  get endpoints() { return [...this.#endpoints]; } // freeze boundary

  setStatus(s) {
    if (!VALID_STATUSES.has(s)) throw RangeError("Invalid status");
    this.#status = s;
  }

  recordSuccess(latency) {
    this.#lastFetchedAt = Date.now();
    this.#lastLatencyMs = latency;
    this.#consecutiveFailures = 0;
    this.#lastError = null;
  }

  recordFailure(err) {
    this.#consecutiveFailures += 1;
    this.#lastError = err;
  }

  start() { throw Error("Must implement start()"); }
  stop() { throw Error("Must implement stop()"); }
  fetch() { throw Error("Must implement fetch()"); }
}""",
        "enablingConcepts": [
            {
                "name": "Abstract Base Class via new.target Guard",
                "inventedFor": "JavaScript historically had no abstract classes like Java/C++. In ES6, new.target was introduced in the ECMA-262 spec to inspect which constructor was invoked by new. If new.target === BaseClass, direct construction is aborted at runtime.",
                "solvesForUs": "Prevents any engineer or test from accidentally creating an unconfigured, incomplete generic feed. Enforces that only specialized concrete pollers (like PollingFeed, WebSocketFeed) can be instantiated.",
                "details": "Throws a native TypeError if instantiated directly. Derived classes set new.target to the child class (e.g. PollingFeed), allowing execution of super() to succeed while enforcing contract completeness."
            },
            {
                "name": "Hard Encapsulation (#private fields)",
                "inventedFor": "Historically, JS used _id (convention) or closures/WeakMaps to simulate private state. Any rogue script or external UI component could mutate feed.status = 'COMPLETED' or wipe internal endpoints in-place.",
                "solvesForUs": "Total state integrity: #id, #status, #endpoints, and #consecutiveFailures cannot be read or written from outside except via getters and audited domain methods (setStatus, recordSuccess).",
                "details": "Stored in lexical private name environments in V8. Even Object.keys(), JSON.stringify(), or Reflect.ownKeys() cannot access or tamper with these slots."
            },
            {
                "name": "Defensive Copying (Immutability at Boundaries)",
                "inventedFor": "Passing array/object references directly in JS allows external callers to push(), pop(), or mutate array contents (aliasing bug). In 2012, security breaches and UI desync bugs regularly occurred from shared mutable arrays.",
                "solvesForUs": "In constructor: [...endpoints] ensures the caller cannot alter endpoints after passing them. In get endpoints(): return [...this.#endpoints] ensures consumers cannot alter the internal endpoints array.",
                "details": "Guarantees O(1) referential comparison safety and protects against unintended side effects without needing heavy external immutability libraries like Immutable.js."
            },
            {
                "name": "Circuit Breaker Telemetry & Health Tracking",
                "inventedFor": "In enterprise microservices (Michael Nygard's 'Release It!'), failing remote dependencies must be flagged before they overwhelm system memory and network sockets.",
                "solvesForUs": "recordSuccess and recordFailure maintain consecutive failure counts and latencies. This enables transition to DEGRADED status when latency spikes or failures breach thresholds.",
                "details": "Zero-allocation state tracking: stores raw timestamps and latency numbers directly on the instance for instant telemetry ingestion."
            }
        ]
    },
    {
        "id": "errors.js",
        "path": "src/feeds/errors.js",
        "name": "errors.js",
        "type": "src",
        "cluster": "errors",
        "category": "Error Telemetry Hierarchy",
        "color": "#ff007f",
        "pos": [-45, -15, 10],
        "contract": {
            "kind": "ES6 Class Inheritance Hierarchy",
            "classes": [
                "FeedError extends Error { constructor(message: string, feedId: string) }",
                "NetworkError extends FeedError { constructor(message: string, feedId: string, statusCode: number) }",
                "ParseError extends FeedError { constructor(message: string, feedId: string) }"
            ],
            "invariants": [
                "Every error carries .feedId for instant telemetry correlation",
                "NetworkError exposes .statusCode for HTTP triage (401, 429, 500, 503)",
                "Preserves proper prototype chain for instanceof checks (e.g. err instanceof FeedError === true)"
            ]
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
                "inventedFor": "Standard JS Error only provides message and stack trace. In multi-tenant streaming engines, generic errors fail to tell which feed crashed, whether it was network-level, or schema malformation.",
                "solvesForUs": "Differentiates network timeouts (retryable with backoff) from schema parse errors (fatal dirty data that must be quarantined).",
                "details": "Extending Error with super(message) sets up native stack capture in V8. Stamping feedId and statusCode directly on the instance enables automated triage in telemetry ring buffers."
            },
            {
                "name": "Polymorphic Error Handling (instanceof discrimination)",
                "inventedFor": "Prevents brittle string-matching on error.message (e.g. err.message.includes('fetch')).",
                "solvesForUs": "The engine catch blocks can cleanly branch: if (err instanceof NetworkError) handleRetry(); else if (err instanceof ParseError) quarantinePayload();",
                "details": "Symbol.hasInstance and prototype chain traversal allow accurate type discrimination without runtime reflection cost."
            }
        ]
    },
    {
        "id": "pipeline.js",
        "path": "src/feeds/pipeline.js",
        "name": "pipeline.js",
        "type": "src",
        "cluster": "pipeline",
        "category": "Pure Functional Ingestion Engine",
        "color": "#7000ff",
        "pos": [15, 20, 10],
        "contract": {
            "kind": "Curried Higher-Order Pipeline Functions",
            "exports": [
                "validateSchema(requiredFields: string[]): (data: object) => object",
                "normalizeTimestamps(timestampField?: string): (data: object) => object",
                "enrichFeedMetadata(feedId: string): (data: object) => object",
                "normalizerFactory(config: {feedId, requiredFields?, timestampField?}): (rawInput: string | object) => NormalizedMetricEvent"
            ],
            "invariants": [
                "Zero mutation: returns new defensive shallow copy ({ ...data }) at each stage",
                "Unary stages: every curried function takes exactly one parameter (data) to be composable by pipe()",
                "Epoch normalization: converts seconds (<10^10) to ms (*1000), parses ISO-8601 strings, defaults to Date.now()"
            ]
        },
        "pseudocode": """// Curried Pipeline Stages
export const validateSchema = (requiredFields) => (data) => {
  if (typeof data !== 'object' || data === null) throw new ParseError('Payload must be non-null object');
  for (const field of requiredFields) {
    if (data[field] === undefined || data[field] === null) {
      throw new ParseError(`Missing required field: ${field}`);
    }
  }
  return data;
};

export const normalizeTimestamps = (timestampField = 'timestamp') => (data) => {
  let raw = data[timestampField];
  let ts = Date.now();
  if (typeof raw === 'string') ts = Date.parse(raw) || Date.now();
  if (typeof raw === 'number') ts = raw < 1e10 ? raw * 1000 : raw; // sec vs ms
  return { ...data, [timestampField]: ts };
};

export const enrichFeedMetadata = (feedId) => (data) => {
  if (typeof feedId !== 'string') throw TypeError('FeedId must be string');
  return { ...data, feedId, ingestedAt: Date.now() };
};

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
                "inventedFor": "Haskell Curry & Moses Schönfinkel formalized currying in combinatory logic. pipe() and compose() require pure unary functions f(x). By pre-supplying configuration (e.g. requiredFields), currying produces unary workers ready for pipeline chaining.",
                "solvesForUs": "Allows the creation of specialized data processors per feed (USGS Earthquake, Open-Meteo, CoinGecko) via config without duplicating transformation plumbing.",
                "details": "The outer function captures configuration in its closure; the returned unary function receives streaming data payloads sequentially."
            },
            {
                "name": "Point-Free Style & Linear Flow Composition",
                "inventedFor": "Unix pipes (cat | grep | awk) proved in 1973 that simple tools chained together eliminate monolithic spaghetti and intermediate mutable state.",
                "solvesForUs": "Data transitions through raw string -> parsed object -> schema validated -> timestamp normalized -> enriched event in one linear, readable pipe() call.",
                "details": "Eliminates temporary variables, try-catch pollution inside business logic, and ensures intermediate results are garbage collected efficiently."
            },
            {
                "name": "Epoch Thresholding (Seconds vs Milliseconds Normalization)",
                "inventedFor": "Unix timestamps (POSIX) are in seconds since 1970 (~1.7e9 today). JavaScript Date uses milliseconds (~1.7e12). Mixing them causes dates to display in 1970 or year 53000.",
                "solvesForUs": "Checks if raw timestamp < 10,000,000,000 (10 billion). If so, it is seconds -> multiplies by 1000. If >= 10 billion, it is already milliseconds.",
                "details": "Bulletproof handling of heterogeneous external APIs (e.g. USGS sends ms, crypto APIs send seconds, weather APIs send ISO strings)."
            }
        ]
    },
    {
        "id": "PollingFeed.js",
        "path": "src/feeds/PollingFeed.js",
        "name": "PollingFeed.js",
        "type": "src",
        "cluster": "feeds",
        "category": "Async Motor / Polling Engine",
        "color": "#00ff66",
        "pos": [-15, 30, -10],
        "contract": {
            "kind": "Concrete Feed Implementation",
            "inherits": "Feed",
            "plannedFeatures": [
                "constructor(id, name, endpoints, intervalMs, normalizer)",
                "start(): kicks off timer loop, prevents double-start",
                "stop(): cleans up timer, aborts active fetch via AbortController",
                "fetch(): executes GET with AbortSignal, pipes through normalizer, dispatches to event bus"
            ],
            "invariants": [
                "GC-safe interval identity: timerId tracked on instance, cleared in stop()",
                "No overlapping polls: subsequent poll scheduled only after previous poll completes",
                "Circuit breaker integration: marks status DEGRADED if consecutiveFailures > threshold"
            ]
        },
        "pseudocode": """// Polling Engine Blueprint
class PollingFeed extends Feed {
  #intervalMs;
  #timerId = null;
  #abortController = null;
  #normalizer;

  constructor(id, name, endpoints, intervalMs = 5000, normalizer) {
    super(id, name, endpoints);
    this.#intervalMs = intervalMs;
    this.#normalizer = normalizer;
  }

  async fetch() {
    this.#abortController = new AbortController();
    const start = performance.now();
    try {
      this.setStatus('FETCHING');
      const res = await fetch(this.endpoints[0], { signal: this.#abortController.signal });
      if (!res.ok) throw new NetworkError(res.statusText, this.id, res.status);
      const text = await res.text();
      const event = this.#normalizer(text);
      this.recordSuccess(performance.now() - start);
      this.setStatus('CONNECTED');
      return event;
    } catch (err) {
      this.recordFailure(err);
      this.setStatus(this.consecutiveFailures >= 3 ? 'DEGRADED' : 'ERROR');
      throw err;
    }
  }

  start() {
    if (this.#timerId) return; // prevent duplicate loops
    const loop = async () => {
      try { await this.fetch(); } catch (e) {}
      if (this.#timerId) this.#timerId = setTimeout(loop, this.#intervalMs);
    };
    loop();
  }

  stop() {
    clearTimeout(this.#timerId);
    this.#timerId = null;
    this.#abortController?.abort();
    this.setStatus('IDLE');
  }
}""",
        "enablingConcepts": [
            {
                "name": "GC-Safe Interval Identity & Memory Leak Elimination",
                "inventedFor": "Single Page Apps (SPAs) left open for days crashed because setInterval retained references to dead components, preventing V8 garbage collection.",
                "solvesForUs": "Tracking timer IDs and explicitly clearing them on stop() or teardown allows V8's Mark-and-Sweep GC to reclaim the feed instance immediately.",
                "details": "Replaces crude setInterval with recursive setTimeout to guarantee no poll overlaps under network latency spikes."
            },
            {
                "name": "Cooperative In-Flight Cancellation (AbortController)",
                "inventedFor": "DOM AbortController standard (WHATWG) was created in 2017 to provide a standardized way to cancel fetch requests and DOM events.",
                "solvesForUs": "When a feed is stopped, paused, or page unmounts, in-flight HTTP requests are immediately aborted. Eliminates zombie responses updating state out-of-order.",
                "details": "Passes abortController.signal to fetch(). Calling abort() rejects the promise with DOMException ('AbortError'), freeing socket connections."
            }
        ]
    },
    {
        "id": "helpers.js",
        "path": "utils/helpers.js",
        "name": "helpers.js",
        "type": "utils",
        "cluster": "utils",
        "category": "Functional Combinators & Safe Parsers",
        "color": "#ffb700",
        "pos": [30, -5, 0],
        "contract": {
            "kind": "Utility Module",
            "exports": [
                "pipe(...funcs): (val: any) => any — left-to-right composition",
                "compose(...funcs): (val: any) => any — right-to-left mathematical composition",
                "parseJson(raw: string | object): object — safe JSON parser throwing ParseError",
                "capitalize(s: string): string — string capitalizer"
            ]
        },
        "pseudocode": """export const pipe = (...funcs) => (val) =>
  funcs.reduce((prev, fn) => fn(prev), val);

export const compose = (...funcs) => (val) =>
  funcs.reduceRight((prev, fn) => fn(prev), val);

export const parseJson = (raw) => {
  if (typeof raw !== 'string') return raw;
  try {
    return JSON.parse(raw);
  } catch (err) {
    throw new ParseError(err.message, 'unknown');
  }
};""",
        "enablingConcepts": [
            {
                "name": "Left-to-Right Pipeline Composition (pipe)",
                "inventedFor": "Mathematical function composition is naturally right-to-left: f(g(h(x))). In human reading and code review, left-to-right pipeline flow pipe(h, g, f) is dramatically easier to comprehend.",
                "solvesForUs": "Transforms raw text into a fully validated, normalized event through a declarative sequence of independent, testable transforms.",
                "details": "Implemented via Array.prototype.reduce: funcs.reduce((acc, fn) => fn(acc), initialValue)."
            },
            {
                "name": "Safe Boundary Exception Shielding (parseJson)",
                "inventedFor": "Native JSON.parse() throws an unhelpful SyntaxError with no domain context, crashing whole render trees if an API returns HTML (e.g. 502 Bad Gateway page).",
                "solvesForUs": "Wraps JSON.parse in try/catch and converts SyntaxError into domain ParseError tagged with feed telemetry metadata.",
                "details": "Handles passthrough if raw input is already an object, preventing redundant serialization roundtrips."
            }
        ]
    },
    {
        "id": "assertions.js",
        "path": "utils/assertions.js",
        "name": "assertions.js",
        "type": "utils",
        "cluster": "assertions",
        "category": "Defensive Invariant Assertion Guard",
        "color": "#ff5500",
        "pos": [-10, -25, -5],
        "contract": {
            "kind": "Assertion Layer",
            "exports": ["assertValid(value: any, label: string, type: 'string' | 'number' | 'array'): void"],
            "errors": [
                "TypeError if value does not match expected primitive/reference type",
                "RangeError if value is empty string or empty array"
            ]
        },
        "pseudocode": """export function assertValid(value, label, type) {
  const rules = VALIDATORS[type];
  if (!rules) throw new TypeError(`Unknown validation type: ${type}`);
  if (!rules.checkType(value)) throw new TypeError(`${label} has invalid type`);
  if (rules.isEmpty(value)) throw new RangeError(`${label} cannot be empty`);
}""",
        "enablingConcepts": [
            {
                "name": "Fail-Fast Design & Boundary Invariant Enforcement",
                "inventedFor": "Jim Gray (Turing Award winner) introduced fail-fast systems: software should immediately halt on invalid inputs rather than continuing with corrupt data and failing mysteriously 10 steps later.",
                "solvesForUs": "Validates feed ID, feed name, and endpoint URLs right in the constructor before allocating system resources or timers.",
                "details": "Separates type correctness (TypeError) from domain bounds correctness (RangeError) for deterministic error classification."
            }
        ]
    },
    {
        "id": "validators.js",
        "path": "utils/validators.js",
        "name": "validators.js",
        "type": "utils",
        "cluster": "validators",
        "category": "Type & Domain Predicate Rulebook",
        "color": "#e056fd",
        "pos": [0, -35, 10],
        "contract": {
            "kind": "Rule Dictionary Object",
            "rules": {
                "string": "checkType: typeof v === 'string', isEmpty: v.trim() === ''",
                "number": "checkType: typeof v === 'number' && !Number.isNaN(v), isEmpty: false",
                "array": "checkType: Array.isArray(v), isEmpty: length === 0 || any element is blank string"
            }
        },
        "pseudocode": """export const VALIDATORS = {
  string: {
    checkType: (v) => typeof v === 'string',
    isEmpty: (v) => v.trim() === '',
  },
  number: {
    checkType: (v) => typeof v === 'number' && !Number.isNaN(v),
    isEmpty: (v) => false,
  },
  array: {
    checkType: (v) => Array.isArray(v),
    isEmpty: (v) => Array.isArray(v) && (v.length === 0 || v.some(e => typeof e === 'string' && e.trim() === '')),
  },
};""",
        "enablingConcepts": [
            {
                "name": "Data-Driven Validation Strategy Pattern",
                "inventedFor": "Avoids hardcoded if/else ladders scattered across constructor bodies.",
                "solvesForUs": "Consolidates all predicate logic into a clean, extensible dictionary. Adding a new validated type (e.g. url, port) requires touching only this file.",
                "details": "Uses strict Array.isArray and Number.isNaN checks to defend against classic JS type pitfalls (typeof null === 'object', typeof NaN === 'number')."
            }
        ]
    },
    {
        "id": "curry.js",
        "path": "kata/curry.js",
        "name": "curry.js",
        "type": "kata",
        "cluster": "kata",
        "category": "Currying Crucible (L1–L5 FAANG Drills)",
        "color": "#00d2d3",
        "pos": [45, 10, -15],
        "contract": {
            "kind": "Algorithm & Language Mechanics Crucible",
            "exports": [
                "sum3(a)(b)(c): number (Fixed arity)",
                "infiniteSum(a)(b)...(): number (Variadic with empty terminator)",
                "add(a)(b)...: returns function with .valueOf() override for coercion sum",
                "curry(fn): returns curried wrapper supporting arbitrary arity chunks until fn.length reached",
                "curryWithPlaceholder(fn): staff-level placeholder (_) argument accumulator"
            ]
        },
        "pseudocode": """// General Purpose Universal Curry
export function curry(fn) {
  return function curried(...args) {
    if (args.length >= fn.length) {
      return fn(...args);
    }
    return function (...next) {
      return curried(...args, ...next);
    };
  };
}

// Coercion Curry via valueOf
export function infiniteSum2(a) {
  if (a === undefined) return 0;
  const next = (b) => (b !== undefined ? infiniteSum2(a + b) : a);
  next.valueOf = () => a;
  return next;
}""",
        "enablingConcepts": [
            {
                "name": "Function Arity (fn.length) & Rest Parameter Traps",
                "inventedFor": "ECMA-262 defines Function.prototype.length as the number of formal parameters before the first default parameter. Rest parameters (...rest) do not increment length.",
                "solvesForUs": "Powers our universal curry() helper which inspects fn.length to decide whether to invoke the target function or return another curried collector.",
                "details": "Knowing arity limits is critical when currying higher-order functions that accept default arguments or rest parameters."
            },
            {
                "name": "Value Coercion & Symbol.toPrimitive / valueOf Overriding",
                "inventedFor": "JavaScript type conversion rules (ToPrimitive abstract operation) query [Symbol.toPrimitive](), valueOf(), and toString() when an object encounters arithmetic (+, ==).",
                "solvesForUs": "Enables infinite function chaining add(1)(2)(3) to evaluate directly in numeric expressions (+ 4 === 10) without needing an explicit invocation terminator.",
                "details": "Attaching valueOf to the returned closure function intercepts JS engine coercion seamlessly."
            }
        ]
    },
    {
        "id": "Feed.test.js",
        "path": "tests/src/feeds/Feed.test.js",
        "name": "Feed.test.js",
        "type": "test",
        "cluster": "test",
        "category": "Behavior-Driven Unit Verification",
        "color": "#1dd1a1",
        "pos": [-30, 45, 10],
        "contract": {
            "kind": "Vitest Test Suite",
            "scenariosCovered": [
                "Instantiation rejection of abstract base Feed directly",
                "Concrete subclass instantiation and property reflection",
                "Defensive array copy mutation proof (pushing to endpoints copy doesn't mutate feed)",
                "Status validation & RangeError on bogus status",
                "Failure tracking and success recovery counter resets"
            ]
        },
        "pseudocode": """describe('Feed.js', () => {
  it('throws on direct construction', () => {
    expect(() => new Feed('id', 'name', ['url'])).toThrow(TypeError);
  });

  it('guarantees defensive copying', () => {
    const feed = new TestFeed('id', 'name', ['url1']);
    const copy = feed.endpoints;
    copy.push('url2');
    expect(feed.endpoints).not.toEqual(copy);
  });
});""",
        "enablingConcepts": [
            {
                "name": "Mathematical Proof via Isolated Vitest BDD Suites",
                "inventedFor": "Behavior-Driven Development (Dan North) focuses tests on system invariants and contracts rather than internal implementation details.",
                "solvesForUs": "Proves that Feed.js remains an airtight boundary preventing mutation leaks and contract violations across rapid refactoring.",
                "details": "Executes in ESM native environment with sub-millisecond execution times in Vitest."
            }
        ]
    },
    {
        "id": "pipeline.test.js",
        "path": "tests/src/feeds/pipeline.test.js",
        "name": "pipeline.test.js",
        "type": "test",
        "cluster": "test",
        "category": "Data Transformation Pipeline Verification",
        "color": "#54a0ff",
        "pos": [35, 40, -5],
        "contract": {
            "kind": "Vitest Test Suite",
            "scenariosCovered": [
                "validateSchema passes valid objects, throws ParseError on null or missing fields",
                "normalizeTimestamps handles ISO string dates, POSIX seconds (<1e10), ms numbers, and invalid fallbacks",
                "enrichFeedMetadata attaches valid feedId and ingestedAt timestamp",
                "normalizerFactory integrates all 4 stages into end-to-end transformation"
            ]
        },
        "pseudocode": """describe('pipeline.js', () => {
  it('normalizes seconds to milliseconds', () => {
    const res = normalizeTimestamps('timestamp')({ timestamp: 60 });
    expect(res.timestamp).toBe(60000);
  });

  it('enriches metadata', () => {
    const res = enrichFeedMetadata('geo-1')({ value: 10 });
    expect(res.feedId).toBe('geo-1');
    expect(typeof res.ingestedAt).toBe('number');
  });
});""",
        "enablingConcepts": [
            {
                "name": "Boundary Fuzzing & Schema Invariant Testing",
                "inventedFor": "APIs frequently send subtle variations (null fields, undefined, string numbers, epoch in seconds). Testing all input permutations prevents unhandled runtime exceptions.",
                "solvesForUs": "Validates every branch of normalizeTimestamps and validateSchema under boundary and malicious inputs.",
                "details": "Tests against JSON string input, plain object input, corrupt strings, and out-of-order fields."
            }
        ]
    },
    {
        "id": "errors.test.js",
        "path": "tests/src/feeds/errors.test.js",
        "name": "errors.test.js",
        "type": "test",
        "cluster": "test",
        "category": "Prototype Inheritance Verification",
        "color": "#ff6b6b",
        "pos": [-55, -5, -15],
        "contract": {
            "kind": "Vitest Test Suite",
            "scenariosCovered": [
                "FeedError inherits from Error, sets message, name, feedId",
                "NetworkError inherits from FeedError and Error, sets statusCode",
                "ParseError inherits from FeedError and Error, sets name"
            ]
        },
        "pseudocode": """it('verifies prototype chain', () => {
  const err = new NetworkError('timeout', 'f1', 504);
  expect(err instanceof NetworkError).toBe(true);
  expect(err instanceof FeedError).toBe(true);
  expect(err instanceof Error).toBe(true);
});""",
        "enablingConcepts": [
            {
                "name": "Prototype Chain Verification",
                "inventedFor": "Transpilers (Babel/TypeScript) historically broke Error inheritance (setting err instanceof CustomError to false).",
                "solvesForUs": "Guarantees that native ES6 class inheritance correctly retains instanceof checks in modern Node/V8 runtimes.",
                "details": "Verifies that catch (e) { if (e instanceof FeedError) ... } behaves deterministically."
            }
        ]
    }
]

# Connecting edges: showing dependencies, data flow, and enabling concepts
edges = [
    {
        "source": "Feed.js",
        "target": "assertions.js",
        "type": "imports",
        "label": "Boundary Invariant Checking",
        "concept": "assertValid enforces non-empty string and array types in constructor"
    },
    {
        "source": "assertions.js",
        "target": "validators.js",
        "type": "delegates",
        "label": "Predicate Rule Lookup",
        "concept": "VALIDATORS dictionary supplies type check and emptiness definitions"
    },
    {
        "source": "PollingFeed.js",
        "target": "Feed.js",
        "type": "extends",
        "label": "Subclass Inheritance",
        "concept": "Inherits private fields, status state-machine, and telemetry methods"
    },
    {
        "source": "pipeline.js",
        "target": "helpers.js",
        "type": "imports",
        "label": "Functional Pipe & Parse",
        "concept": "Uses pipe() to compose unary steps and parseJson() to shield SyntaxErrors"
    },
    {
        "source": "pipeline.js",
        "target": "errors.js",
        "type": "imports",
        "label": "Telemetry Error Raising",
        "concept": "Throws ParseError when incoming schema is malformed or null"
    },
    {
        "source": "helpers.js",
        "target": "errors.js",
        "type": "imports",
        "label": "Safe Parsing Shield",
        "concept": "parseJson catches JSON.parse SyntaxError and re-raises as ParseError"
    },
    {
        "source": "curry.js",
        "target": "pipeline.js",
        "type": "conceptual",
        "label": "Underlying Currying Foundation",
        "concept": "Currying mechanics mastered in curry.js enable validateSchema and enrichFeedMetadata unary stages"
    },
    {
        "source": "PollingFeed.js",
        "target": "pipeline.js",
        "type": "consumes",
        "label": "Payload Normalization",
        "concept": "PollingFeed.fetch() passes raw response text into normalizerFactory"
    },
    {
        "source": "PollingFeed.js",
        "target": "errors.js",
        "type": "throws",
        "label": "Network Telemetry Error",
        "concept": "Throws NetworkError with HTTP statusCode when response.ok is false"
    },
    {
        "source": "Feed.test.js",
        "target": "Feed.js",
        "type": "tests",
        "label": "Behavioral Contract Verification",
        "concept": "Verifies new.target guard, defensive copying, and status transitions"
    },
    {
        "source": "pipeline.test.js",
        "target": "pipeline.js",
        "type": "tests",
        "label": "Pipeline Unit Verification",
        "concept": "Verifies schema validation, timestamp normalization, and metadata injection"
    },
    {
        "source": "errors.test.js",
        "target": "errors.js",
        "type": "tests",
        "label": "Inheritance Chain Verification",
        "concept": "Verifies instanceof prototype integrity across FeedError subclasses"
    }
]

# Write out concept_graph.json
with open(os.path.join(BASE_DIR, 'docs/visualizer/concept_graph.json'), 'w', encoding='utf-8') as f:
    json.dump({"nodes": nodes, "edges": edges}, f, indent=2)

print("concept_graph.json generated successfully.")
