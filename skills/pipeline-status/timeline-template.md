# Application timeline template

`timeline.html` for the **`pipeline-status`** skill. It is a fixed page: the layout, markers, filter,
legend and tooltips all live here and are never rewritten by hand. The page loads its data from
`timeline-data.js` in the same folder and derives everything it draws in the browser.

**To install or refresh the page**, copy the block below into
`{user_dir}/CareerNavigator/timeline.html` exactly as written, from `<!DOCTYPE html>` to `</html>`.
Do not retype, reformat, summarize or "improve" it. Extracting it with a command is the reliable way:

```bash
awk '/^```html$/{f=1;next} /^```$/{f=0} f' "{plugin_dir}/skills/pipeline-status/timeline-template.md" > "{user_dir}/CareerNavigator/timeline.html"
```

The second line of the page carries a version marker (`career-navigator timeline template v2`). If an
existing `timeline.html` has the same marker, leave it alone and only refresh `timeline-data.js`.

## What the page shows

- One row per application, most recently submitted first, on a shared month axis with a dashed "today" line.
- A line from when the role entered the pipeline to its end: today for active applications, the last event
  for closed ones, and a fade-out for ghosted ones.
- Things the user did sit **on** the line: added to pipeline (ring), application submitted (diamond),
  outreach (triangle), withdrawn or declined (open square), note (dot).
- Things the employer did float **above** the line: recruiter or contact reached out, phone screen or
  interview, offer (star), rejected (cross), gone quiet (three dots), meeting held (square).
- A filter (Active, All, Rejected, Ghosted, Withdrawn / declined), a count, a legend, and a hover tooltip
  listing every dated event and contact interaction for the row.

## The data file

`timeline-data.js` is described in the skill (section 5). Its shape, with one fictional application:

```js
window.TIMELINE_RAW = {"generated":"2026-01-15T02:15:00","applications":[
  {"company":"Acme Corp","role":"Senior Product Manager","status":"phone_screen","outcome":"pending",
   "priority":"high","date_added":"2026-01-02","date_applied":"2026-01-05",
   "stage_history":[
     {"date":"2026-01-05","stage":"applied","notes":"Applied via careers page."},
     {"date":"2026-01-12","stage":"phone_screen","notes":"30-minute recruiter screen."}],
   "contacts":[
     {"name":"Jordan Lee","interactions":[
       {"date":"2026-01-08","type":"email","notes":"Sent a short note to the recruiter."},
       {"date":"2026-01-09","type":"email_reply","notes":"Recruiter replied with times."}]}]}
]};
```

## The page

```html
<!DOCTYPE html>
<!-- career-navigator timeline template v2 -->
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Application Pipeline — Timeline</title>
<style id="tl-style">
html,body{height:100%;margin:0;padding:0}
#tl-root{height:100%;display:flex;flex-direction:column;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#1a1a1a;background:#fff;font-size:13px}
#tl-root *{box-sizing:border-box}
#tl-root h1{flex:none;font-size:16px;font-weight:600;margin:0 0 10px}
#tl-root .tl-sub{font-size:11px;color:#9ca3af;font-weight:400}
#tl-root .tl-legend{flex:none;display:flex;flex-wrap:wrap;gap:14px;align-items:center;font-size:11px;color:#4b5563}
#tl-root .tl-legend .li{display:inline-flex;align-items:center;gap:5px}
#tl-root .tl-legend .tl-legend-head{font-weight:600;color:#374151;margin-left:4px}
#tl-root .tl-legend .tl-legend-head:first-child{margin-left:0}
#tl-root .tl-legend svg{overflow:visible}
#tl-root .tl-legend{margin:10px 0 0;padding-top:10px;border-top:1px solid #f0f0f0}
#tl-root .tl-controls{flex:none;display:flex;align-items:center;gap:8px;margin:0 0 12px;font-size:11px;color:#4b5563}
#tl-root .tl-controls select{font-size:11px;padding:3px 8px;border:0.5px solid #d1d5db;border-radius:6px;background:#fff;color:#1a1a1a;cursor:pointer}
#tl-root .tl-controls .tl-count{color:#9ca3af}
#tl-root .tl-axis-head{flex:none;width:100%;overflow:hidden}
#tl-root .tl-wrap{flex:1 1 auto;min-height:0;position:relative;width:100%;overflow-y:auto;overflow-x:hidden}
#tl-root svg.tl-chart{display:block;width:100%;height:auto;font-family:inherit}
#tl-root .rowhit{cursor:default}
#tl-root .rowhit:hover .rowbg{fill:#f6f7f9}
#tl-root .colab{font-size:11px;fill:#374151}
#tl-root .mlab{font-size:10px;fill:#9ca3af}
#tl-root .axis{stroke:#eceef1;stroke-width:1}
#tl-root .todayln{stroke:#10b981;stroke-width:1;stroke-dasharray:2 3}
#tl-root .tl-tip{position:fixed;pointer-events:none;z-index:9999;background:#111827;color:#f9fafb;padding:8px 10px;border-radius:7px;font-size:11px;line-height:1.45;width:280px;box-shadow:0 6px 20px rgba(0,0,0,.25);opacity:0;transition:opacity .08s;white-space:normal}
#tl-root .tl-tip b{color:#fff}
#tl-root .tl-tip .ev{color:#cbd5e1}
</style>
</head>
<body>
<div id="tl-root">
  <h1>Application Pipeline — Timeline <span class="tl-sub" id="tl-stamp"></span></h1>
  <div class="tl-controls">
    <label for="tl-filter">Show</label>
    <select id="tl-filter">
      <option value="active" selected>Active</option>
      <option value="all">All</option>
      <option value="rejected">Rejected</option>
      <option value="ghosted">Ghosted</option>
      <option value="closed">Withdrawn / declined</option>
    </select>
    <span class="tl-count" id="tl-count"></span>
  </div>
  <div class="tl-axis-head" id="tl-axis"></div>
  <div class="tl-wrap" id="tl-wrap"></div>
  <div class="tl-legend" id="tl-legend"></div>
  <div class="tl-tip" id="tl-tip"></div>
</div>

<script src="timeline-data.js"></script>
<script id="tl-script">
// ---- model: built in the browser from timeline-data.js ----------------------
// timeline-data.js sets window.TIMELINE_RAW = { generated, applications:[...] }.
// Each application is its tracker.json summary row plus `stage_history` (from its
// applications/<id>.json detail file) and `contacts` (from its contacts file).
// Everything below derives the drawable rows; nothing is precomputed on disk.
const APPLY_STAGES = ['applied','re-applied'];
const TERMINAL_REJECT = ['rejected'];
const TERMINAL_OUT = ['withdrawn','declined_by_candidate'];
function glyphFor(stage){
  if(APPLY_STAGES.includes(stage)) return ['applied','mine'];
  if(stage==='considering') return ['discovered','mine'];
  if(stage==='recruiter') return ['response','theirs'];
  if(stage==='phone_screen') return ['screen','theirs'];
  if(['interview','onsite','final','panel'].includes(stage)) return ['screen','theirs'];
  if(stage==='offer') return ['offer','theirs'];
  if(stage==='rejected') return ['rejected','theirs'];
  if(stage==='ghosted') return ['ghosted','theirs'];
  if(TERMINAL_OUT.includes(stage)) return ['closed','mine'];
  return ['update','mine'];
}
function buildModel(raw, todayOverride){
  const pad = n => String(n).padStart(2,'0');
  const now = new Date();
  const TODAY = todayOverride || `${now.getFullYear()}-${pad(now.getMonth()+1)}-${pad(now.getDate())}`;
  const dd = s => (typeof s==='string' && s.length>=10) ? s : null;
  const clip = s => Array.from(s||'').slice(0,400).join('');
  const byDate = (a,b) => a.date<b.date ? -1 : a.date>b.date ? 1 : 0;
  const minS = arr => arr.reduce((m,v)=> v<m ? v : m);
  const maxS = arr => arr.reduce((m,v)=> v>m ? v : m);
  const rows = [];
  ((raw && raw.applications) || []).forEach(a=>{
    const sh = (a.stage_history||[]).filter(s=>s && dd(s.date)).slice().sort(byDate);
    let cand = sh.map(s=>s.date);
    ['date_added','date_applied','applied_date'].forEach(k=>{ if(dd(a[k])) cand.push(a[k]); });
    if(!cand.length) return;                       // nothing to place on a time axis

    // contact interactions (outreach / responses / meetings)
    const touches = [];
    (a.contacts||[]).forEach(c=>{
      const who = (c && c.name) || 'Contact';
      ((c && c.interactions)||[]).forEach(it=>{
        if(!it || !dd(it.date)) return;
        const t = (it.type||'').toLowerCase();
        let kind;
        if(t.includes('meet') || t.includes('zoom') || t==='phone_screen') kind='meeting';
        else if(t.includes('inbound') || t.endsWith('_reply')) kind='inbound';
        else kind='outbound';
        touches.push({date:it.date, dir:kind, type:t||'contact', who:who, note:clip(it.notes)});
      });
    });
    touches.sort(byDate);
    if(touches.length) cand = cand.concat(touches.map(x=>x.date));

    const start = minS(cand);
    const applied = dd(a.date_applied) || dd(a.applied_date);
    const status = (a.status||'').toLowerCase();
    const outcome = (a.outcome||'').toLowerCase();

    // event markers from stage history
    const events = sh.map(s=>{
      const st = (s.stage||'').toLowerCase();
      const gw = glyphFor(st);
      return {date:s.date, stage:st||'update', g:gw[0], who:gw[1], note:clip(s.notes)};
    });
    // a discovery ring sits at the very start if the first event isn't already there
    if(!events.length || events[0].date > start)
      events.unshift({date:start, stage:'discovered', g:'discovered', who:'mine', note:''});
    // an applied diamond always exists once there is an application date
    if(applied && !events.some(e=>e.g==='applied'))
      events.push({date:applied, stage:'applied', g:'applied', who:'mine', note:''});
    events.sort(byDate);

    const lastEvent = maxS(events.map(e=>e.date));
    const ghosted = status==='ghosted';
    let ghostDate = null;
    if(ghosted){
      // an explicit "ghosted" stage is the recognized date; otherwise the silence
      // runs to the present, so the line fades out to today.
      const gd = events.filter(e=>e.g==='ghosted').map(e=>e.date);
      ghostDate = gd.length ? gd[0] : (TODAY>lastEvent ? TODAY : lastEvent);
    }
    const active = !ghosted && !TERMINAL_REJECT.includes(status) && !TERMINAL_OUT.includes(status)
                   && (outcome==='pending' || outcome==='');
    const end = ghosted ? ghostDate : active ? (TODAY>lastEvent ? TODAY : lastEvent) : lastEvent;

    rows.push({co:a.company||'—', role:a.role||'', status:status||'unknown', outcome:outcome,
               priority:(a.priority||'').toLowerCase(), start:start, applied:applied, end:end,
               ghost:ghostDate, active:active, events:events, touches:touches});
  });
  // most recently submitted at top (fall back to start date); company as stable tiebreak
  rows.sort((p,q)=> p.co<q.co ? -1 : p.co>q.co ? 1 : 0);
  rows.sort((p,q)=>{ const kp=p.applied||p.start, kq=q.applied||q.start; return kp<kq ? 1 : kp>kq ? -1 : 0; });
  return {generated:(raw && raw.generated) || '', today:TODAY, rows:rows};
}
const TL = buildModel(window.TIMELINE_RAW);
// ---- end model -----------------------------------------------------------------

const C = {
  active:'#2563eb', applied:'#2563eb', screen:'#059669', interview:'#059669',
  offer:'#15803d', rejected:'#dc2626', ghosted:'#d97706', closed:'#6b7280', unknown:'#6b7280',
  contact:'#7c3aed'
};
function lineColor(r){
  if(r.ghost) return C.ghosted;
  if(r.status==='rejected') return C.rejected;
  if(r.status==='withdrawn'||r.status==='declined_by_candidate') return C.closed;
  if(r.status==='phone_screen') return C.screen;
  return C.active;
}
const parse = s => new Date(s+'T00:00:00');
const DAY = 86400000;

// ---- marker shapes (small, centered at 0,0) --------------------------------
function marker(g, color){
  switch(g){
    case 'discovered': return `<circle r="3.4" fill="#fff" stroke="${color}" stroke-width="1.4"/>`;
    case 'applied':    return `<path d="M0,-4.6 L4.6,0 L0,4.6 L-4.6,0 Z" fill="${color}"/>`;
    case 'outreach':   return `<path d="M-3.4,-3.2 L3.6,0 L-3.4,3.2 Z" fill="${color}"/>`;
    case 'closed':     return `<rect x="-3.1" y="-3.1" width="6.2" height="6.2" rx="1" fill="#fff" stroke="${color}" stroke-width="1.4"/>`;
    case 'screen':
    case 'interview':  return `<circle r="3.6" fill="${color}"/>`;
    case 'offer':      return `<path d="M0,-5 L1.4,-1.6 L5,-1.6 L2.1,0.6 L3.2,4.2 L0,2 L-3.2,4.2 L-2.1,0.6 L-5,-1.6 L-1.4,-1.6 Z" fill="${color}"/>`;
    case 'rejected':   return `<path d="M-3.2,-3.2 L3.2,3.2 M3.2,-3.2 L-3.2,3.2" stroke="${color}" stroke-width="1.6" stroke-linecap="round"/>`;
    case 'ghosted':    return `<g fill="${color}"><circle cx="-3" cy="0" r="1"/><circle cx="0" cy="0" r="1"/><circle cx="3" cy="0" r="1"/></g>`;
    case 'response':   return `<circle r="2.7" fill="${color}"/>`;
    case 'meeting':    return `<rect x="-2.6" y="-2.6" width="5.2" height="5.2" rx="1" fill="${color}"/>`;
    default:           return `<circle r="2" fill="${color}"/>`;
  }
}

// color for a given glyph, falling back to the row's own status color for
// the "mine" glyphs (discovered / applied / closed / update) so those stay
// visually tied to the row's overall state.
function eventColor(g, rowColor){
  if(g==='rejected') return C.rejected;
  if(g==='ghosted') return C.ghosted;
  if(g==='screen'||g==='interview') return C.screen;
  if(g==='offer') return C.offer;
  if(g==='response'||g==='meeting'||g==='outreach') return C.contact;
  return rowColor;
}

const LEGEND_MINE = [
  ['discovered','Added to pipeline'],
  ['applied','Application submitted'],
  ['outreach','You reached out'],
  ['closed','Withdrawn / declined by you'],
  ['update','Note added'],
];
const LEGEND_THEIRS = [
  ['response','Recruiter / contact reached out'],
  ['screen','Phone screen / interview'],
  ['offer','Offer'],
  ['rejected','Rejected'],
  ['ghosted','Gone quiet (ghosted)'],
  ['meeting','Meeting held'],
];

const LABEL_W = 168, PAD_R = 20, ROW_H = 20, AXIS_H = 26, BOT = 14;

let VIEW = [];              // rows currently drawn (post-filter), indexed by data-i
let FILTER = 'active';

function matchFilter(r,f){
  if(f==='all') return true;
  if(f==='active') return !!r.active;
  if(f==='ghosted') return !!r.ghost;
  if(f==='rejected') return r.status==='rejected';
  if(f==='closed') return r.status==='withdrawn' || r.status==='declined_by_candidate';
  return true;
}

function render(){
  const wrap = document.getElementById('tl-wrap');
  const head = document.getElementById('tl-axis');
  const W = Math.max(640, wrap.clientWidth || 900);
  const plotX0 = LABEL_W, plotX1 = W - PAD_R, plotW = plotX1 - plotX0;
  const rows = TL.rows.filter(r=>matchFilter(r,FILTER));
  VIEW = rows;
  const cnt = document.getElementById('tl-count');
  if(cnt) cnt.textContent = `${rows.length} of ${TL.rows.length} applications`;
  if(!rows.length){
    head.innerHTML = '';
    wrap.innerHTML = '<svg class="tl-chart" viewBox="0 0 640 40"><text x="12" y="24" class="mlab">No applications match this filter.</text></svg>';
    return;
  }

  // time domain (include stage events, span endpoints, and contact touches)
  let lo = Infinity, hi = -Infinity;
  rows.forEach(r=>{ r.events.forEach(e=>{const t=parse(e.date).getTime(); if(t<lo)lo=t; if(t>hi)hi=t;});
                    (r.touches||[]).forEach(e=>{const t=parse(e.date).getTime(); if(t<lo)lo=t; if(t>hi)hi=t;});
                    const s=parse(r.start).getTime(), en=parse(r.end).getTime();
                    if(s<lo)lo=s; if(en>hi)hi=en; });
  const todayT = parse(TL.today).getTime(); if(todayT>hi)hi=todayT;
  lo -= 5*DAY; hi += 6*DAY;
  const x = t => plotX0 + (t-lo)/(hi-lo)*plotW;

  // month ticks
  let ticks=[]; const dLo=new Date(lo);
  let m=new Date(dLo.getFullYear(), dLo.getMonth(), 1);
  if(m.getTime()<lo) m=new Date(m.getFullYear(), m.getMonth()+1, 1);
  const MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  while(m.getTime()<=hi){ ticks.push(new Date(m)); m=new Date(m.getFullYear(), m.getMonth()+1, 1); }
  const xt = x(todayT);
  const bodyH = rows.length*ROW_H + 6;

  // ---- fixed axis header (does not scroll) --------------------------------
  let hs = `<svg class="tl-chart" viewBox="0 0 ${W} ${AXIS_H}" style="width:${W}px;height:${AXIS_H}px" preserveAspectRatio="xMinYMin meet">`;
  ticks.forEach(t=>{ const xp=x(t.getTime());
    hs += `<text class="mlab" x="${xp.toFixed(1)}" y="${AXIS_H-9}" text-anchor="middle">${MON[t.getMonth()]}${t.getMonth()===0?" '"+String(t.getFullYear()).slice(2):''}</text>`;
  });
  hs += `<text class="mlab" x="${xt.toFixed(1)}" y="10" text-anchor="middle" fill="#10b981">today</text>`;
  hs += `<line class="axis" x1="0" y1="${AXIS_H-1}" x2="${W}" y2="${AXIS_H-1}"/></svg>`;
  head.innerHTML = hs;

  // ---- scrollable body ----------------------------------------------------
  let s = `<svg class="tl-chart" viewBox="0 0 ${W} ${bodyH}" style="width:${W}px;height:${bodyH}px" preserveAspectRatio="xMinYMin meet" role="img">`;
  let defs = '<defs>';
  ticks.forEach(t=>{ const xp=x(t.getTime());
    s += `<line class="axis" x1="${xp.toFixed(1)}" y1="0" x2="${xp.toFixed(1)}" y2="${bodyH}"/>`;
  });
  s += `<line class="todayln" x1="${xt.toFixed(1)}" y1="0" x2="${xt.toFixed(1)}" y2="${bodyH}"/>`;

  rows.forEach((r,i)=>{
    const yc = i*ROW_H + ROW_H/2;
    const col = lineColor(r);
    const xs = x(parse(r.start).getTime());
    const xe = x(parse(r.end).getTime());

    // row hit area + hover background
    s += `<g class="rowhit" data-i="${i}">`;
    s += `<rect class="rowbg" x="0" y="${i*ROW_H}" width="${W}" height="${ROW_H}" fill="transparent"/>`;

    // label (company) — truncated via textLength safety
    const co = r.co.length>24 ? r.co.slice(0,23)+'…' : r.co;
    s += `<text class="colab" x="10" y="${yc+3}">${esc(co)}</text>`;

    // the line
    if(r.ghost){
      const xa = x(parse(r.applied||r.start).getTime());
      const gid = 'g'+i;
      const af = Math.max(0, Math.min(1, (xa-xs)/Math.max(1,(xe-xs))));
      defs += `<linearGradient id="${gid}" gradientUnits="userSpaceOnUse" x1="${xs}" y1="0" x2="${xe}" y2="0">`
            + `<stop offset="0" stop-color="${col}" stop-opacity="0.9"/>`
            + `<stop offset="${af.toFixed(3)}" stop-color="${col}" stop-opacity="0.9"/>`
            + `<stop offset="1" stop-color="${col}" stop-opacity="0"/></linearGradient>`;
      s += `<line x1="${xs.toFixed(1)}" y1="${yc}" x2="${xe.toFixed(1)}" y2="${yc}" stroke="url(#${gid})" stroke-width="2.4" stroke-linecap="round"/>`;
    } else {
      const dash = r.active ? '' : '';
      s += `<line x1="${xs.toFixed(1)}" y1="${yc}" x2="${xe.toFixed(1)}" y2="${yc}" stroke="${col}" stroke-width="2.4" stroke-opacity="0.9" stroke-linecap="round"${dash}/>`;
      if(r.active) s += `<circle cx="${xe.toFixed(1)}" cy="${yc}" r="3.2" fill="#fff" stroke="${col}" stroke-width="1.5"/>`;
    }

    // markers — things you did sit ON the line; things they did (recruiter
    // contact, screens, offer, rejection, silence) float just above it,
    // connected back down by a short tick.
    r.events.forEach(e=>{
      const mc = eventColor(e.g, col);
      const ex = x(parse(e.date).getTime());
      const theirs = e.who === 'theirs';
      const ey = theirs ? (yc-7) : yc;
      if(theirs) s += `<line x1="${ex.toFixed(1)}" y1="${yc}" x2="${ex.toFixed(1)}" y2="${ey.toFixed(1)}" stroke="${mc}" stroke-width="0.75" stroke-opacity="0.4"/>`;
      s += `<g transform="translate(${ex.toFixed(1)},${ey.toFixed(1)})">${marker(e.g,mc)}</g>`;
    });

    // contact interactions: your outreach rides on the line same as any
    // other thing you did; their replies and meetings float above it.
    (r.touches||[]).forEach(e=>{
      const tx = x(parse(e.date).getTime());
      const gl = e.dir==='outbound' ? 'outreach' : (e.dir==='meeting' ? 'meeting' : 'response');
      const theirs = e.dir !== 'outbound';
      const ty = theirs ? (yc-7) : yc;
      if(theirs) s += `<line x1="${tx.toFixed(1)}" y1="${yc}" x2="${tx.toFixed(1)}" y2="${ty.toFixed(1)}" stroke="${C.contact}" stroke-width="0.75" stroke-opacity="0.4"/>`;
      s += `<g transform="translate(${tx.toFixed(1)},${ty.toFixed(1)})">${marker(gl,C.contact)}</g>`;
    });

    s += `</g>`;
  });

  s += defs + '</defs></svg>';
  wrap.innerHTML = s;
  attachTips(wrap);
}

function esc(t){return (t||'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}

const STLAB = {applied:'Applied',considering:'Considering',recruiter:'Recruiter contact',
  phone_screen:'Phone screen',rejected:'Rejected',ghosted:'Ghosted',withdrawn:'Withdrawn',
  declined_by_candidate:'Declined',discovered:'Discovered','re-applied':'Re-applied',update:'Update'};

const DIRLAB = {outbound:'you reached out', inbound:'contact replied', meeting:'meeting'};

function attachTips(wrap){
  const tip = document.getElementById('tl-tip');
  wrap.querySelectorAll('.rowhit').forEach(g=>{
    g.addEventListener('mousemove',ev=>{
      const r = VIEW[+g.dataset.i];
      if(!r) return;
      const items = [];
      r.events.forEach(e=>items.push([e.date, `${STLAB[e.stage]||e.stage}`, false]));
      (r.touches||[]).forEach(e=>items.push([e.date,
        `✉ ${esc(e.who)} — ${DIRLAB[e.dir]||e.dir}`, true]));
      items.sort((a,b)=>a[0]<b[0]?-1:a[0]>b[0]?1:0);
      const evs = items.map(([dt,lab,isc])=>
        `<span class="ev"${isc?' style="color:#c4b5fd"':''}>${dt} · ${lab}</span>`).join('<br>');
      let statusLine = r.ghost ? `ghosted (recognized ${r.ghost})`
                     : r.active ? `active · ${r.status}` : r.status;
      tip.innerHTML = `<b>${esc(r.co)}</b><br>${esc(r.role)}<br>`
        + `<span class="ev">${statusLine}</span><br><br>${evs}`;
      // anchor a corner at the cursor; expand into whichever side has room
      const GAP = 14, M = 8;
      const tw = tip.offsetWidth, th = tip.offsetHeight;
      const vw = window.innerWidth, vh = window.innerHeight;
      let left = ev.clientX + GAP;
      if(left + tw + M > vw) left = ev.clientX - GAP - tw;   // flip left
      if(left < M) left = M;
      let top = ev.clientY + GAP;
      if(top + th + M > vh) top = ev.clientY - GAP - th;     // flip up
      if(top < M) top = M;
      tip.style.left = left+'px'; tip.style.top = top+'px'; tip.style.opacity = 1;
    });
    g.addEventListener('mouseleave',()=>{tip.style.opacity=0;});
  });
}

function legend(){
  const el = document.getElementById('tl-legend');
  const item = ([g,label])=>{
    const c = eventColor(g, C.active);
    return `<span class="li"><svg width="14" height="14" viewBox="-7 -7 14 14">${marker(g,c)}</svg>${label}</span>`;
  };
  el.innerHTML =
    `<span class="li tl-legend-head">On the line — you:</span>` + LEGEND_MINE.map(item).join('') +
    `<span class="li tl-legend-head">Above the line — them:</span>` + LEGEND_THEIRS.map(item).join('');
}

function boot(){
  document.getElementById('tl-stamp').textContent = !window.TIMELINE_RAW
    ? '(no data — timeline-data.js must sit in the same folder)'
    : `(${TL.rows.length} applications` + (TL.generated ? ` · data from ${TL.generated.replace('T',' ')}` : '') + ')';
  legend();
  render();
}
const sel = document.getElementById('tl-filter');
if(sel){ FILTER = sel.value; sel.addEventListener('change',()=>{FILTER = sel.value; boot();}); }
let rt; window.addEventListener('resize',()=>{clearTimeout(rt);rt=setTimeout(boot,150);});
boot();
</script>
</body>
</html>
```
