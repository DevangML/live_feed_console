// Real extended-range presentation; no SDR tone mapper masquerading as HDR.
// https://developer.chrome.com/blog/new-in-webgpu-129#hdr_support_with_canvas_tone_mapping_mode
export async function createLightRenderer(canvas, report) {
  const p3 = matchMedia('(color-gamut: p3)');
  const high = matchMedia('(dynamic-range: high)');
  let device, context, frame = 0, dead = false;
  const describeFallback = reason => report({ mode: p3.matches ? 'Display P3 CSS · SDR graphics' : 'sRGB · SDR graphics', detail: `${reason} The file diagram and simulation still work. HDR luminance is not measured by this page.` });
  if (!navigator.gpu) { describeFallback('WebGPU is unavailable in this browser.'); return { update() {}, destroy() {} }; }
  try {
    const adapter = await navigator.gpu.requestAdapter();
    if (!adapter) throw new Error('No WebGPU adapter was provided.');
    device = await adapter.requestDevice();
    context = canvas.getContext('webgpu');
    if (!context) throw new Error('A WebGPU canvas could not be created.');
    let hdr = false, profile = null, sampled = false;
    function configure() {
      const config = { device, format: 'rgba16float', colorSpace: p3.matches ? 'display-p3' : 'srgb', alphaMode: 'premultiplied', usage: GPUTextureUsage.RENDER_ATTACHMENT | GPUTextureUsage.COPY_SRC, toneMapping: { mode: high.matches ? 'extended' : 'standard' } };
      context.configure(config);
      const accepted = context.getConfiguration?.();
      hdr = high.matches && accepted?.format === 'rgba16float' && accepted?.toneMapping?.mode === 'extended';
      const gamut = accepted?.colorSpace === 'display-p3' ? 'Display P3' : accepted?.colorSpace === 'srgb' ? 'sRGB' : 'Color space unconfirmed';
      profile = { mode: `${hdr ? 'HDR output enabled' : 'SDR output'} · ${gamut}`, detail: `${accepted?.format || 'Requested rgba16float'} canvas; ${accepted?.toneMapping?.mode || 'unconfirmed'} tone mapping. Display reports ${high.matches ? 'high' : 'standard'} dynamic range. ${hdr ? 'Highlights are emitted above SDR white; ' : ''}Physical brightness and panel accuracy are not measured. Capabilities update when the display changes.` };
      sampled=false;
      report(profile);
    }
    configure();
    const shader = device.createShaderModule({ code: `
      struct Params { size: vec2f, time: f32, focusLane: f32, packet: f32, hdr: f32, visible: f32, pad: f32 };
      @group(0) @binding(0) var<uniform> p: Params;
      @vertex fn vs(@builtin(vertex_index) i: u32) -> @builtin(position) vec4f {
        var v = array<vec2f,3>(vec2f(-1.,-1.),vec2f(3.,-1.),vec2f(-1.,3.));
        return vec4f(v[i],0.,1.);
      }
      @fragment fn fs(@builtin(position) pixel: vec4f) -> @location(0) vec4f {
        let xy = pixel.xy / p.size;
        var palette = array<vec3f,5>(vec3f(.25,1.,.58),vec3f(1.,.71,.28),vec3f(.65,.28,1.),vec3f(.25,.82,1.),vec3f(.74,.91,1.));
        var light = vec3f(0.); var alpha = 0.;
        for (var i=0u; i<5u; i++) {
          let center = vec2f((f32(i)+.5)/5.,74./180.);
          let d = (xy-center)*vec2f(p.size.x/p.size.y,1.);
          let r = length(d);
          let strength = select(.55,1.,abs(p.focusLane-f32(i))<.1);
          let core = exp(-r*r*1700.);
          let halo = exp(-r*r*250.)*.16;
          let ring = exp(-pow((r-.084)*260.,2.))*.11;
          let energy = core*mix(.9,3.2,p.hdr)*strength + halo + ring;
          light += palette[i]*energy;
          alpha = max(alpha, clamp(core+halo+ring,0.,1.));
        }
        let d = (xy-vec2f(p.packet,74./180.))*vec2f(p.size.x/p.size.y,1.);
        let dot = exp(-dot(d,d)*11000.) * p.visible;
        light += vec3f(.7,1.,.87)*dot*mix(1.,3.8,p.hdr);
        alpha = max(alpha,dot);
        return vec4f(light,alpha);
      }
    ` });
    const messages = await shader.getCompilationInfo();
    if (messages.messages.some(m => m.type === 'error')) throw new Error(messages.messages.filter(m => m.type === 'error').map(m => m.message).join('; '));
    const pipeline = await device.createRenderPipelineAsync({ layout: 'auto', vertex: { module: shader, entryPoint: 'vs' }, fragment: { module: shader, entryPoint: 'fs', targets: [{ format: 'rgba16float' }] }, primitive: { topology: 'triangle-list' } });
    const buffer = device.createBuffer({ size: 32, usage: GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST });
    const bindGroup = device.createBindGroup({ layout: pipeline.getBindGroupLayout(0), entries: [{ binding: 0, resource: { buffer } }] });
    let state = { active: -1, packet: .1, visible: false };
    const values = new Float32Array(8);
    function draw() {
      if (dead) return;
      const ratio = Math.min(devicePixelRatio || 1, 2);
      const w = Math.max(1, Math.round(canvas.clientWidth * ratio));
      const h = Math.max(1, Math.round(canvas.clientHeight * ratio));
      if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }
      values.set([w,h,0,state.active,state.packet,hdr ? 1 : 0,state.visible ? 1 : 0,0]);
      device.queue.writeBuffer(buffer,0,values);
      const surface = context.getCurrentTexture();
      const encoder = device.createCommandEncoder();
      const pass = encoder.beginRenderPass({ colorAttachments: [{ view: surface.createView(), clearValue: {r:0,g:0,b:0,a:0}, loadOp: 'clear', storeOp: 'store' }] });
      pass.setPipeline(pipeline); pass.setBindGroup(0,bindGroup); pass.draw(3); pass.end();
      let probe = null;
      if (!sampled) {
        sampled = true;
        probe = device.createBuffer({ size: 256, usage: GPUBufferUsage.COPY_DST | GPUBufferUsage.MAP_READ });
        encoder.copyTextureToBuffer({ texture: surface, origin: {x: Math.floor(w*.1), y: Math.floor(h*74/180)} }, { buffer: probe, bytesPerRow: 256 }, {width:1,height:1});
      }
      device.queue.submit([encoder.finish()]);
      if (probe) probe.mapAsync(GPUMapMode.READ).then(() => {
        const half = new Uint16Array(probe.getMappedRange());
        const decode = h => { const e=(h>>10)&31, m=h&1023; return (h&32768?-1:1)*(e===0 ? m*2**-24 : e===31 ? Infinity : (1+m/1024)*2**(e-15)); };
        const peak = Math.max(...Array.from(half.slice(0,3),decode));
        probe.unmap(); probe.destroy();
        if (!dead) report({...profile, detail: `${profile.detail} GPU highlight readback: ${peak.toFixed(2)} (SDR white = 1.00). This verifies the rendered signal, not display luminance.`});
      }).catch(() => probe.destroy());
    }
    function requestDraw() { if (!frame && !dead) frame = requestAnimationFrame(() => { frame = 0; try { draw(); } catch (error) { lose(error.message); } }); }
    function lose(reason) { dead = true; document.documentElement.classList.remove('gpu-active'); canvas.style.visibility = 'hidden'; describeFallback(reason); }
    device.addEventListener('uncapturederror', event => lose(event.error.message));
    device.lost.then(info => { if (!dead) lose(`GPU device lost: ${info.message}`); });
    const change = () => { if (!dead) { try { configure(); requestDraw(); } catch(error) { lose(error.message); } } };
    p3.addEventListener('change',change); high.addEventListener('change',change);
    const observer = new ResizeObserver(requestDraw); observer.observe(canvas);
    document.documentElement.classList.add('gpu-active');
    requestDraw();
    return { update(next) { state = {...state,...next}; requestDraw(); }, destroy() { dead=true; cancelAnimationFrame(frame); observer.disconnect(); p3.removeEventListener('change',change); high.removeEventListener('change',change); buffer.destroy(); device.destroy(); } };
  } catch(error) {
    device?.destroy(); canvas.style.visibility='hidden'; describeFallback(error.message);
    return { update() {}, destroy() {} };
  }
}
