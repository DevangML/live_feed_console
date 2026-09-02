import { describe, expect, it } from 'vitest';
import { VALIDATORS } from '../../utils/validators.js';

describe('utils/validators', () => {
  describe('string validator', () => {
    it('correctly validates string types', () => {
      expect(VALIDATORS.string.checkType('hello')).toBe(true);
      expect(VALIDATORS.string.checkType(123)).toBe(false);
      expect(VALIDATORS.string.checkType(null)).toBe(false);
      expect(VALIDATORS.string.checkType(undefined)).toBe(false);
    });

    it('identifies empty and whitespace-only strings', () => {
      expect(VALIDATORS.string.isEmpty('')).toBe(true);
      expect(VALIDATORS.string.isEmpty(' ')).toBe(true);
      expect(VALIDATORS.string.isEmpty('valid_id')).toBe(false);
    });
  });

  describe('Array Validator', () => {
    it('correctly validates array types', () => {
      expect(VALIDATORS.array.checkType(['first', 'second', 'third'])).toBe(
        true
      );
      expect(VALIDATORS.array.checkType(`['first', 'second', 'third']`)).toBe(
        false
      );
      expect(VALIDATORS.array.checkType('string')).toBe(false);
      expect(VALIDATORS.array.checkType({})).toBe(false);
    });

    it('identifies empty arrays and arrays with blank items', () => {
      expect(VALIDATORS.array.isEmpty([])).toBe(true);
      expect(VALIDATORS.array.isEmpty([''])).toBe(true);
      expect(VALIDATORS.array.isEmpty(['https://api.com'])).toBe(false);
    });
  });
});
