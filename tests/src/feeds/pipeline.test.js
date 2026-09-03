import { describe, expect, it } from 'vitest';
import { ParseError } from '../../../src/feeds/errors.js';
import {
  enrichFeedMetadata,
  normalizerFactory,
  normalizeTimestamps,
  validateSchema,
} from '../../../src/feeds/pipeline.js';

describe('src/feeds/pipeline.js', () => {
  const mockRequiredFields = ['id', 'value', 'status', 'timestamp'];
  const undefinedRequiredFields = ['id', undefined, 'status', 'timestamp'];
  const nullRequiredFields = ['id', null, 'status', 'timestamp'];

  const validPayload = {
    id: 'event-101',
    value: 42.5,
    status: 'ACTIVE',
    timestamp: '2026-09-03T10:10:31.347Z',
  };

  const invalidPayload = {
    id: 'event-102',
    value: 99.9,
    timestamp: 1693656000000,
  };

  const secondsPayload = {
    id: 'event-102',
    value: 99.9,
    timestamp: 60,
  };

  const validJsonString = JSON.stringify(validPayload);

  describe('validateSchema', () => {
    it('passes silently if data is right and required fields are present', () => {
      const data = validateSchema(mockRequiredFields)(validPayload);

      expect(data).toEqual(validPayload);
    });

    it('passes silently if data is right and required fields is empty (no validation required)', () => {
      const data = validateSchema([])(validPayload);

      expect(data).toEqual(validPayload);
    });

    it('throws ParseError if data is not an object', () => {
      expect(() => validateSchema([])('Some data')).toThrow(ParseError);
    });

    it('throws ParseError if data is null', () => {
      expect(() => validateSchema([])(null)).toThrow(ParseError);
    });

    it('throws ParseError if data is valid but one of the required fields is undefined', () => {
      expect(() =>
        validateSchema(undefinedRequiredFields)(validPayload)
      ).toThrow(ParseError);
    });

    it('throws ParseError if data is valid but one of the required fields is null', () => {
      expect(() => validateSchema(nullRequiredFields)(validPayload)).toThrow(
        ParseError
      );
    });

    it('throws ParseError if data invalid', () => {
      expect(() => validateSchema(mockRequiredFields)(invalidPayload)).toThrow(
        ParseError
      );
    });
  });

  describe('normalizeTimestamps', () => {
    it('parses ISO strings into milliseconds', () => {
      const timestamp = normalizeTimestamps('timestamp')(validPayload);

      expect(timestamp['timestamp']).toBe(1788430231347);
    });

    it('parses timestamp which is in milliseconds as is', () => {
      const timestamp = normalizeTimestamps('timestamp')(invalidPayload);

      expect(timestamp['timestamp']).toBe(1693656000000);
    });

    it('parses timestamp which is in seconds into milliseconds', () => {
      const timestamp = normalizeTimestamps('timestamp')(secondsPayload);

      expect(timestamp['timestamp']).toBe(60000);
    });

    // This is an isolated testcase, it won't be generally hit in the pipe as previous step makes sure if field is missing the whole workflow throws
    it('parses invalid timestamp field with field with Date.now()', () => {
      const timestamp = normalizeTimestamps('timestampField')(secondsPayload);

      expect(timestamp['timestampField']).toBeGreaterThan(1000000000000);
      expect(typeof timestamp['timestampField']).toBe('number');
    });

    it('parses valid timestamp field with undefined as Date.now()', () => {
      const undefinedPayload = { ...secondsPayload, timestamp: undefined };

      const timestamp = normalizeTimestamps('timestamp')(undefinedPayload);

      expect(timestamp['timestamp']).not.toBe(60000);
      expect(typeof timestamp['timestamp']).toBe('number');
    });

    it('parses valid timestamp field with null as Date.now()', () => {
      const nullPayload = { ...secondsPayload, timestamp: null };

      const timestamp = normalizeTimestamps('timestamp')(nullPayload);

      expect(timestamp['timestamp']).not.toBe(60000);
      expect(typeof timestamp['timestamp']).toBe('number');
    });

    it('parses valid timestamp field with NaN as Date.now()', () => {
      const nanPayload = { ...secondsPayload, timestamp: NaN };

      const timestamp = normalizeTimestamps('timestamp')(nanPayload);

      expect(timestamp['timestamp']).not.toBe(60000);
      expect(typeof timestamp['timestamp']).toBe('number');
    });
  });

  describe('enrichFeedMetadata', () => {
    it('adds feedId properly', () => {
      const feedId = 'Feed ID';

      const enrichedData = enrichFeedMetadata(feedId)(validPayload);

      expect(enrichedData['feedId']).toBe('Feed ID');
    });

    it('attaches valid igestedAt', () => {
      const feedId = 'Feed ID';

      const enrichedData = enrichFeedMetadata(feedId)(validPayload);

      expect(typeof enrichedData['ingestedAt']).toBe('number');
    });
  });

  describe('normalizerFactory', () => {
    it('happy flow works properly', () => {
      const feedId = 'Feed 2';
      const normalizedData = normalizerFactory({
        feedId: feedId,
        requiredFields: mockRequiredFields,
        timestampField: 'timestamp',
      })(validJsonString);

      expect(normalizedData['feedId']).toBe(feedId);
      expect(normalizedData['timestamp']).toBeGreaterThan(10000000000);
      expect(typeof normalizedData['timestamp']).toBe('number');
      expect(typeof normalizedData['ingestedAt']).toBe('number');
    });
  });
});
