import { describe, expect, it } from 'vitest';
import Feed from '../../../src/feeds/Feed.js';

describe('src/feeds/Feed.js', () => {
  describe('contructor', () => {
    it('throws when instatiating with new keyword', () => {
      expect(
        () => new Feed('valid_id', 'valid_name', ['https://www.google.com'])
      ).toThrow(TypeError);
      expect(
        () => new Feed('valid_id', 'valid_name', ['https://www.google.com'])
      ).toThrow('Cannot construct Feed instances directly');
    });

    it('allows concrete subclass instantiation', () => {
      class TestFeed extends Feed {
        fetch() {
          return Promise.resolve([]);
        }
        start() {}
        stop() {}
      }

      const feed = new TestFeed('valid_id', 'valid_name', [
        'https://www.google.com',
      ]);

      expect(feed.id === 'valid_id').toBe(true);
    });
  });
});
