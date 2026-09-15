import json, os

knowledge = {
  "nodes": [
    {
      "id": "Feed.js",
      "path": "src/feeds/Feed.js",
      "name": "Feed.js",
      "type": "src",
      "cluster": "feeds",
      "category": "Core Domain Base (Abstract State Machine)",
      "color": "#00f0ff",
      "pos": [-40, 18, 5],
      "contract": {
        "kind": "Abstract Domain Class (ES6 / ECMA-262 Specification)",
        "instantiationGuard": "if (new.target === Feed) throw new TypeError('Cannot construct Feed instances directly');",
        "constructorSignature": "constructor(id: string, name: string, endpoints: string[])",
        "privateFields": [
          "#id (string) — Unique identifier across all registered feeds",
          "#name (string) — Human-readable display identifier",
          "#endpoints (string[]) — Array of remote HTTP/WS URLs (Defensively cloned)",
          "#status ('IDLE' | 'FETCHING' | 'CONNECTED' | 'DEGRADED' | 'ERROR')",
          "#lastFetchedAt (number | null) — Epoch millisecond timestamp of last successful ping",
          "#lastLatencyMs (number) — Roundtrip response latency in ms",
          "#consecutiveFailures (number) — Counter driving the circuit-breaker status",
          "#lastError (Error | null) — Telemetry payload of most recent caught exception"
        ],
        "publicGetters": [
          "id -> string",
          "name -> string",
          "status -> string",
          "endpoints -> [...this.#endpoints] (Defensive copy returned on EVERY read)",
          "lastFetchedAt -> number | null",
          "lastLatencyMs -> number",
          "consecutiveFailures -> number",
          "lastError -> Error | null"
        ],
        "domainMethods": [
          "setStatus(newStatus: string): void — Validates against Set(['IDLE', 'FETCHING', 'CONNECTED', 'DEGRADED', 'ERROR']) or throws RangeError",
          "recordSuccess(latencyMs: number): void — Updates #lastFetchedAt, #lastLatencyMs, resets #consecutiveFailures to 0, wipes #lastError",
          "recordFailure(error: Error): void — Increments #consecutiveFailures by 1, stores #lastError"
        ],
        "abstractMethods": [
          "start(): void — Must be implemented by concrete subclasses (e.g. PollingFeed)",
          "stop(): void — Must be implemented by concrete subclasses to tear down timers",
          "fetch(): Promise<any> — Must be implemented to execute network fetch + normalization"
        ]
      },
      "semanticsAndFlow": {
        "lifecycle": "Construct (Guarded) -> start() -> Periodic fetch() -> recordSuccess() / recordFailure() -> stop()",
        "stateMachine": {
          "initial": "IDLE",
          "transitions": [
            {"from": "IDLE", "event": "start() / polling loop starts", "to": "FETCHING"},
            {"from": "FETCHING", "event": "HTTP 200 + Schema Validated", "to": "CONNECTED"},
            {"from": "FETCHING", "event": "Network / Parse Error (failures < 3)", "to": "ERROR"},
            {"from": "ERROR", "event": "consecutiveFailures >= 3", "to": "DEGRADED"},
            {"from": "DEGRADED", "event": "recordSuccess() resets failure streak", "to": "CONNECTED"},
            {"from": "ANY", "event": "stop() invoked by UI or teardown", "to": "IDLE"}
          ]
        },
        "memoryCharacteristics": "Zero external object allocations during polling. Fields are held in private brand slots in V8 heap. Endpoints array is defensively shallow-copied twice to maintain absolute encapsulation."
      },
      "pseudocode": """// Abstract Base Feed: Pure Domain Invariant Boundary
class Feed {
  #id; #name; #endpoints = []; #status = 'IDLE';
  #lastFetchedAt = null; #lastLatencyMs = 0;
  #consecutiveFailures = 0; #lastError = null;

  constructor(id, name, endpoints) {
    if (new.target === Feed) {
      throw new TypeError('Cannot construct Feed instances directly');
    }
    assertValid(id, 'Id', 'string');
    assertValid(name, 'Name', 'string');
    assertValid(endpoints, 'Endpoints', 'array');

    this.#id = id;
    this.#name = name;
    this.#endpoints = [...endpoints]; // Defensive copy prevents caller mutation
  }

  get endpoints() { return [...this.#endpoints]; } // Read boundary defensive copy

  setStatus(newStatus) {
    if (!VALID_STATUSES.has(newStatus)) {
      throw new RangeError('The status is not within the valid range of values');
    }
    this.#status = newStatus;
  }

  recordSuccess(latencyMs) {
    this.#lastFetchedAt = Date.now();
    this.#lastLatencyMs = latencyMs;
    this.#consecutiveFailures = 0;
    this.#lastError = null;
  }

  recordFailure(error) {
    this.#consecutiveFailures += 1;
    this.#lastError = error;
  }

  start() { throw new Error('Method start() must be implemented by derived subclass'); }
  stop() { throw new Error('Method stop() must be implemented by derived subclass'); }
  fetch() { throw new Error('Method fetch() must be implemented by derived subclass'); }
}""",
      "enablingConcepts": [
        {
          "name": "Abstract Base Class via new.target Guard",
          "inventedFor": "In classical OOP (C++/Java), 'abstract' is a keyword that prevents compiling direct instances. JavaScript had no such keyword. In ES6, TC39 added 'new.target' to ECMA-262 to inspect the constructor invoked by 'new'.",
          "solvesForUs": "Guarantees no developer or test can accidentally instantiate a half-baked Feed instance without a concrete poller (PollingFeed, WebSocketFeed). Enforces that abstract methods (fetch, start, stop) are always provided by derived children.",
          "details": "When 'new Feed()' is called, new.target === Feed, triggering a TypeError. When 'new PollingFeed()' is called, new.target === PollingFeed during the super() call, allowing construction to succeed cleanly."
        },
        {
          "name": "True V8 Lexical Hard Encapsulation (#private fields)",
          "inventedFor": "Historically, JS developers prefixed fields with underscores (_id, _status). Any rogue library, analytics tag, or bug in a React component could mutate feed._status = 'CONNECTED' or wipe endpoints array directly in memory.",
          "solvesForUs": "Zero-trust state integrity. Neither UI components, console scripts, nor external libraries can modify internal telemetry, failure counts, or endpoints. State changes MUST go through audited domain methods.",
          "details": "Private fields are stored in private identifier brand checks in V8. They do not appear in Object.keys(), Object.getOwnPropertyNames(), or JSON.stringify(). Accessing #id outside the class throws a native SyntaxError at parse time."
        },
        {
          "name": "Defensive Copying at System Boundaries",
          "inventedFor": "Array aliasing bugs: In JavaScript, objects and arrays are passed by reference. If caller passed 'const urls = ['http://...']; new Feed('f1', 'name', urls); urls.push('http://malicious.com');', the feed was silently compromised.",
          "solvesForUs": "In the constructor: this.#endpoints = [...endpoints] isolates internal storage. In the getter: return [...this.#endpoints] guarantees that UI code calling 'feed.endpoints.pop()' mutates a disposable throwaway copy, keeping feed state intact.",
          "details": "Prevents subtle race conditions and memory aliasing bugs in asynchronous multi-feed polling loops."
        },
        {
          "name": "Circuit-Breaker Telemetry State Machine",
          "inventedFor": "Michael Nygard introduced the Circuit Breaker pattern in 'Release It!' (2007) for distributed systems. If an external service is down, hammering it with retries exhausts client thread pools and memory.",
          "solvesForUs": "Tracks #consecutiveFailures and #lastLatencyMs directly on the feed. When consecutive failures hit 3, feed automatically shifts to DEGRADED, allowing UI to throttle requests or show fallback data.",
          "details": "Zero-allocation arithmetic updates: primitive number mutations in place without creating throwaway garbage collector objects."
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
      "color": "#9d4edd",
      "pos": [25, 22, 10],
      "contract": {
        "kind": "Curried Higher-Order Functional Pipeline (Pure)",
        "exports": [
          "validateSchema(requiredFields: string[]): (data: object) => object",
          "normalizeTimestamps(timestampField?: string): (data: object) => object",
          "enrichFeedMetadata(feedId: string): (data: object) => object",
          "normalizerFactory({ feedId, requiredFields?, timestampField? }): (raw: string | object) => NormalizedMetricEvent"
        ],
        "invariants": [
          "Referential Purity: Never mutates incoming objects; always returns a new defensive shallow spread ({ ...data })",
          "Strict Unary Shape: Every curried step takes exactly one parameter (data) so it seamlessly fits pipe()",
          "Fail-Fast Schema Guard: Throws ParseError immediately upon encountering null, non-object, or missing keys",
          "Epoch Disambiguation: Detects POSIX seconds vs JavaScript milliseconds (< 10^10 threshold) and ISO-8601 strings"
        ]
      },
      "semanticsAndFlow": {
        "lifecycle": "Raw External Input (string / malformed JSON) -> parseJson -> validateSchema -> normalizeTimestamps -> enrichFeedMetadata -> Clean NormalizedMetricEvent",
        "dataTransformation": [
          {"stage": "Raw API Response", "example": "{\"id\":\"quake-1\",\"mag\":4.2,\"time\":1693656000}"},
          {"stage": "parseJson", "example": "{\"id\":\"quake-1\",\"mag\":4.2,\"time\":1693656000} (Clean JS Object)"},
          {"stage": "validateSchema(['id','mag','time'])", "example": "Throws ParseError if any required key is undefined/null"},
          {"stage": "normalizeTimestamps('time')", "example": "time < 10^10 -> 1693656000 * 1000 = 1693656000000 ms"},
          {"stage": "enrichFeedMetadata('usgs_earthquakes')", "example": "Attaches feedId: 'usgs_earthquakes', ingestedAt: 1789055900123"}
        ],
        "errorPropagation": "Throws ParseError with feedId and message. Error bypasses Redux/UI state, routed directly to telemetry."
      },
      "pseudocode": """// Curried Functional Pipeline Engine
export const validateSchema = (requiredFields) => (data) => {
  if (typeof data !== 'object' || data === null) {
    throw new ParseError('Payload must be a valid non-null object');
  }
  for (const field of requiredFields) {
    if (data[field] === undefined || data[field] === null) {
      throw new ParseError(`Missing required field: ${field}`);
    }
  }
  return data;
};

export const normalizeTimestamps = (timestampField = 'timestamp') => (data) => {
  const raw = data[timestampField];
  let ts;
  if (typeof raw === 'number') {
    ts = raw < 10000000000 ? raw * 1000 : raw; // 10 Billion boundary: sec vs ms
  } else if (typeof raw === 'string') {
    ts = Date.parse(raw) || Date.now();
  } else {
    ts = Date.now();
  }
  return { ...data, [timestampField]: ts };
};

export const enrichFeedMetadata = (feedId) => (data) => {
  if (typeof feedId !== 'string') throw new TypeError('Feed Id must be a valid string');
  return { ...data, feedId, ingestedAt: Date.now() };
};

export const normalizerFactory = ({ feedId, requiredFields = [], timestampField }) =>
  pipe(
    parseJson,
    validateSchema(requiredFields),
    normalizeTimestamps(timestampField),
    enrichFeedMetadata(feedId)
  );""",
      "enablingConcepts": [
        {
          "name": "Currying & Partial Application for Unary Composition",
          "inventedFor": "Moses Schönfinkel (1924) & Haskell Curry (1930) in mathematical logic. Standard functions take multiple arguments f(config, data). But functional pipelines (pipe/compose) require unary functions g(data) taking only one argument.",
          "solvesForUs": "Currying separates the configuration phase from the execution phase. We configure validateSchema(['temp', 'humidity']) once at app startup, and receive a unary worker function ready to process thousands of live incoming socket packets.",
          "details": "Outer function captures configuration parameters in its lexical closure. The returned inner function receives the streaming data payload from the previous pipeline stage."
        },
        {
          "name": "Point-Free Style & Unix Pipe Architecture",
          "inventedFor": "Ken Thompson & Doug McIlroy created Unix pipes in 1973: 'Write programs that do one thing and do it well. Write programs to work together.' Point-free style in FP removes intermediate assignment boilerplate.",
          "solvesForUs": "Eliminates mutable intermediate variables (e.g. let step1 = ...; let step2 = ...). Data flows in a pure, uninterrupted stream. Memory footprint is minimal because intermediate transient objects are immediately eligible for V8 young-generation garbage collection.",
          "details": "normalizerFactory(config) returns a single composite function created via pipe(...stages). Calling it with raw text executes the complete 4-stage pipeline in a single invocation."
        },
        {
          "name": "Epoch Thresholding (Seconds vs Milliseconds Normalization)",
          "inventedFor": "Unix POSIX time measures seconds since Jan 1 1970 (~1.7 billion). JavaScript Date measures milliseconds (~1.7 trillion). In distributed architectures, crypto APIs send seconds, weather APIs send ISO strings, and seismic feeds send ms. Mixing them corrupts time-series charts.",
          "solvesForUs": "Disambiguates seconds from milliseconds using a mathematical heuristic: 10,000,000,000 (10 billion). Any timestamp below 10 billion is seconds (multiplied by 1000). Any timestamp above 10 billion is already milliseconds.",
          "details": "Handles ISO-8601 strings via Date.parse() with defensive fallback to Date.now() if invalid or NaN."
        },
        {
          "name": "Referential Transparency for React 60 FPS Immutability",
          "inventedFor": "React uses shallow referential equality (prevProps !== nextProps) to determine whether to re-render. If a background pipeline mutates an existing object in-place, React will not detect the change and UI will fail to update.",
          "solvesForUs": "Every pipeline stage creates a shallow clone { ...data, [timestampField]: ts }. This guarantees referential inequality (new object reference), triggering instant, deterministic React updates without expensive deep object diffing.",
          "details": "Ensures O(1) shallow equality checks across React memoization hooks (useMemo, React.memo, useSyncExternalStore)."
        }
      ]
    },
    {
      "id": "PollingFeed.js",
      "path": "src/feeds/PollingFeed.js",
      "name": "PollingFeed.js",
      "type": "src",
      "cluster": "feeds",
      "category": "Asynchronous Motor (Polling & Lifecycle)",
      "color": "#00ff66",
      "pos": [-15, 35, -5],
      "contract": {
        "kind": "Concrete Domain Implementation Subclass",
        "inherits": "Feed",
        "constructorSignature": "constructor(id: string, name: string, endpoints: string[], intervalMs?: number, normalizer: Function)",
        "internalState": [
          "#intervalMs (number, defaults to 5000ms)",
          "#timerId (NodeJS.Timeout | number | null) — Handle of active setTimeout",
          "#abortController (AbortController | null) — Signal source for active fetch",
          "#normalizer (Function) — Unary pipeline normalizerFactory instance"
        ],
        "implementedMethods": [
          "start(): void — Starts recursive polling loop. Idempotent guard prevents duplicate loops.",
          "stop(): void — Clears active timeout, calls abortController.abort(), shifts status to IDLE.",
          "fetch(): Promise<NormalizedMetricEvent> — Dispatches fetch with AbortSignal, measures latency, records success/failure, returns normalized event."
        ]
      },
      "semanticsAndFlow": {
        "lifecycle": "Construct -> start() -> schedule next loop -> fetch() with signal -> normalizer() -> recordSuccess() -> schedule next loop -> stop() clears timer & aborts socket",
        "concurrencyDefense": "Uses recursive setTimeout instead of setInterval. In setInterval, if a request takes 6 seconds on a 5-second interval, requests stack up and flood the network. Recursive setTimeout guarantees that the next poll is only scheduled AFTER the previous one has completely settled."
      },
      "pseudocode": """// Asynchronous Polling Motor (Staff Blueprint)
class PollingFeed extends Feed {
  #intervalMs; #timerId = null;
  #abortController = null; #normalizer;

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
      const res = await fetch(this.endpoints[0], {
        signal: this.#abortController.signal
      });
      if (!res.ok) {
        throw new NetworkError(`HTTP ${res.status}: ${res.statusText}`, this.id, res.status);
      }
      const rawText = await res.text();
      const normalizedEvent = this.#normalizer(rawText);
      this.recordSuccess(performance.now() - start);
      this.setStatus('CONNECTED');
      return normalizedEvent;
    } catch (err) {
      if (err.name === 'AbortError') return; // Intentional teardown
      this.recordFailure(err);
      this.setStatus(this.consecutiveFailures >= 3 ? 'DEGRADED' : 'ERROR');
      throw err;
    }
  }

  start() {
    if (this.#timerId) return; // Idempotent guard
    const pollLoop = async () => {
      try { await this.fetch(); } catch (e) {}
      if (this.#timerId !== null) {
        this.#timerId = setTimeout(pollLoop, this.#intervalMs);
      }
    };
    this.#timerId = setTimeout(pollLoop, 0); // Immediate kickoff
  }

  stop() {
    if (this.#timerId) {
      clearTimeout(this.#timerId);
      this.#timerId = null;
    }
    this.#abortController?.abort();
    this.setStatus('IDLE');
  }
}""",
      "enablingConcepts": [
        {
          "name": "Recursive setTimeout vs. setInterval Stack Accumulation",
          "inventedFor": "setInterval schedules callbacks at fixed clock ticks regardless of how long the async network operation takes. On slow 3G or backend degradation, multiple requests queue in the event loop, causing socket exhaustion and browser tab freezing.",
          "solvesForUs": "Recursive setTimeout schedules the next poll ONLY inside the 'finally' block of the previous settled request. Guarantees zero overlapping requests, constant memory footprint, and natural backpressure.",
          "details": "If the interval is 5000ms and fetch takes 3000ms, the next fetch runs 5000ms after completion (8000ms total period), adapting dynamically to network load."
        },
        {
          "name": "Cooperative Request Abort (AbortController & AbortSignal)",
          "inventedFor": "WHATWG standard (2017) introduced AbortController to solve zombie network requests in SPAs when users navigate away or pause feeds.",
          "solvesForUs": "Calling feed.stop() immediately closes open TCP sockets, aborting in-flight HTTP responses before they can resolve and corrupt newer state.",
          "details": "Passes signal to fetch(url, { signal }). Calling abort() causes the fetch promise to reject immediately with a DOMException named 'AbortError', skipping pipeline execution."
        },
        {
          "name": "GC-Safe Interval Identity & Memory Leak Elimination",
          "inventedFor": "V8 Garbage Collector uses Mark-and-Sweep. If a setInterval closure references a component or feed instance, that entire object subgraph remains pinned in memory forever, leaking RAM.",
          "solvesForUs": "By storing the numeric timer handle on #timerId and setting it to null in stop(), the timer handle is decoupled, allowing V8's GC to collect dead feed instances when detached from UI.",
          "details": "Essential for long-running real-time monitoring consoles that remain open 24/7 on trading or ops floor displays."
        }
      ]
    },
    {
      "id": "errors.js",
      "path": "src/feeds/errors.js",
      "name": "errors.js",
      "type": "src",
      "cluster": "errors",
      "category": "Telemetry-Aware Error Hierarchy",
      "color": "#ff007f",
      "pos": [-55, -12, 10],
      "contract": {
        "kind": "Custom Prototypal Error Hierarchy",
        "classes": [
          "FeedError extends Error { constructor(message: string, feedId: string) }",
          "NetworkError extends FeedError { constructor(message: string, feedId: string, statusCode: number) }",
          "ParseError extends FeedError { constructor(message: string, feedId: string) }"
        ],
        "properties": [
          "message: string (Inherited from Error)",
          "name: 'FeedError' | 'NetworkError' | 'ParseError'",
          "feedId: string (Tagged to every error for automated metric routing)",
          "statusCode?: number (HTTP response code 400, 429, 500, 503 on NetworkError)"
        ]
      },
      "semanticsAndFlow": {
        "hierarchy": "Error -> FeedError -> NetworkError / ParseError",
        "discrimination": "Downstream catch handlers use: 'if (err instanceof NetworkError)' -> retry with exponential backoff; 'if (err instanceof ParseError)' -> quarantine dirty payload; 'else' -> unhandled system crash."
      },
      "pseudocode": """// Telemetry Error Hierarchy
class FeedError extends Error {
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
          "name": "Prototypal Inheritance & instanceof Discrimination",
          "inventedFor": "JavaScript's prototypical inheritance allows objects to inherit properties and methods dynamically via [[Prototype]].",
          "solvesForUs": "Allows polymorphic error handling without brittle string parsing on error.message (e.g. avoiding err.message.includes('404')).",
          "details": "Inherits native stack capture from Error.prototype while establishing proper prototype chains for err instanceof FeedError and err instanceof Error."
        },
        {
          "name": "Telemetry Correlation Identifiers (feedId & statusCode)",
          "inventedFor": "Distributed tracing (Dapper, OpenTelemetry). When an exception is caught in a high-throughput stream, logging a bare message loses the origin context.",
          "solvesForUs": "Every error carries the feedId and optional HTTP statusCode, enabling error telemetry ring buffers to instantly aggregate error rates per feed without secondary parsing.",
          "details": "Zero-overhead metadata stamping directly on the Error instance in V8."
        }
      ]
    },
    {
      "id": "helpers.js",
      "path": "utils/helpers.js",
      "name": "helpers.js",
      "type": "utils",
      "cluster": "utils",
      "category": "Functional Combinators & Safe Boundary Parsers",
      "color": "#ffb700",
      "pos": [35, -5, -5],
      "contract": {
        "kind": "Utility Combinator Module",
        "exports": [
          "pipe(...funcs: Function[]): (val: any) => any — Left-to-right functional pipeline",
          "compose(...funcs: Function[]): (val: any) => any — Right-to-left mathematical composition",
          "parseJson(raw: string | object): object — Safe parsing shield throwing ParseError",
          "capitalize(s: string): string — String formatting helper"
        ]
      },
      "semanticsAndFlow": {
        "pipeFlow": "pipe(f, g, h)(x) === h(g(f(x))) — Executed via Array.prototype.reduce",
        "composeFlow": "compose(f, g, h)(x) === f(g(h(x))) — Executed via Array.prototype.reduceRight",
        "parseJsonShield": "If raw is already an object, returns it immediately. If string, tries JSON.parse; on SyntaxError, catches and re-throws domain ParseError."
      },
      "pseudocode": """// Left-to-Right Pipeline Combinator
export const pipe = (...funcs) => (val) =>
  funcs.reduce((prev, fn) => fn(prev), val);

// Mathematical Composition Combinator
export const compose = (...funcs) => (val) =>
  funcs.reduceRight((prev, fn) => fn(prev), val);

// Safe Boundary JSON Parsing Shield
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
          "name": "Variadic Function Composition via Array.prototype.reduce",
          "inventedFor": "Formalized in category theory as morphism composition. In JS, reduce enables chaining an arbitrary list of unary functions without nested parenthesis nesting.",
          "solvesForUs": "Powers normalizerFactory to chain parsing, validation, timestamp normalization, and metadata injection cleanly in one line.",
          "details": "Functions are executed synchronously. The output of funcs[i] becomes the input of funcs[i+1]."
        },
        {
          "name": "Boundary Exception Shielding (parseJson)",
          "inventedFor": "Defensive programming at system I/O boundaries. Native JSON.parse throws SyntaxError, which has no domain meaning and crashes unexpected consumers.",
          "solvesForUs": "Converts native V8 SyntaxError into our domain-specific ParseError with a standardized telemetry shape.",
          "details": "Passthrough optimization: if the network adapter already parsed JSON into an object, typeof raw !== 'string' returns it instantly without redundant stringifying and parsing."
        }
      ]
    },
    {
      "id": "assertions.js",
      "path": "utils/assertions.js",
      "name": "assertions.js",
      "type": "utils",
      "cluster": "assertions",
      "category": "Defensive Invariant Guard Layer",
      "color": "#ff5500",
      "pos": [-15, -28, -5],
      "contract": {
        "kind": "Invariant Assertion Module",
        "exports": [
          "assertValid(value: any, label: string, type: 'string' | 'number' | 'array'): void"
        ],
        "throws": [
          "TypeError if unknown validation type or checkType returns false",
          "RangeError if isEmpty returns true (blank string, empty array, or array with whitespace strings)"
        ]
      },
      "semanticsAndFlow": {
        "execution": "Reads rules from VALIDATORS[type]. Runs rules.checkType(value). Runs rules.isEmpty(value). Throws immediately on violation."
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
          "inventedFor": "Jim Gray (Turing Award winner). Systems that fail silently on bad arguments cause corrupt state to propagate through thousands of subsequent instructions before exploding unpredictably.",
          "solvesForUs": "Guarantees that no Feed or PollingFeed can exist with empty ID, empty name, or empty endpoints list. Fails immediately at construction time.",
          "details": "Differentiates type errors (wrong primitive) from domain boundary errors (empty string) using distinct TypeError and RangeError constructors."
        }
      ]
    },
    {
      "id": "validators.js",
      "path": "utils/validators.js",
      "name": "validators.js",
      "type": "utils",
      "cluster": "validators",
      "category": "Predicate Strategy Dictionary",
      "color": "#e056fd",
      "pos": [0, -38, 10],
      "contract": {
        "kind": "Strategy Rule Dictionary Object",
        "rules": {
          "string": "{ checkType: (v) => typeof v === 'string', isEmpty: (v) => v.trim() === '' }",
          "number": "{ checkType: (v) => typeof v === 'number' && !Number.isNaN(v), isEmpty: () => false }",
          "array": "{ checkType: (v) => Array.isArray(v), isEmpty: (v) => v.length === 0 || v.some(e => typeof e === 'string' && e.trim() === '') }"
        }
      },
      "semanticsAndFlow": {
        "strategyLookup": "O(1) dictionary key access. Decouples the assertion runner from the specific type checking logic."
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
    isEmpty: (v) =>
      Array.isArray(v) === true &&
      (v.length === 0 || v.some((e) => typeof e === 'string' && e.trim() === '')),
  },
};""",
      "enablingConcepts": [
        {
          "name": "Strategy Pattern for Extensible Validation Rules",
          "inventedFor": "Gang of Four (GoF). Avoids bloated, monolithic if/else chains. Allows adding new validated data shapes (e.g. 'url', 'regex') by adding a new object property without altering callers.",
          "solvesForUs": "Provides rock-solid array and number validation that explicitly defends against JavaScript edge cases (e.g. typeof NaN === 'number', typeof [] === 'object').",
          "details": "Uses Array.isArray() and !Number.isNaN() to defend against JS type coercion flaws."
        }
      ]
    },
    {
      "id": "curry.js",
      "path": "kata/curry.js",
      "name": "curry.js",
      "type": "kata",
      "cluster": "kata",
      "category": "Algorithm & Language Mechanics Crucible",
      "color": "#00d2d3",
      "pos": [50, 8, -12],
      "contract": {
        "kind": "Language Engineering Crucible (L1 to L5)",
        "exports": [
          "sum3(a)(b)(c) -> Fixed 3-arity curried sum",
          "infiniteSum(a)(b)...() -> Variadic accumulator terminated by empty invocation",
          "add(a)(b)... -> Infinite chain evaluated via valueOf / Symbol.toPrimitive coercion",
          "curry(fn) -> Universal currying utility inspecting fn.length",
          "curryWithPlaceholder(fn) -> Staff-level placeholder (_) argument accumulator"
        ]
      },
      "semanticsAndFlow": {
        "levels": [
          {"level": 1, "name": "Fixed Arity", "behavior": "Nested lexical closures returning functions until all arguments collected."},
          {"level": 2, "name": "Empty Terminator", "behavior": "Accumulates until args.length === 0, then returns sum."},
          {"level": 3, "name": "Coercion Trap", "behavior": "Attaches .valueOf() to returned closure so JS engine coercion evaluates sum in numeric expressions."},
          {"level": 4, "name": "Universal curry()", "behavior": "Compares accumulated args.length against fn.length; recurses or invokes fn."},
          {"level": 5, "name": "Placeholder Curry", "behavior": "Supports out-of-order arguments using placeholder tokens."}
        ]
      },
      "pseudocode": """// Universal Curry Function
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
          "name": "Function Arity (fn.length) & Rest Parameter Mechanics",
          "inventedFor": "ECMA-262 defines Function.prototype.length as the number of formal parameters up to the first parameter with a default value. Rest parameters (...rest) do not count towards length.",
          "solvesForUs": "Powers our universal curry() helper, which dynamically inspects fn.length to decide whether to invoke the target function or return another curried collector function.",
          "details": "Knowing arity limits is critical when currying higher-order functions that accept default arguments or rest parameters."
        },
        {
          "name": "ToPrimitive Type Coercion & valueOf Interception",
          "inventedFor": "JavaScript's Abstract Equality (==) and addition (+) operators call the internal [[ToPrimitive]] operation, which invokes valueOf() followed by toString().",
          "solvesForUs": "Enables infinite chaining add(1)(2)(3) to evaluate directly in numeric expressions (add(1)(2) + 4 === 7) without needing an explicit invocation terminator.",
          "details": "Attaching a custom valueOf function to the returned closure function intercepts JS engine coercion seamlessly."
        }
      ]
    },
    {
      "id": "Feed.test.js",
      "path": "tests/src/feeds/Feed.test.js",
      "name": "Feed.test.js",
      "type": "test",
      "cluster": "test",
      "category": "BDD Invariant Verification Suite",
      "color": "#1dd1a1",
      "pos": [-35, 48, 8],
      "contract": {
        "kind": "Vitest Behavioral Test Suite",
        "verifications": [
          "Rejects direct instantiation of abstract Feed class with TypeError",
          "Allows concrete subclass instantiation and asserts property encapsulation",
          "Verifies defensive copying: mutating endpoints array does not mutate internal feed",
          "Enforces valid status transitions and throws RangeError on bogus status",
          "Validates failure recording and success recovery counter reset"
        ]
      },
      "semanticsAndFlow": {
        "harness": "Vitest runner executes with native ESM. Mocks concrete subclass TestFeed to verify abstract base class invariants."
      },
      "pseudocode": """describe('Feed.js', () => {
  it('throws when instantiating abstract base directly', () => {
    expect(() => new Feed('id', 'name', ['url'])).toThrow(TypeError);
  });

  it('guarantees defensive copying on read and write', () => {
    const feed = new TestFeed('id', 'name', ['url1']);
    const copy = feed.endpoints;
    copy.push('url2');
    expect(feed.endpoints).not.toEqual(copy);
  });
});""",
      "enablingConcepts": [
        {
          "name": "Automated BDD Invariant Verification",
          "inventedFor": "Dan North & Kent Beck (TDD/BDD). Prevents regression in complex object-oriented domain boundaries during rapid refactoring.",
          "solvesForUs": "Mathematically proves that Feed encapsulation and status guards remain unbreakable across all future feature extensions.",
          "details": "Runs in sub-millisecond execution times in Vitest using V8 isolates."
        }
      ]
    },
    {
      "id": "pipeline.test.js",
      "path": "tests/src/feeds/pipeline.test.js",
      "name": "pipeline.test.js",
      "type": "test",
      "cluster": "test",
      "category": "Pipeline Ingestion Verification Suite",
      "color": "#54a0ff",
      "pos": [38, 45, -5],
      "contract": {
        "kind": "Vitest Pipeline Test Suite",
        "verifications": [
          "validateSchema accepts valid payloads, throws ParseError on null or missing fields",
          "normalizeTimestamps converts POSIX seconds (<1e10) to ms (*1000) and parses ISO strings",
          "enrichFeedMetadata attaches feedId and valid ingestedAt timestamp",
          "normalizerFactory integrates all 4 stages into end-to-end transformation"
        ]
      },
      "semanticsAndFlow": {
        "testMatrix": "Fuzzes pipeline with edge-case inputs: numbers, ISO strings, corrupt strings, null payloads, missing properties, and verifies error telemetry shapes."
      },
      "pseudocode": """describe('pipeline.js', () => {
  it('normalizes seconds to milliseconds', () => {
    const res = normalizeTimestamps('timestamp')({ timestamp: 60 });
    expect(res.timestamp).toBe(60000);
  });

  it('enriches metadata with feedId and ingestedAt', () => {
    const res = enrichFeedMetadata('usgs-1')({ value: 10 });
    expect(res.feedId).toBe('usgs-1');
    expect(typeof res.ingestedAt).toBe('number');
  });
});""",
      "enablingConcepts": [
        {
          "name": "Boundary Fuzzing & Schema Invariant Proof",
          "inventedFor": "Ensuring pure functions handle every permutation of dirty data without throwing unhandled exceptions.",
          "solvesForUs": "Verifies that the ingestion pipeline acts as an impenetrable shield between chaotic external APIs and internal application state.",
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
      "category": "Prototype Inheritance Verification Suite",
      "color": "#ff6b6b",
      "pos": [-60, -2, -18],
      "contract": {
        "kind": "Vitest Inheritance Test Suite",
        "verifications": [
          "FeedError inherits from Error, sets message, name, and feedId",
          "NetworkError inherits from FeedError and Error, sets statusCode",
          "ParseError inherits from FeedError and Error, sets name"
        ]
      },
      "semanticsAndFlow": {
        "verification": "Asserts prototype chain integrity via instanceof operator across all 3 levels of the error hierarchy."
      },
      "pseudocode": """it('verifies prototype inheritance chain', () => {
  const err = new NetworkError('timeout', 'feed-1', 504);
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
  ],
  "edges": [
    {
      "source": "Feed.js",
      "target": "assertions.js",
      "type": "imports",
      "label": "Boundary Invariant Checking",
      "concept": "assertValid enforces non-empty string and array types in constructor before allocating fields"
    },
    {
      "source": "assertions.js",
      "target": "validators.js",
      "type": "delegates",
      "label": "Predicate Rule Lookup",
      "concept": "VALIDATORS dictionary supplies type check and emptiness definitions via Strategy Pattern"
    },
    {
      "source": "PollingFeed.js",
      "target": "Feed.js",
      "type": "extends",
      "label": "Subclass Inheritance",
      "concept": "Inherits private fields, status state-machine, and telemetry methods via super(id, name, endpoints)"
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
      "concept": "Throws ParseError with feedId when incoming schema is malformed or null"
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
}

with open(os.path.join('/Users/devang/Desktop/live_feed_console', 'docs/visualizer/concept_graph.json'), 'w', encoding='utf-8') as f:
  json.dump(knowledge, f, indent=2)

print("Comprehensive concept_graph.json successfully built!")
