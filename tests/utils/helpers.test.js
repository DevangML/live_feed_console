import { describe, expect, it } from 'vitest';
import { ParseError } from '../../src/feeds/errors.js';
import { capitalize, compose, parseJson, pipe } from '../../utils/helpers.js';

describe('utils/helpers', () => {
  describe('capitalize', () => {
    it('capitalizes the first letter of a lowercase string', () => {
      expect(capitalize('devang')).toBe('Devang');
    });

    it('keeps already capitalized strings intact', () => {
      expect(capitalize('Tokyo')).toBe('Tokyo');
    });

    it('handles single characters and empty strings cleanly', () => {
      expect(capitalize('a')).toBe('A');
      expect(capitalize('')).toBe('');
    });

    it('throws TypeError when passed non-string arguments', () => {
      // Note: Always wrap function in () => ... when asserting exceptions!
      expect(() => capitalize(123)).toThrow(TypeError);
      expect(() => capitalize(null)).toThrow(TypeError);
      expect(() => capitalize(undefined)).toThrow(TypeError);
      expect(() => capitalize({})).toThrow(TypeError);
    });
  });

  describe('pipe and compose', () => {
    const add2 = (x) => x + 2;
    const square = (x) => x * x;

    it('pipe executes left-to-right: (3+2)^2 = 25', () => {
      const pipeline = pipe(add2, square);
      expect(pipeline(3)).toBe(25);
    });

    it('pipe and compose both return input untouched when no function is given', () => {
      const emptyPipe = pipe();
      const emptyCompose = compose();

      expect(emptyCompose('name')).toBe('name');
      expect(emptyPipe(98)).toBe(98);
    });

    it('compose executes right-to-left: (3)^2 + 2 = 11', () => {
      const composition = compose(add2, square);
      expect(composition(3)).toBe(11);
    });

    it('handles multi-step type-transforming pipelines', () => {
      const double = (n) => n * 2;
      const formatCurrency = (n) => `$${n}`;
      const wrapInObject = (str) => ({ price: str });
      const createPriceTag = pipe(double, formatCurrency, wrapInObject);
      // 50 -> 100 -> "$100" -> { price: "$100" }
      expect(createPriceTag(50)).toEqual({ price: '$100' });
    });
  });

  describe('parseJson', () => {
    it('parses valid JSON strings into JavaScript objects', () => {
      const rawJson = '{"feedId": "usgs", "value": 4.5}';
      expect(parseJson(rawJson)).toEqual({
        feedId: 'usgs',
        value: 4.5,
      });
    });

    it('returns the input untouched if it is already an object', () => {
      const alreadyAnObject = { title: 'Earthquake' };
      expect(parseJson(alreadyAnObject)).toBe(alreadyAnObject);
    });

    it('throws a ParseError when JSON is invalid or malformed', () => {
      // Tests that malformed JSON is caught and converted to our custom ParseError
      expect(() => parseJson('{ invalid json, missing quotes }')).toThrow(
        ParseError
      );
      expect(() => parseJson('<html>502 Bad Gateway</html>')).toThrow(
        ParseError
      );
    });
  });
});
