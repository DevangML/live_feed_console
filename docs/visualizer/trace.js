import { parseJson } from '/utils/helpers.js';
import { validateSchema, normalizeTimestamps, enrichFeedMetadata } from '/src/feeds/pipeline.js';

let initialized = false;
export function initializeTrace() {
  if (initialized) return;
  initialized = true;
  const input = document.getElementById('trace-input');
  const output = document.getElementById('trace-output');
  const fixtures = {
    valid: '{"value":4.2,"timestamp":1700000000}',
    missing: '{"timestamp":1700000000}',
    malformed: '{"value":4.2,"timestamp":',
  };
  document.getElementById('trace-fixture').addEventListener('change', event => {
    input.value = fixtures[event.target.value];
    output.replaceChildren();
  });
  document.getElementById('run-trace').addEventListener('click', () => {
    output.replaceChildren();
    let value = input.value;
    const stages = [
      ['parseJson', parseJson, 'Parses JSON text. A syntax error becomes ParseError.'],
      ['validateSchema', validateSchema(['value', 'timestamp']), 'Checks presence of required fields; it does not validate their types. Returns the same object.'],
      ['normalizeTimestamps', normalizeTimestamps('timestamp'), 'Uses the existing magnitude heuristic for seconds versus milliseconds. Invalid values may fall back to the current clock.'],
      ['enrichFeedMetadata', enrichFeedMetadata('visualizer-demo'), 'Adds feedId and ingestedAt using the current clock. This stage is time-dependent.'],
    ];
    for (const [name, transform, explanation] of stages) {
      const card = document.createElement('section'); card.className = 'trace-step';
      const title = document.createElement('h3'); title.textContent = name;
      const detail = document.createElement('p'); detail.textContent = explanation;
      const before = document.createElement('pre'); before.textContent = `BEFORE\n${JSON.stringify(value, null, 2)}`;
      card.append(title, detail, before);
      try {
        const next = transform(value);
        const after = document.createElement('pre'); after.textContent = `AFTER\n${JSON.stringify(next, null, 2)}`;
        const identity = document.createElement('p'); identity.textContent = `Same reference/value: ${Object.is(value, next)}`;
        card.append(after, identity); value = next;
      } catch (error) {
        card.classList.add('failed');
        const failure = document.createElement('p'); failure.textContent = `${error.name}: ${error.message} · Execution stopped here; later stages did not run.`;
        card.append(failure); output.append(card); return;
      }
      output.append(card);
    }
  });
  document.getElementById('run-trace').click();
}
