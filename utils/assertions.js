import { capitalize } from './helpers';
import { VALIDATORS } from './validators';

function assertValid(value, type) {
  const rules = VALIDATORS[type];

  if (!rules) {
    throw new TypeError(`Unknown validation type: ${type}`);
  }

  const label = capitalize(value);

  if (!rules.checktype(value)) throw new TypeError(`${label} has invalid type`);
  if (rules.isEmpty(value)) throw new RangeError(`${label} cannot be empty`);
}
