import { VALIDATORS } from './validators.js';

export function assertValid(value, label, type) {
  const rules = VALIDATORS[type];

  if (!rules) {
    throw new TypeError(`Unknown validation type: ${type}`);
  }

  if (!rules.checkType(value)) throw new TypeError(`${label} has invalid type`);
  if (rules.isEmpty(value)) throw new RangeError(`${label} cannot be empty`);
}
