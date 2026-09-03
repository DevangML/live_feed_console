import { beforeEach, describe, expect, it } from 'vitest';
import Feed from '../../../src/feeds/Feed.js';

describe('src/feeds/Feed.js', () => {
  describe('contructor', () => {
    class TestFeed extends Feed {
      fetch() {
        return Promise.resolve([]);
      }
      start() {}
      stop() {}
    }

    class IncompleteFeed extends Feed {}

    let feed;

    beforeEach(() => {
      feed = new TestFeed('valid_id', 'valid_name', ['https://www.google.com']);
    });

    it('throws when instatiating with new keyword', () => {
      expect(
        () => new Feed('valid_id', 'valid_name', ['https://www.google.com'])
      ).toThrow(TypeError);
      expect(
        () => new Feed('valid_id', 'valid_name', ['https://www.google.com'])
      ).toThrow('Cannot construct Feed instances directly');
    });

    it('allows concrete subclass instantiation', () => {
      expect(feed.id === 'valid_id').toBe(true);
    });

    it('defensive copying', () => {
      const endpoints = feed.endpoints;

      endpoints.push('https://youtube.com');

      expect(feed.endpoints).not.toEqual(endpoints);
    });

    it('allows valid setState', () => {
      feed.setStatus('FETCHING');

      expect(feed.status).toBe('FETCHING');
    });

    it('throws RangeError on invalid setState', () => {
      expect(() => feed.setStatus('Fake_Status')).toThrow(RangeError);
    });

    it('failure and success are properly recorded', () => {
      const timeoutError = new Error('Connection Timeout');

      const lastLatencyMs = feed.lastLatencyMs;

      feed.recordFailure(timeoutError);
      feed.recordFailure(timeoutError);

      expect(feed.consecutiveFailures).toBe(2);
      expect(feed.lastError).toBe(timeoutError);

      feed.recordSuccess();

      expect(feed.consecutiveFailures).toBe(0);
      expect(feed.lastLatencyMs).not.toBe(lastLatencyMs);
    });

    it('incomplete instantiation throws', () => {
      const incompleteFeed = new IncompleteFeed('valid_id', 'valid_name', [
        'https://www.google.com',
      ]);

      expect(() => incompleteFeed.start()).toThrow(Error);
      expect(() => incompleteFeed.stop()).toThrow(Error);
      expect(() => incompleteFeed.fetch()).toThrow(Error);
    });
  });
});
