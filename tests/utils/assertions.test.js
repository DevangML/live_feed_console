import { describe, expect, it } from 'vitest';
import { assertValid } from '../../utils/assertions.js';

describe('utils/assertions', () => {
  describe('assertValid', () => {
    it('passes silently when value is valid and non-empty', () => {
      expect(() => assertValid('valid_id', 'Feed ID', 'string')).not.toThrow();
      expect(() =>
        assertValid(['https://www.google.com'], 'Endpoints', 'array')
      ).not.toThrow();
    });

    it('throws TypeError with invalid value passed to valid type but non-empty value', () => {
      expect(() => assertValid(123, 'Feed ID', 'string')).toThrow(TypeError);
      expect(() => assertValid('some_value', 'Endpoints', 'array')).toThrow(
        TypeError
      );
    });

    it('throws TypeError with valid value passed to invalid type but non-empty value', () => {
      expect(() => assertValid('some_id', 'Feed ID', 'array')).toThrow(
        TypeError
      );
      expect(() =>
        assertValid(['https://google.com'], 'Endpoints', 'string')
      ).toThrow(TypeError);
    });

    it('throws TypeError with empty value passed to valid type', () => {
      expect(() => assertValid('', 'Feed ID', 'string')).toThrow(RangeError);
      expect(() => assertValid([''], 'Endpoints', 'array')).toThrow(RangeError);
      expect(() => assertValid([], 'Endpoints', 'array')).toThrow(RangeError);
    });
  });
});
