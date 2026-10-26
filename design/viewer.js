// Outer Bounds Pro - dependency-free WebGL viewer for the model primitives (model.py → JSON).
(function () {
  const MODEL = JSON.parse(document.getElementById('modelData').textContent);
  const canvas = document.getElementById('gl');
  const gl = canvas.getContext('webgl', { antialias: true, preserveDrawingBuffer: true });
  if (!gl) { document.getElementById('glFallback').hidden = false; return; }

  const VS = `attribute vec3 p; attribute vec3 n; uniform mat4 mvp; uniform mat4 mdl; varying vec3 vn; varying vec3 vp;
    void main(){ vn = mat3(mdl) * n; vp = (mdl*vec4(p,1.0)).xyz; gl_Position = mvp*vec4(p,1.0); }`;
  const FS = `precision mediump float; varying vec3 vn; varying vec3 vp; uniform vec3 col; uniform float alpha; uniform vec3 eye; uniform float hi;
    void main(){ vec3 N = normalize(vn); vec3 L1 = normalize(vec3(0.4,0.8,0.6)); vec3 L2 = normalize(vec3(-0.6,0.2,-0.5));
      vec3 V = normalize(eye-vp); float d = max(dot(N,L1),0.0)*0.75 + max(dot(N,L2),0.0)*0.25 + 0.28;
      float s = pow(max(dot(reflect(-L1,N),V),0.0), 24.0)*0.25; vec3 c = col*d + s + hi*vec3(0.25,0.18,0.0);
      gl_FragColor = vec4(c, alpha); }`;
  function sh(t, s) { const o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); return o; }
  const prog = gl.createProgram(); gl.attachShader(prog, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(prog); gl.useProgram(prog);
  const loc = { p: gl.getAttribLocation(prog, 'p'), n: gl.getAttribLocation(prog, 'n'), mvp: gl.getUniformLocation(prog, 'mvp'), mdl: gl.getUniformLocation(prog, 'mdl'),
    col: gl.getUniformLocation(prog, 'col'), alpha: gl.getUniformLocation(prog, 'alpha'), eye: gl.getUniformLocation(prog, 'eye'), hi: gl.getUniformLocation(prog, 'hi') };

  const hex = h => [1, 3, 5].map(i => parseInt(h.substr(i, 2), 16) / 255);
  function rotY(v, c, deg) { if (!deg) return v; const r = deg * Math.PI / 180, x = v[0] - c[0], z = v[2] - c[2];
    return [c[0] + x * Math.cos(r) + z * Math.sin(r), v[1], c[2] - x * Math.sin(r) + z * Math.cos(r)]; }
  function geom(p) {
    const P = [], N = [];
    const quad = (a, b, c, d, n) => { [a, b, c, a, c, d].forEach(v => { P.push(...v); N.push(...n); }); };
    const c = p.c;
    if (p.t === 'sph') {
      const n = 24, m = 14, r = p.r;
      const V = (a, b) => [Math.sin(a) * Math.cos(b), Math.cos(a), Math.sin(a) * Math.sin(b)];
      for (let i = 0; i < m; i++) for (let j = 0; j < n; j++) {
        const a0 = Math.PI * i / m, a1 = Math.PI * (i + 1) / m, b0 = 2 * Math.PI * j / n, b1 = 2 * Math.PI * (j + 1) / n;
        [[a0, b0], [a1, b0], [a1, b1], [a0, b0], [a1, b1], [a0, b1]].forEach(([a, b]) => { const u = V(a, b); P.push(c[0] + r * u[0], c[1] + r * u[1], c[2] + r * u[2]); N.push(...u); });
      }
      return { P: new Float32Array(P), N: new Float32Array(N) };
    }
    if (p.t === 'mesh') {   // convex faceted solid: fan-triangulate each face, flat normals
      p.f.forEach((f, i) => { const n = p.fn[i]; for (let k = 1; k + 1 < f.length; k++) [f[0], f[k], f[k + 1]].forEach(j => { P.push(...p.v[j]); N.push(...n); }); });
      return { P: new Float32Array(P), N: new Float32Array(N) };
    }
    if (p.t === 'box') {
      const [hx, hy, hz] = p.s.map(v => v / 2);
      const V = (sx, sy, sz) => rotY([c[0] + sx * hx, c[1] + sy * hy, c[2] + sz * hz], c, p.ry);
      const R = n => rotY(n, [0, 0, 0], p.ry);
      quad(V(1, -1, -1), V(1, 1, -1), V(1, 1, 1), V(1, -1, 1), R([1, 0, 0])); quad(V(-1, -1, -1), V(-1, -1, 1), V(-1, 1, 1), V(-1, 1, -1), R([-1, 0, 0]));
      quad(V(-1, 1, -1), V(-1, 1, 1), V(1, 1, 1), V(1, 1, -1), R([0, 1, 0])); quad(V(-1, -1, -1), V(1, -1, -1), V(1, -1, 1), V(-1, -1, 1), R([0, -1, 0]));
      quad(V(-1, -1, 1), V(1, -1, 1), V(1, 1, 1), V(-1, 1, 1), R([0, 0, 1])); quad(V(-1, -1, -1), V(-1, 1, -1), V(1, 1, -1), V(1, -1, -1), R([0, 0, -1]));
    } else {
      const n = Math.max(p.seg, 24), r = p.r, h = p.h;
      const at = (u, v, w) => ({ x: [w, u, v], y: [u, w, v], z: [u, v, w] })[p.ax];
      const W = (u, v, w) => { const a = at(u, v, w); return rotY([c[0] + a[0], c[1] + a[1], c[2] + a[2]], c, p.ry); };
      const Nn = (u, v, w) => rotY(at(u, v, w), [0, 0, 0], p.ry);
      for (let k = 0; k < n; k++) {
        const a0 = 2 * Math.PI * k / n, a1 = 2 * Math.PI * (k + 1) / n;
        const u0 = r * Math.cos(a0), v0 = r * Math.sin(a0), u1 = r * Math.cos(a1), v1 = r * Math.sin(a1);
        const nm = Nn(Math.cos((a0 + a1) / 2), Math.sin((a0 + a1) / 2), 0);
        quad(W(u0, v0, -h / 2), W(u1, v1, -h / 2), W(u1, v1, h / 2), W(u0, v0, h / 2), nm);
        [[h / 2, 1], [-h / 2, -1]].forEach(([w, s]) => { const nn = Nn(0, 0, s); const cc = W(0, 0, w);
          const A = W(u0, v0, w), B = W(u1, v1, w); (s > 0 ? [cc, A, B] : [cc, B, A]).forEach(v => { P.push(...v); N.push(...nn); }); });
      }
    }
    return { P: new Float32Array(P), N: new Float32Array(N) };
  }
  const meshes = MODEL.prims.concat((MODEL.scene || []).map(q => Object.assign({ scene: true }, q))).map(p => { const g = geom(p); const pb = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, pb); gl.bufferData(gl.ARRAY_BUFFER, g.P, gl.STATIC_DRAW);
    const nb = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, nb); gl.bufferData(gl.ARRAY_BUFFER, g.N, gl.STATIC_DRAW);
    return { p, pb, nb, count: g.P.length / 3, col: hex(p.col) }; });

  // ---------------------------------------------------------- math
  const persp = (f, a, n, fa) => { const t = 1 / Math.tan(f / 2); return [t / a, 0, 0, 0, 0, t, 0, 0, 0, 0, (fa + n) / (n - fa), -1, 0, 0, 2 * fa * n / (n - fa), 0]; };
  const mul = (a, b) => { const o = new Array(16).fill(0); for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) for (let k = 0; k < 4; k++) o[j * 4 + i] += a[k * 4 + i] * b[j * 4 + k]; return o; };
  const lookAt = (e, c, u) => { let z = [e[0] - c[0], e[1] - c[1], e[2] - c[2]]; let l = Math.hypot(...z); z = z.map(v => v / l);
    let x = [u[1] * z[2] - u[2] * z[1], u[2] * z[0] - u[0] * z[2], u[0] * z[1] - u[1] * z[0]]; l = Math.hypot(...x); x = x.map(v => v / l);
    const y = [z[1] * x[2] - z[2] * x[1], z[2] * x[0] - z[0] * x[2], z[0] * x[1] - z[1] * x[0]];
    return [x[0], y[0], z[0], 0, x[1], y[1], z[1], 0, x[2], y[2], z[2], 0, -(x[0] * e[0] + x[1] * e[1] + x[2] * e[2]), -(y[0] * e[0] + y[1] * e[1] + y[2] * e[2]), -(z[0] * e[0] + z[1] * e[1] + z[2] * e[2]), 1]; };
  const trans = (t) => [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, t[0], t[1], t[2], 1];

  // ---------------------------------------------------------- state
  const S = { az: -38, el: 20, dist: 640, explode: 0, xray: false, hidden: new Set(), hover: null, target: [0, 20, 0], setup: false };
  const SETUP_TARGET = MODEL.setupTarget || [1300, 300, 600];
  const setupBox = document.getElementById('showSetup');
  function setSetup(on) { S.setup = on; if (setupBox) setupBox.checked = on; }
  const groups = [...new Set(MODEL.prims.map(p => p.g))];
  const gbox = document.getElementById('groupToggles');
  groups.forEach(g => { const l = document.createElement('label'); const c = document.createElement('input'); c.type = 'checkbox'; c.checked = true;
    c.addEventListener('change', () => { c.checked ? S.hidden.delete(g) : S.hidden.add(g); draw(); }); l.append(c, document.createTextNode(' ' + g)); gbox.appendChild(l); });
  const views = { iso: [-38, 20], front: [0, 0], rear: [180, 0], top: [0, 89], left: [-90, 0], right: [90, 0], under: [-30, -40], ball: [-55, 8],
    setup: [-135, 28, 5600, [1100, 300, 500]], plan: [0, 89, 7400, SETUP_TARGET], golfer: [10, 52, 2300, [-60, -40, 250]], behind: [-90, 12, 3800, [600, 300, 492]] };
  document.querySelectorAll('[data-view]').forEach(b => b.addEventListener('click', () => { const v = views[b.dataset.view];
    document.querySelectorAll('[data-view]').forEach(x => x.classList.toggle('on', x === b));
    if (v.length > 2) { setSetup(true); animateTo(v[0], v[1], v[2], v[3]); } else { if (S.setup) { setSetup(false); } animateTo(v[0], v[1], 640, [0, 20, 0]); } }));
  if (setupBox) setupBox.addEventListener('change', e => { const on = e.target.checked; const v = on ? views.setup : views.iso; setSetup(on); animateTo(v[0], v[1], on ? v[2] : 640, on ? v[3] : [0, 20, 0]); });
  const ex = document.getElementById('explode'); ex.addEventListener('input', () => { S.explode = +ex.value / 100; draw(); });
  document.getElementById('xray').addEventListener('change', e => { S.xray = e.target.checked; draw(); });
  document.getElementById('hideShell').addEventListener('change', e => {
    MODEL.shellGroups.forEach(g => e.target.checked ? S.hidden.add(g) : S.hidden.delete(g));
    gbox.querySelectorAll('label').forEach(l => { const g = l.textContent.trim(); l.querySelector('input').checked = !S.hidden.has(g); }); draw(); });
  document.getElementById('snap').addEventListener('click', () => { draw(); const a = document.createElement('a'); a.download = 'outer-bounds-pro.png'; a.href = canvas.toDataURL('image/png'); a.click(); });

  function animateTo(az, el, dist, tgt) { const a0 = S.az, e0 = S.el, d0 = S.dist, t0v = S.target.slice(); let d = az - a0; while (d > 180) d -= 360; while (d < -180) d += 360;
    const d1 = dist || S.dist, t1 = tgt || S.target; const t0 = performance.now();
    (function step(t) { const k = Math.min(1, (t - t0) / 550), s = k * k * (3 - 2 * k); S.az = a0 + d * s; S.el = e0 + (el - e0) * s; S.dist = d0 + (d1 - d0) * s;
      S.target = t0v.map((v, i) => v + (t1[i] - v) * s); draw(); if (k < 1) requestAnimationFrame(step); })(t0); }

  let drag = null;
  canvas.addEventListener('pointerdown', e => { drag = { x: e.clientX, y: e.clientY, pan: e.shiftKey || e.button === 2 }; canvas.setPointerCapture(e.pointerId); });
  canvas.addEventListener('pointerup', () => drag = null);
  canvas.addEventListener('contextmenu', e => e.preventDefault());
  canvas.addEventListener('pointermove', e => {
    if (drag) { const dx = e.clientX - drag.x, dy = e.clientY - drag.y; drag.x = e.clientX; drag.y = e.clientY;
      if (drag.pan) { const a = S.az * Math.PI / 180; const k = S.dist / 700; S.target[0] -= dx * Math.cos(a) * k; S.target[2] += dx * Math.sin(a) * k; S.target[1] += dy * k; }
      else { S.az -= dx * 0.4; S.el = Math.max(-89, Math.min(89, S.el + dy * 0.35)); } draw(); return; }
    pick(e);
  });
  canvas.addEventListener('pointerleave', () => { S.hover = null; tipEl.style.opacity = 0; draw(); });
  canvas.addEventListener('wheel', e => { e.preventDefault(); S.dist = Math.max(160, Math.min(12000, S.dist * (1 + e.deltaY * 0.001))); draw(); }, { passive: false });

  function eyePos() { const a = S.az * Math.PI / 180, el = S.el * Math.PI / 180;
    return [S.target[0] + S.dist * Math.cos(el) * Math.sin(a), S.target[1] + S.dist * Math.sin(el), S.target[2] + S.dist * Math.cos(el) * Math.cos(a)]; }
  let VP = null;
  function draw() {
    const dpr = S.fw ? 1 : (window.devicePixelRatio || 1), w = S.fw || canvas.clientWidth, h = S.fh || canvas.clientHeight;
    if (canvas.width !== w * dpr || canvas.height !== h * dpr) { canvas.width = w * dpr; canvas.height = h * dpr; }
    gl.viewport(0, 0, canvas.width, canvas.height);
    const bg = getComputedStyle(document.documentElement).getPropertyValue('--viewer-bg').trim() || '#eef0f2';
    const b = hex(bg.length === 7 ? bg : '#eef0f2'); gl.clearColor(b[0], b[1], b[2], 1); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.enable(gl.DEPTH_TEST); gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
    const e = eyePos(); const up = Math.abs(S.el) > 88 ? [0, 0, -1] : [0, 1, 0];
    VP = mul(persp(0.62, w / h, 10, 40000), lookAt(e, S.target, up)); gl.uniform3fv(loc.eye, e);
    const order = [...meshes].filter(m => !S.hidden.has(m.p.g) && (S.setup || !m.p.scene));
    const opaque = order.filter(m => m.p.a >= 1 && !(S.xray && m.p.ext)), trans_ = order.filter(m => !(m.p.a >= 1 && !(S.xray && m.p.ext)));
    const drawM = (m, alpha) => { const t = m.p.ex.map(v => v * S.explode); const M = trans(t); gl.uniformMatrix4fv(loc.mvp, false, mul(VP, M)); gl.uniformMatrix4fv(loc.mdl, false, M);
      gl.uniform3fv(loc.col, m.col); gl.uniform1f(loc.alpha, alpha); gl.uniform1f(loc.hi, S.hover === m.p.g ? 1 : 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, m.pb); gl.enableVertexAttribArray(loc.p); gl.vertexAttribPointer(loc.p, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, m.nb); gl.enableVertexAttribArray(loc.n); gl.vertexAttribPointer(loc.n, 3, gl.FLOAT, false, 0, 0); gl.drawArrays(gl.TRIANGLES, 0, m.count); };
    gl.depthMask(true); opaque.forEach(m => drawM(m, 1));
    gl.depthMask(false); trans_.forEach(m => drawM(m, S.xray && m.p.ext ? 0.12 : m.p.a)); gl.depthMask(true);
  }
  // picking: project primitive centres, pick nearest within radius (cheap & good enough for labels)
  const tipEl = document.getElementById('viewerTip');
  function pick(e) {
    if (!VP) return; const r = canvas.getBoundingClientRect(); const mx = e.clientX - r.left, my = e.clientY - r.top;
    let best = null, bd = 28;
    meshes.forEach(m => { if (S.hidden.has(m.p.g) || (m.p.scene && !S.setup)) return; if (S.xray && m.p.ext) return; const c = m.p.c.map((v, i) => v + m.p.ex[i] * S.explode);
      const v = [c[0], c[1], c[2], 1]; const o = [0, 0, 0, 0]; for (let i = 0; i < 4; i++) for (let k = 0; k < 4; k++) o[i] += VP[k * 4 + i] * v[k];
      if (o[3] <= 0) return; const sx = (o[0] / o[3] * 0.5 + 0.5) * r.width, sy = (1 - (o[1] / o[3] * 0.5 + 0.5)) * r.height; const d = Math.hypot(sx - mx, sy - my);
      if (d < bd) { bd = d; best = m; } });
    const g = best ? best.p.g : null; if (g !== S.hover) { S.hover = g; draw(); }
    if (best) { tipEl.replaceChildren(); const a = document.createElement('b'); a.textContent = best.p.n; const b2 = document.createElement('div'); b2.textContent = best.p.g; tipEl.append(a, b2);
      tipEl.style.left = (mx + 14) + 'px'; tipEl.style.top = (my + 10) + 'px'; tipEl.style.opacity = 1; } else tipEl.style.opacity = 0;
  }
  new ResizeObserver(draw).observe(canvas);
  window.OB_redraw3d = draw;
  // Static renders for the gallery: z-buffered snapshots from this same renderer.
  window.OB_snapshot = function (o) {
    const keep = { az: S.az, el: S.el, dist: S.dist, explode: S.explode, xray: S.xray, hidden: new Set(S.hidden), target: S.target.slice(), hover: S.hover, setup: S.setup, fw: 0, fh: 0 };
    S.az = o.az; S.el = o.el; S.dist = o.dist || 560; S.explode = o.explode || 0; S.xray = false; S.hover = null; S.target = o.target || [0, 0, 0]; S.setup = !!o.setup;
    S.hidden = new Set(o.hide || []); S.fw = 1200; S.fh = 900; draw(); const url = canvas.toDataURL('image/png'); S.fw = S.fh = 0;
    Object.assign(S, keep); draw(); return url;
  };
  document.querySelectorAll('img[data-snap]').forEach(img => { img.src = window.OB_snapshot(JSON.parse(img.dataset.snap)); });
  draw();
})();
