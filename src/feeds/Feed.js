const VALID_STATUSES = new Set([
  'IDLE',
  'FETCHING',
  'CONNECTED',
  'DEGRADED',
  'ERROR',
]);

class Feed {
  #id;
  #name;
  #endpoints = [];
  #status = 'IDLE';

  constructor(id, name, endpoints) {
    if (new.target === Feed) {
      throw TypeError('Cannot constuct Feed instances directly');
    }

    if (typeof id !== 'string') {
      throw TypeError('Id must be string');
    }
    if (id === '') {
      throw RangeError('Id cannot be empty');
    }

    if (typeof name !== 'string') {
      throw TypeError('Name must be string');
    }

    if (name === '') {
      throw RangeError('Name cannot be empty');
    }

    if (Array.isArray(endpoints) !== true) {
      throw TypeError('Endpoints must be an array');
    }

    if (Array.isArray(endpoints) && endpoints.length < 1) {
      throw RangeError('Endpoints cannot be empty');
    }

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
}
