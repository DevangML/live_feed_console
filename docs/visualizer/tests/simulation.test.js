import { describe, it, expect, vi, afterEach } from 'vitest';
import { Simulation, fixtures } from '../simulation-model.js';
afterEach(() => vi.useRealTimers());
describe('Source-backed system replay', () => {
  it('preserves text/object boundaries, timestamp conversion and reference behavior', () => {
    vi.useFakeTimers(); vi.setSystemTime(new Date('2026-09-10T12:00:00Z'));
    const run = new Simulation();
    while (run.next()) {}
    expect(run.history).toHaveLength(8);
    expect(typeof run.history[1].output).toBe('string');
    expect(run.history[2].output).toEqual({value:4.2,timestamp:1700000000});
    expect(run.history[3].sameReference).toBe(true);
    expect(run.history[4].sameReference).toBe(false);
    expect(run.history[4].output.timestamp).toBe(1700000000000);
    expect(run.history[5].output).toEqual({value:4.2,timestamp:1700000000000,feedId:'demo-feed',ingestedAt:Date.now()});
    expect(run.history[6].telemetry).toEqual({status:'CONNECTED',lastLatencyMs:120,consecutiveFailures:0});
    expect(run.history[7].output).toEqual(run.history[5].output);
    expect(run.next()).toBeNull();
  });
  it.each([['missing',3],['malformed',2]])('stops %s at the actual throwing stage', (fixture, index) => {
    const run = new Simulation(fixtures[fixture]);
    while(run.next()) {}
    expect(run.history.at(-1).index).toBe(index);
    expect(run.history.at(-1).error.name).toBe('ParseError');
    expect(run.feed.status).toBe('ERROR');
    expect(run.feed.consecutiveFailures).toBe(1);
    expect(run.history.some(record=>record.lane===4)).toBe(false);
    expect(run.next()).toBeNull();
  });
  it('does not attribute automatic status transitions to Feed', () => {
    const run = new Simulation();
    for(let i=0;i<6;i++)run.next();
    expect(run.feed.status).toBe('IDLE');
    run.next();
    expect(run.feed.status).toBe('CONNECTED');
  });
  it('retains independent before/after snapshots as later stages enrich data', () => {
    const run = new Simulation();
    while(run.next()) {}
    expect(run.history[4].input).toEqual({value:4.2,timestamp:1700000000});
    expect(run.history[4].output).not.toHaveProperty('feedId');
    const restarted = new Simulation(fixtures.malformed);
    expect(restarted.feed.status).toBe('IDLE');
    expect(restarted.history).toEqual([]);
  });
});
