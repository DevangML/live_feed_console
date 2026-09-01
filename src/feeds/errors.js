class FeedError extends Error {
  constructor(message, feedId) {
    super(message);
    this.feedId = feedId;
    this.name = "FeedError";
  }
}

class NetworkError extends FeedError {
  constructor(message, feedId, statusCode) {
    super(message, feedId);
    this.statusCode = statusCode;
    this.name = "NetworkError";
  }
}

class ParseError extends FeedError {
  constructor(message, feedId) {
    super(message, feedId);
    this.name = "ParseError";
  }
}

export {FeedError, NetworkError, ParseError}