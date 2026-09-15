import { Simulation, fixtures, steps } from './simulation-model.js';
import { createLightRenderer } from './hdr-renderer.js';
const $ = id => document.getElementById(id);
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
let model = new Simulation(), selected = -1, playing = false, elapsed = 0, lastTime = 0, raf = 0;
let sourceRequest = 0, sourceRevision = null, previousLane = 0, currentLane = 0;
let lights = { update() {}, destroy() {} };
const dwell = 5000;
const pretty = value => typeof value === 'string' ? value : JSON.stringify(value, null, 2);
const laneNames = ['request','object','clean event','recorded','rendered'];

function buttons() {
  const complete = model.failed || selected === steps.length - 1;
  $('play').textContent = playing ? 'Ⅱ Pause journey' : complete ? '↺ Replay system' : selected < 0 ? '▶ Play system' : '▶ Continue journey';
  $('next').disabled = complete;
}
function drawOutput(record) {
  const area = $('output'); area.replaceChildren();
  if (record.error) { area.textContent = `${record.error.name}\n${record.error.message}`; return; }
  const before = record.input;
  const after = record.telemetry || record.output;
  if (after && typeof after === 'object' && !Array.isArray(after)) {
    area.append('{\n');
    const entries = Object.entries(after);
    entries.forEach(([key,value],i) => {
      const line = document.createElement('span');
      line.textContent = `  ${JSON.stringify(key)}: ${JSON.stringify(value)}${i < entries.length-1 ? ',' : ''}\n`;
      if (!before || typeof before !== 'object' || JSON.stringify(before[key]) !== JSON.stringify(value)) line.className='changed';
      area.append(line);
    });
    area.append('}');
  } else area.textContent = pretty(after);
}
function show(record) {
  selected = record.index;
  previousLane = currentLane; currentLane = record.lane;
  $('step-file').textContent = `${record.file} / STEP ${record.index + 1}`;
  $('step-title').textContent = record.title;
  $('step-kind').textContent = record.kind;
  $('input').textContent = pretty(record.input);
  $('input-type').textContent=typeof record.input;
  $('output-type').textContent=record.error ? 'error' : typeof (record.telemetry || record.output);
  document.body.classList.toggle('ui-complete', record.index===7);
  $('operation').textContent = record.operation;
  $('reason').textContent = record.why;
  drawOutput(record);
  $('change-note').textContent = record.error ? 'Rejected here. Nothing reaches the UI.' : record.sameReference === true ? 'Same object returned · no fields changed.' : record.sameReference === false ? 'New shallow object · changed fields highlighted.' : record.telemetry ? 'Telemetry shown above; the event continues unchanged.' : '';
  $('error-note').hidden = !record.error;
  $('error-note').textContent = record.error ? `${record.error.name} is created by the source. The replay harness records the failure and explicitly sets Feed status to ERROR. Later transforms and the UI update do not run.` : '';
  document.body.classList.toggle('failed',!!record.error);
  $('progress-label').textContent = `${record.index + 1} / ${steps.length} steps${record.error ? ' · stopped' : ''}`;
  $('journey-label').textContent = record.error ? 'THE JOURNEY / rejected at the boundary' : `THE JOURNEY / ${record.file}`;
  document.querySelectorAll('.file-stage').forEach(button => { const lane=Number(button.dataset.lane);button.classList.toggle('active',lane===record.lane);button.classList.toggle('done',lane<record.lane);button.setAttribute('aria-pressed',String(lane===record.lane)); });
  document.querySelectorAll('#timeline button').forEach((button,i) => { button.classList.toggle('active',i===selected);button.classList.toggle('done',i<selected);button.setAttribute('aria-current',i===selected ? 'step' : 'false'); });
  $('ui-value').textContent = record.index === 7 ? `${record.output.value} · event received` : 'Waiting for an event';
  $('packet').classList.remove('idle');
  $('packet').style.left = `${((playing ? previousLane : record.lane) + .5) * 20}%`;
  $('packet').querySelector('span').textContent = record.error ? 'rejected' : record.index===1 ? 'JSON text' : record.index===4 ? 'ms timestamp' : laneNames[record.lane];
  lights.update({ active: currentLane, packet: (currentLane + .5)/5, visible: true });
  $('source-details').hidden = !record.path;
  $('source-details').open = false;
  $('source-code').textContent = 'Open to load the current file from disk.';
  sourceRequest++;
  buttons();
}
function advance() {
  if (selected < model.history.length-1) show(model.history[selected+1]);
  else { const record = model.next(); if (!record) return false; show(record); }
  elapsed = 0;
  return !model.history[selected].error && selected < steps.length-1;
}
function stop() { playing=false; cancelAnimationFrame(raf); lastTime=0; buttons(); }
function tick(now) {
  if (!playing) return;
  if (lastTime) elapsed += Math.min(now-lastTime,100);
  lastTime=now;
  const t = reducedMotion ? 1 : Math.min(elapsed/1800,1);
  const eased = t*t*(3-2*t);
  const packetPosition=(previousLane+.5+(currentLane-previousLane)*eased)/5;
  $('packet').style.left=`${packetPosition*100}%`;
  lights.update({ active:currentLane, packet:packetPosition, visible:true });
  if (elapsed >= dwell && !advance()) { stop(); return; }
  raf=requestAnimationFrame(tick);
}
function reset() {
  stop();model=new Simulation(fixtures[$('scenario').value]);selected=-1;elapsed=0;previousLane=0;currentLane=0;
  $('step-file').textContent='START HERE';$('step-title').textContent='One click. One traceable journey.';$('step-kind').textContent='Interactive simulation';
  $('input').textContent='{ "action": "Refresh feed" }';$('operation').textContent='Press Play system';$('reason').textContent='Each stop reveals the input, the operation that changes it, and the output passed onward. Select a file to study its steps.';$('output').textContent='Waiting for your click…';$('change-note').textContent='';$('error-note').hidden=true;
  $('progress-label').textContent='0 / 8 steps';$('journey-label').textContent='THE JOURNEY / ready to begin';$('ui-value').textContent='Waiting for an event';$('source-details').hidden=true;sourceRequest++;
  $('input-type').textContent='object';$('output-type').textContent='pending';
  document.body.classList.remove('ui-complete');
  document.body.classList.remove('failed');document.querySelectorAll('.active,.done').forEach(element=>element.classList.remove('active','done'));
  document.querySelectorAll('.file-stage').forEach(button=>button.setAttribute('aria-pressed','false'));
  document.querySelectorAll('#timeline button').forEach(button=>button.setAttribute('aria-current','false'));
  $('packet').classList.add('idle');lights.update({active:-1,visible:false});buttons();
}
function jump(index) {
  stop();
  // Do not silently re-run past steps. Stored snapshots keep clock values stable.
  while(model.history.length <= index && !model.failed) model.next();
  const record=model.history[Math.min(index,model.history.length-1)];
  if(record) { show(record);elapsed=0; }
}
steps.forEach((step,index) => {
  const button=document.createElement('button');button.title=`${index+1}. ${step.title}`;button.setAttribute('aria-label',button.title);button.addEventListener('click',()=>jump(index));$('timeline').append(button);
});
document.querySelectorAll('.file-stage').forEach(button=>button.addEventListener('click',()=>jump(steps.findIndex(step=>step.lane===Number(button.dataset.lane)))));
$('play').addEventListener('click',()=>{
  if(playing){stop();return;}
  if(model.failed || selected===steps.length-1) reset();
  if(selected<0) advance();
  playing=true;lastTime=0;buttons();raf=requestAnimationFrame(tick);
});
$('next').addEventListener('click',()=>{stop();advance();});
$('restart').addEventListener('click',reset);
$('scenario').addEventListener('change',reset);
document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
$('source-details').addEventListener('toggle',async()=>{
  if(!$('source-details').open)return;
  const record=model.history[selected];if(!record?.path)return;
  const request=++sourceRequest;$('source-code').textContent='Loading source…';
  try{const response=await fetch(`/api/file-content?path=${encodeURIComponent(record.path)}`);if(!response.ok)throw new Error(`HTTP ${response.status}`);const source=await response.text();if(request===sourceRequest)$('source-code').textContent=source;}
  catch(error){if(request===sourceRequest)$('source-code').textContent=error.message;}
});
async function sync() {
  try{const response=await fetch('/api/graph');if(!response.ok)throw new Error('Source inventory unavailable');const graph=await response.json();
    $('disk-status').textContent=sourceRevision && sourceRevision!==graph.revision ? 'Source changed on disk. Reload to run the new code; this session keeps its imported modules.' : `${graph.nodes.length} source files indexed · checked every 5 seconds. Transport and production UI remain simulated.`;
    if(!sourceRevision)sourceRevision=graph.revision;
  }catch(error){$('disk-status').textContent=error.message;}
}
reset();$('play').disabled=false;$('next').disabled=false;
createLightRenderer($('light-canvas'), info=>{$('display-status').textContent=info.mode;$('display-explanation').textContent=info.detail;}).then(renderer=>{lights=renderer;lights.update({active:currentLane,visible:selected>=0,packet:(currentLane+.5)/5});});
sync();const syncTimer=setInterval(()=>{if(!document.hidden)sync();},5000);
window.addEventListener('pagehide',()=>{stop();clearInterval(syncTimer);lights.destroy();});
