import { assertValid } from '../../utils/assertions.js';

const VALID_STATUSES = new Set([
  'IDLE',
  'FETCHING',
  'CONNECTED',
  'DEGRADED',
  'ERROR',
]);

const Labels = {
  id: 'Id',
  name: 'Name',
  endpoints: 'Endpoints',
};

class Feed {
  #id;
  #name;
  #endpoints = [];
  #status = 'IDLE';
  #lastFetchedAt = null;
  #lastLatencyMs = 0;
  #consecutiveFailures = 0;
  #lastError = null;

  constructor(id, name, endpoints) {
    if (new.target === Feed) {
      throw new TypeError('Cannot constuct Feed instances directly');
    }

    assertValid(id, Labels.id, 'string');
    assertValid(name, Labels.name, 'string');
    assertValid(endpoints, Labels.endpoints, 'array');

    this.#id = id;
    this.#name = name;
    this.#endpoints = [...endpoints];
  }

  get id() {
    return this.#id;
  }

  get status() {
    return this.#status;
  }

  get endpoints() {
    return [...this.#endpoints];
  }

  get lastFetchedAt() {
    return this.#lastFetchedAt;
  }

  get lastLatencyMs() {
    return this.#lastLatencyMs;
  }

  get consecutiveFailures() {
    return this.#consecutiveFailures;
  }

  get lastError() {
    return this.#lastError;
  }

  get name() {
    return this.#name;
  }

  // Not a property setter but setter method
  setStatus(newStatus) {
    if (!VALID_STATUSES.has(newStatus)) {
      throw new RangeError(
        'The status is not within the valid range of values'
      );
    }

    this.#status = newStatus;
  }

  // Domain Methods

  recordSuccess(latencyMs) {
    this.#lastFetchedAt = Date.now();
    this.#lastLatencyMs = latencyMs;

    // As winning streak has started
    this.#consecutiveFailures = 0;
    this.#lastError = null;
  }

  recordFailure(error) {
    this.#consecutiveFailures += 1;
    this.#lastError = error;
  }

  // Abstract Methods

  start() {
    throw new Error('Method start() must be implemented by derived subclass');
  }

  stop() {
    throw new Error(
      'Method stop() must be implemented by the derived subclass'
    );
  }

  fetch() {
    throw new Error(
      'Method fetch() must be implemented by the derived subclass'
    );
  }
}

export default Feed;
