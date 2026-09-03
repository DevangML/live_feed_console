import { describe, expect, it } from 'vitest';
import {
  FeedError,
  NetworkError,
  ParseError,
} from '../../../src/feeds/errors.js';

describe('src/feeds/errors.js', () => {
  it('FeedError', () => {
    const feedError = new FeedError('This is feed error', 'abcd');

    expect(feedError.message).toBe('This is feed error');
    expect(feedError.name).toBe('FeedError');
    expect(feedError.feedId).toBe('abcd');
    expect(feedError instanceof Error).toBe(true);
  });

  it('NetworkError', () => {
    const networkError = new NetworkError('This is network error', 'abcd');

    expect(networkError.message).toBe('This is network error');
    expect(networkError.name).toBe('NetworkError');
    expect(networkError.feedId).toBe('abcd');
    expect(networkError instanceof FeedError).toBe(true);
    expect(networkError instanceof Error).toBe(true);
  });

  it('ParseError', () => {
    const parseError = new ParseError('This is parse error', 'abcd');

    expect(parseError.message).toBe('This is parse error');
    expect(parseError.name).toBe('ParseError');
    expect(parseError.feedId).toBe('abcd');
    expect(parseError instanceof FeedError).toBe(true);
    expect(parseError instanceof Error).toBe(true);
  });
});
