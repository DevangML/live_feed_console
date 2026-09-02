import { ParseError } from '../src/feeds/errors.js';

function capitalize(s) {
  if (!(typeof s === 'string')) {
    throw new TypeError(`${s} is of invalid type`);
  }

  return s.charAt(0).toUpperCase() + s.slice(1);
}

// Combinators

// Pipe

const pipe = function (...funcs) {
  return function (val) {
    return funcs.reduce((prev, fn) => fn(prev), val);
  };
};

// Compose

const compose = function (...funcs) {
  return function (val) {
    return funcs.reduceRight((prev, fn) => fn(prev), val);
  };
};

// parseJson
// Input: Raw String input or already parsed object
// Output: Return clean JS Object
// Corner Case: If invalid JSON, throw a ParseError

export const parseJson = function (raw) {
  if (typeof raw !== 'string') return raw;

  try {
    return JSON.parse(raw);
  } catch (err) {
    throw new ParseError(err.message, 'unknown');
  }
};

export { capitalize, compose, pipe };
