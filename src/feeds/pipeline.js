// Data cleansing engine for various data sources we use like USGS Earthquake Feed, the Open-Meteo Weather Feed, CoinGecko Crypto Feed

import { parseJson, pipe } from '../../utils/helpers.js';
import { ParseError } from './errors.js';

// Intercepts the raw external responses at the boundary, transforms them into a single unified internal event shape, and ensures the data is rejected before ever touching our redux store or react state

// rawData (json) --parseJson-> JS Object -validateSchema-> Validated JS Object (or throws ParseError) --normalizeTimestamps--> Object with timestamp as a clean 'ms' number ---enrichFeedMetadata---> Clean NormalizedMetricEvent ready for Redux

// Purity is required to make sure sideeffects, shared reference mutation nightmare is avoided, because react has a shallow referrential equality because of immutable referrential comparisons to achieve 60 fps O(1) comparisons

// All these methods must be curried HOC functions as pipe/compose require unary pure functions only

export const validateSchema = (requiredFields) => (data) => {
  if (typeof data !== 'object' || data === null) {
    throw new ParseError('Payload must be a valid non-null object');
  }

  requiredFields.forEach((field) => {
    if (data[field] === undefined || data[field] === null) {
      throw new ParseError(`Missing required field: ${field}`);
    }
  });

  return data;
};

export const normalizeTimestamps =
  (timestampField = 'timestamp') =>
  (data) => {
    const rawTimestamp = data[timestampField];
    let timestamp;

    if (
      rawTimestamp === null ||
      rawTimestamp === undefined ||
      Number.isNaN(rawTimestamp)
    ) {
      timestamp = Date.now();
    }

    if (typeof rawTimestamp === 'string') {
      let ts = Date.parse(rawTimestamp);
      !Number.isNaN(ts) ? (timestamp = ts) : null;
    }

    if (typeof rawTimestamp === 'number') {
      const tenBillion = 10000000000;

      if (rawTimestamp < tenBillion) {
        timestamp = rawTimestamp * 1000;
      } else {
        timestamp = rawTimestamp;
      }
    }

    // Just in case nothing works, and timestamp is of wrong format
    if (!timestamp) {
      timestamp = Date.now();
    }

    const finalData = { ...data, [timestampField]: timestamp };

    return finalData;
  };

// Enrich Feed Metadata
// It attaches our client-side telemetry metadata to the normalized event before it enters the redux store
// Metadata: feedId (passed), ingestedAt (Date.now())

export const enrichFeedMetadata = (feedId) => (data) => {
  if (typeof data !== 'object' || data === null) {
    throw new ParseError('Payload must be a non-null object');
  }

  if (typeof feedId !== 'string') {
    throw new TypeError('Feed Id must be a valid string');
  }

  const ingestedAt = Date.now();

  const finalData = { ...data, feedId: feedId, ingestedAt: ingestedAt };

  return finalData;
};

/// normalizer factory method using pipe (which returns an inner function expecting data as the initial value for the first step that goes to parseJson)

export const normalizerFactory = ({
  feedId,
  requiredFields = [],
  timestampField,
}) => {
  return pipe(
    parseJson,
    validateSchema(requiredFields),
    normalizeTimestamps(timestampField),
    enrichFeedMetadata(feedId)
  );
};
