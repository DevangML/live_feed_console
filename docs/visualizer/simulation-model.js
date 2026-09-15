import Feed from '../../src/feeds/Feed.js';
import { parseJson } from '../../utils/helpers.js';
import { validateSchema, normalizeTimestamps, enrichFeedMetadata } from '../../src/feeds/pipeline.js';

// A replay harness, not a PollingFeed implementation. Real Feed methods are called
// explicitly; transport and UI boundaries below are explanatory fixtures.
class ReplayFeed extends Feed {}
const clone = value => value === undefined ? null : JSON.parse(JSON.stringify(value));
export const fixtures = {
  valid: '{"value":4.2,"timestamp":1700000000}',
  missing: '{"timestamp":1700000000}',
  malformed: '{"value":4.2,"timestamp":',
};
export const steps = [
  { title: 'A click requests fresh data', file: 'UI interaction', path: null, lane: 0, kind: 'Simulated boundary', operation: 'Refresh feed → request', why: 'The user asks for an update. This simulation creates a request command; a production UI is not connected yet.' },
  { title: 'The response arrives as text', file: 'PollingFeed.js', path: 'src/feeds/PollingFeed.js', lane: 0, kind: 'Simulated boundary', operation: 'Fixture → response text', why: 'The transport boundary supplies raw JSON text. PollingFeed is currently an empty subclass, so a local response fixture stands in for HTTP.' },
  { title: 'Text becomes a JavaScript value', file: 'helpers.js', path: 'utils/helpers.js', lane: 1, kind: 'Executed source', operation: 'parseJson(raw)', why: 'JSON text cannot be read as named fields. parseJson converts it into a value, or wraps a syntax failure in ParseError.' },
  { title: 'Required fields are checked', file: 'pipeline.js', path: 'src/feeds/pipeline.js', lane: 2, kind: 'Executed source', operation: "validateSchema(['value', 'timestamp'])(data)", why: 'Reject absent or null required fields before normalization. This checks presence, not field types; the same object is returned.' },
  { title: 'Seconds become milliseconds', file: 'pipeline.js', path: 'src/feeds/pipeline.js', lane: 2, kind: 'Executed source', operation: "normalizeTimestamps('timestamp')(data)", why: 'For this fixture, 1,700,000,000 is below the implementation’s 10-billion threshold, so it is multiplied by 1,000. This is a heuristic, not a universal unit detector.' },
  { title: 'The event gets its identity', file: 'pipeline.js', path: 'src/feeds/pipeline.js', lane: 2, kind: 'Executed source', operation: "enrichFeedMetadata('demo-feed')(data)", why: 'Attach the feed ID and current ingestion time so the consumer knows where the value came from. Reading Date.now() makes this step time-dependent.' },
  { title: 'The domain records success', file: 'Feed.js', path: 'src/feeds/Feed.js', lane: 3, kind: 'Source + replay harness', operation: "recordSuccess(120); setStatus('CONNECTED')", why: 'The harness explicitly calls the real Feed methods. recordSuccess resets failure telemetry; setStatus changes status separately. The 120 ms latency is illustrative, not measured network time.' },
  { title: 'A consumer can render the event', file: 'UI preview', path: null, lane: 4, kind: 'Simulated boundary', operation: 'event.value → visible readout', why: 'The completed event reaches this preview. This demonstrates a possible UI consumer; no application store or production UI subscription is implemented.' },
];

export class Simulation {
  constructor(raw = fixtures.valid) {
    this.raw = raw;
    this.feed = new ReplayFeed('demo-feed', 'Simulation feed', ['fixture://local']);
    this.value = null;
    this.index = -1;
    this.history = [];
    this.failed = false;
  }
  next() {
    if (this.failed || this.index >= steps.length - 1) return null;
    this.index += 1;
    const step = steps[this.index];
    const input = this.index === 0 ? { action: 'Refresh feed' } : clone(this.value);
    let reference = null;
    try {
      switch (this.index) {
        case 0: this.value = { command: 'request', feedId: 'demo-feed' }; break;
        case 1: this.value = this.raw; break;
        case 2: this.value = parseJson(this.value); break;
        case 3: { const old = this.value; this.value = validateSchema(['value', 'timestamp'])(old); reference = Object.is(old, this.value); break; }
        case 4: { const old = this.value; this.value = normalizeTimestamps('timestamp')(old); reference = Object.is(old, this.value); break; }
        case 5: { const old = this.value; this.value = enrichFeedMetadata('demo-feed')(old); reference = Object.is(old, this.value); break; }
        case 6: this.feed.recordSuccess(120); this.feed.setStatus('CONNECTED'); break;
        case 7: break;
      }
      const record = { ...step, index: this.index, input, output: clone(this.value), sameReference: reference, status: this.feed.status };
      if (this.index === 6) record.telemetry = { status: this.feed.status, lastLatencyMs: this.feed.lastLatencyMs, consecutiveFailures: this.feed.consecutiveFailures };
      this.history.push(record);
      return record;
    } catch (error) {
      this.failed = true;
      this.feed.recordFailure(error);
      this.feed.setStatus('ERROR');
      const record = { ...step, index: this.index, input, output: null, error: { name: error.name, message: error.message, feedId: error.feedId ?? null }, status: this.feed.status };
      this.history.push(record);
      return record;
    }
  }
}
