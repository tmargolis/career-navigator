---
name: pipeline-dashboard
description: >
  Generates a self-contained interactive D3 pipeline dashboard as an HTML
  file and opens it in the browser. Shows application timeline, pipeline
  funnel with conversion rates, benchmark comparisons against industry
  norms, AI displacement outlook, transferable strengths, and ExperienceLibrary
  performance weights. Can be invoked standalone or as the final step of
  the analyst report.
triggers:
  - "show me my pipeline"
  - "open the dashboard"
  - "pipeline dashboard"
  - "visualize my search"
  - "show me a chart"
  - "generate the dashboard"
  - "pipeline visualization"
  - "show my pipeline visually"
---

Generate a self-contained HTML dashboard visualizing the user's job search pipeline and open it in their browser.

## Data files

| File | Purpose |
|---|---|
| `{user_dir}/CareerNavigator/tracker.json` | Applications, stage history, pipeline summary |
| `{user_dir}/CareerNavigator/ExperienceLibrary.json` | Experience units with performance weights and update log |
| `{user_dir}/CareerNavigator/artifacts-index.json` | Generated artifacts with ATS scores |
| `{user_dir}/CareerNavigator/analyst-graph-data.json` | Optional graph data from the analyst report |

---

## Workflow

### 1. Assemble the data object

Read all three files and build the following JSON object. This will be embedded directly into the HTML file.

```json
{
  "generated_at": "{YYYY-MM-DD HH:MM}",
  "confidence": "{Preliminary | Directional | Moderate | High}",
  "applications": [
    {
      "company": "{company}",
      "role": "{role — truncate to 40 chars if longer}",
      "date_applied": "{YYYY-MM-DD or null}",
      "status": "{status}",
      "last_stage_date": "{date of most recent stage_history entry}"
    }
  ],
  "benchmarks": [
    {
      "label": "App → Response",
      "user_value": {integer 0–100 or null if < 3 data points},
      "norm_low": {integer},
      "norm_high": {integer}
    },
    { "label": "Response → Screen",  "user_value": ..., "norm_low": ..., "norm_high": ... },
    { "label": "Screen → Interview", "user_value": ..., "norm_low": ..., "norm_high": ... },
    { "label": "Interview → Offer",  "user_value": ..., "norm_low": ..., "norm_high": ... }
  ],
  "experience_library_units": [
    {
      "label": "{title} — {company} ({dates})",
      "weight": {float 0.1–1.0},
      "update_note": "{most recent weight_update_log rationale, or null}"
    }
  ],
  "ai_displacement_outlook": {
    "overall_risk": "{label}",
    "exposure_min_pct": {number},
    "exposure_max_pct": {number},
    "durable_min_pct": {number},
    "durable_max_pct": {number},
    "durable_differentiators": ["..."],
    "narrative_reframe": "..."
  },
  "transferable_strengths": [
    {
      "name": "{strength name}",
      "rating": "{HIGH|VERY_HIGH|MODERATE_HIGH|...}",
      "score_0_100": {number},
      "evidence": "{short evidence snippet}",
      "destinations": ["..."]
    }
  ]
}
```

**Computing benchmark values:**
- Use the same method as analyst Operation 4 — calculate from `tracker.json` and compare against the norm tables for the user's level and company size mix
- If a metric has fewer than 3 resolved data points, set `user_value` to `null`
- Use the norm ranges from the analyst benchmark tables (Director level, enterprise/mid-market mix, Chicago/remote geography as appropriate for the user's profile)

**Confidence tier:** count applications where `outcome` != `"pending"` — use analyst Op 4 thresholds (0–4: Preliminary, 5–14: Directional, 15–29: Moderate, 30+: High)

**ExperienceLibrary units:** read `units[]` from `CareerNavigator/ExperienceLibrary.json`. For `update_note`, use the most recent entry from `weight_update_log` for that unit (match by `unit_id`), or `null` if none.

**AI displacement + strengths graphs:** optionally read `{user_dir}/CareerNavigator/analyst-graph-data.json`. If missing or invalid, set `ai_displacement_outlook` to `null` and `transferable_strengths` to `[]`.

---

### 2. Write the HTML file

Write the assembled dashboard to `{user_dir}/CareerNavigator/pipeline-dashboard.html` using the exact template below. Replace `/*DATA_PLACEHOLDER*/` with the serialized JSON object from Step 1.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Career Navigator — Pipeline Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#0f1117;color:#e1e4e8;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;padding:28px 32px}
    h1{font-size:17px;font-weight:600;color:#f0f6fc;margin-bottom:3px}
    .sub{font-size:12px;color:#8b949e;margin-bottom:32px}
    .grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}
    .panel{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:20px}
    .panel.wide{grid-column:1/-1}
    .panel h2{font-size:11px;font-weight:600;color:#8b949e;text-transform:uppercase;letter-spacing:.06em;margin-bottom:16px}
    .tip{position:fixed;background:#21262d;border:1px solid #30363d;border-radius:6px;padding:8px 12px;font-size:12px;pointer-events:none;opacity:0;transition:opacity .12s;color:#e1e4e8;z-index:100;max-width:260px;line-height:1.5}
    text{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
    .no-data{font-size:12px;color:#484f58;padding:8px 0}
  </style>
</head>
<body>
  <h1>Career Navigator — Pipeline Dashboard</h1>
  <div class="sub" id="sub"></div>
  <div class="tip" id="tip"></div>
  <div class="grid">
    <div class="panel wide"><h2>Application Timeline</h2><svg id="sv-timeline"></svg></div>
    <div class="panel"><h2>Pipeline Funnel</h2><svg id="sv-funnel"></svg></div>
    <div class="panel"><h2>vs. Industry Norms</h2><svg id="sv-bench"></svg></div>
    <div class="panel"><h2>AI Displacement Outlook</h2><svg id="sv-displacement"></svg></div>
    <div class="panel"><h2>Transferable Strengths</h2><svg id="sv-strengths"></svg></div>
    <div class="panel wide"><h2>ExperienceLibrary Performance Weights</h2><svg id="sv-experience-library"></svg></div>
  </div>
<script>
const D = /*DATA_PLACEHOLDER*/;

const SC = {
  considering:'#58a6ff',applied:'#3fb950',phone_screen:'#d2a8ff',
  interview:'#ffa657',offer:'#f78166',accepted:'#56d364',
  rejected:'#484f58',withdrew:'#484f58',ghosted:'#484f58'
};

document.getElementById('sub').textContent =
  `Generated ${D.generated_at}  ·  ${D.applications.length} application${D.applications.length!==1?'s':''}  ·  Confidence: ${D.confidence}`;

const tip = document.getElementById('tip');
function showTip(html, e){ tip.innerHTML=html; tip.style.opacity=1; moveTip(e); }
function moveTip(e){ tip.style.left=(e.clientX+14)+'px'; tip.style.top=(e.clientY-8)+'px'; }
function hideTip(){ tip.style.opacity=0; }

function truncate(s, n){
  s = (s ?? '').toString();
  if(s.length <= n) return s;
  return s.slice(0, Math.max(0, n-3)) + '...';
}

// ── TIMELINE ────────────────────────────────────────────────────────────────
(function(){
  const apps = D.applications
    .filter(a => a.date_applied)
    .map(a => ({...a, t0: new Date(a.date_applied), t1: a.last_stage_date ? new Date(a.last_stage_date) : new Date()}))
    .sort((a,b) => a.t0 - b.t0);

  if(!apps.length){ document.querySelector('#sv-timeline').closest('.panel').innerHTML+='<p class="no-data">No applications with dates yet.</p>'; return; }

  const ml=160, mr=24, mt=8, mb=28;
  const W = document.querySelector('#sv-timeline').closest('.panel').clientWidth - 40 - ml - mr;
  const rh = 26, H = apps.length * rh;

  const svg = d3.select('#sv-timeline')
    .attr('width', W+ml+mr).attr('height', H+mt+mb)
    .append('g').attr('transform',`translate(${ml},${mt})`);

  const now = new Date();
  const xMin = new Date(d3.min(apps,a=>a.t0) - 86400000*4);
  const xMax = new Date(Math.max(now, d3.max(apps,a=>a.t1)) + 86400000*4);
  const x = d3.scaleTime().domain([xMin, xMax]).range([0, W]);
  const y = d3.scaleBand().domain(apps.map(a=>a.company+' — '+a.role)).range([0,H]).padding(.3);

  svg.append('g').attr('transform',`translate(0,${H})`)
    .call(d3.axisBottom(x).ticks(6).tickFormat(d3.timeFormat('%b %d')))
    .selectAll('text').attr('fill','#8b949e').attr('font-size',10);
  svg.select('.domain').attr('stroke','#30363d');
  svg.selectAll('.tick line').attr('stroke','#30363d');

  svg.append('g').call(d3.axisLeft(y).tickSize(0))
    .selectAll('text')
    .attr('fill','#8b949e').attr('font-size',11).attr('dx',0)
    .style('text-anchor','start')
    .each(function(d){
      const full = d;
      d3.select(this).text(truncate(full, 34)).attr('title', full).style('cursor','help');
    });
  svg.select('.domain').remove();

  // today line
  svg.append('line')
    .attr('x1',x(now)).attr('x2',x(now)).attr('y1',0).attr('y2',H)
    .attr('stroke','#30363d').attr('stroke-dasharray','4,3').attr('stroke-width',1);
  svg.append('text').attr('x',x(now)+3).attr('y',H+14)
    .attr('fill','#484f58').attr('font-size',9).text('today');

  apps.forEach(a => {
    const key = a.company+' — '+a.role;
    const barW = Math.max(x(a.t1)-x(a.t0), 6);

    svg.append('rect')
      .attr('x',x(a.t0)).attr('y',y(key)).attr('width',barW).attr('height',y.bandwidth())
      .attr('fill',SC[a.status]||'#484f58').attr('opacity',.18).attr('rx',3);

    svg.append('circle')
      .attr('class','timeline-dot')
      .attr('data-status',a.status)
      .attr('cx',x(a.t0)).attr('cy',y(key)+y.bandwidth()/2).attr('r',5)
      .attr('fill',SC[a.status]||'#484f58').attr('stroke','none').attr('stroke-width',0)
      .attr('opacity',1).attr('cursor','pointer')
      .on('mouseover', e => showTip(`<strong>${a.company}</strong><br>${a.role}<br>Applied: ${a.date_applied}<br>Status: <span style="color:${SC[a.status]||'#8b949e'}">${a.status}</span>`,e))
      .on('mousemove', moveTip).on('mouseout', hideTip);
  });

  // legend (hover to highlight matching dots)
  const statuses = [...new Set(apps.map(a=>a.status))];
  const allDots = svg.selectAll('.timeline-dot');

  function resetDots(){
    allDots
      .attr('opacity',1)
      .attr('r',5)
      .attr('stroke','none')
      .attr('stroke-width',0);
  }

  function focusDots(s){
    allDots
      .attr('opacity',0.12)
      .attr('r',4)
      .attr('stroke','none')
      .attr('stroke-width',0);

    svg.selectAll(`.timeline-dot[data-status="${s}"]`)
      .attr('opacity',1)
      .attr('r',7)
      .attr('stroke','#e1e4e8')
      .attr('stroke-width',1.6);
  }

  const lg = svg.append('g').attr('transform',`translate(0,${H+mb-4})`);
  let lx = 0;
  statuses.forEach(s => {
    const g = lg.append('g').attr('transform',`translate(${lx},0)`).style('cursor','pointer');
    g.append('circle').attr('cx',4).attr('cy',0).attr('r',4).attr('fill',SC[s]||'#484f58');
    g.append('text').attr('x',12).attr('y',4).attr('fill','#8b949e').attr('font-size',10).text(s);
    g.on('mouseover', () => focusDots(s)).on('mouseout', resetDots);
    lx += 80;
  });

  resetDots();
})();

// ── FUNNEL ───────────────────────────────────────────────────────────────────
(function(){
  const stages = ['considering','applied','phone_screen','interview','offer','accepted'];
  const labels = ['Considering','Applied','Phone Screen','Interview','Offer','Accepted'];
  const all = D.applications || [];

  function stageOrder(status){
    switch(status){
      case 'considering': return 0;
      case 'applied': return 1;
      case 'phone_screen': return 2;
      case 'interview': return 3;
      case 'offer': return 4;
      case 'accepted': return 5;
      // Terminal outcomes we currently bucket as "after applied" in the funnel.
      // This prevents phone/interview/offer bars appearing when you only have rejections.
      case 'rejected':
      case 'withdrew':
      case 'ghosted':
      case 'declined_or_inactive':
        return 1;
      default:
        return 1;
    }
  }

  if(!all.length){
    document.querySelector('#sv-funnel').insertAdjacentHTML('afterend','<p class="no-data">No applications yet.</p>');
    return;
  }

  const buckets = stages.map((stage, i) => {
    const apps = all.filter(a => stageOrder(a.status) >= i);
    return { stage, label: labels[i], count: apps.length, apps };
  }).filter(b => b.count > 0);

  const ml=96, mr=40, mt=8, mb=8;
  const panelW = document.querySelector('#sv-funnel').closest('.panel').clientWidth - 40;
  const W = panelW - ml - mr;
  const rh = 34, H = buckets.length * rh;

  const svg = d3.select('#sv-funnel')
    .attr('width',panelW).attr('height',H+mt+mb)
    .append('g').attr('transform',`translate(${ml},${mt})`);

  const x = d3.scaleLinear().domain([0, Math.max(1, buckets[0].count)]).range([0, W]);
  const y = d3.scaleBand().domain(buckets.map(b => b.label)).range([0,H]).padding(.28);

  svg.append('g').call(d3.axisLeft(y).tickSize(0))
    .selectAll('text').attr('fill','#8b949e').attr('font-size',11).attr('dx',0).style('text-anchor','start');
  svg.select('.domain').remove();

  buckets.forEach((b, i) => {
    const yPos = y(b.label);
    const w = Math.max(x(b.count), 4);

    svg.append('rect')
      .attr('x',0).attr('y',yPos).attr('width',w).attr('height',y.bandwidth())
      .attr('fill',SC[b.stage]||'#484f58').attr('rx',3).attr('opacity',.82)
      .on('mouseover', e => {
        const apps = b.apps || [];
        const shown = apps.slice(0,6).map(a => `• ${a.company} — ${a.role} (${a.status})`).join('<br>');
        const more = apps.length > 6 ? `<br>+${apps.length-6} more` : '';
        const html = `<strong>${b.label}</strong><br>${b.count} application${b.count!==1?'s':''}<br>${shown || '—'}${more}`;
        showTip(html, e);
      })
      .on('mousemove', moveTip)
      .on('mouseout', hideTip);

    svg.append('text')
      .attr('x',w+6).attr('y',yPos+y.bandwidth()/2+4)
      .attr('fill','#8b949e').attr('font-size',11).text(b.count);

    if(i > 0 && buckets[i-1].count > 0){
      const rate = Math.round(b.count / buckets[i-1].count * 100);
      svg.append('text')
        .attr('x',W).attr('y',yPos-3)
        .attr('text-anchor','end').attr('fill','#484f58').attr('font-size',9)
        .text(`${rate}% conversion`);
    }
  });
})();

// ── BENCHMARKS ───────────────────────────────────────────────────────────────
(function(){
  const metrics = D.benchmarks;
  if(!metrics||!metrics.length){
    document.querySelector('#sv-bench').insertAdjacentHTML('afterend','<p class="no-data">Run /pattern-analysis to generate benchmark data.</p>');
    return;
  }

  const ml=130, mr=50, mt=10, mb=28;
  const panelW = document.querySelector('#sv-bench').closest('.panel').clientWidth - 40;
  const W = panelW - ml - mr;
  const rh = 38, H = metrics.length * rh;

  const svg = d3.select('#sv-bench')
    .attr('width',panelW).attr('height',H+mt+mb)
    .append('g').attr('transform',`translate(${ml},${mt})`);

  const x = d3.scaleLinear().domain([0,100]).range([0,W]);
  const y = d3.scaleBand().domain(metrics.map(m=>m.label)).range([0,H]).padding(.35);

  svg.append('g').attr('transform',`translate(0,${H})`)
    .call(d3.axisBottom(x).ticks(5).tickFormat(d=>d+'%'))
    .selectAll('text').attr('fill','#8b949e').attr('font-size',10);
  svg.select('.domain').attr('stroke','#30363d');
  svg.selectAll('.tick line').attr('stroke','#30363d');

  svg.append('g').call(d3.axisLeft(y).tickSize(0))
    .selectAll('text')
    .attr('fill','#8b949e').attr('font-size',11).attr('dx',0)
    .style('text-anchor','start')
    .each(function(d){
      const full = d;
      d3.select(this).text(truncate(full, 40)).attr('title', full).style('cursor','help');
    });
  svg.select('.domain').remove();

  metrics.forEach(m => {
    // norm band
    svg.append('rect')
      .attr('x',x(m.norm_low)).attr('y',y(m.label))
      .attr('width',x(m.norm_high)-x(m.norm_low)).attr('height',y.bandwidth())
      .attr('fill','#21262d').attr('stroke','#30363d').attr('stroke-width',1).attr('rx',2);

    svg.append('text')
      .attr('x',x(m.norm_low)).attr('y',y(m.label)-3)
      .attr('fill','#484f58').attr('font-size',9)
      .text(`norm ${m.norm_low}–${m.norm_high}%`);

    if(m.user_value !== null){
      const above = m.user_value >= m.norm_low;
      svg.append('rect')
        .attr('x',0).attr('y',y(m.label)+y.bandwidth()*.15)
        .attr('width',Math.max(x(m.user_value),3)).attr('height',y.bandwidth()*.7)
        .attr('fill',above?'#3fb950':'#f78166').attr('rx',2).attr('opacity',.88)
        .on('mouseover', e => showTip(`<strong>${m.label}</strong><br>Your rate: ${m.user_value}%<br>Norm: ${m.norm_low}–${m.norm_high}%<br>${above?'▲ Above norm':'▼ Below norm'}`,e))
        .on('mousemove',moveTip).on('mouseout',hideTip);

      svg.append('text')
        .attr('x',Math.max(x(m.user_value),3)+5).attr('y',y(m.label)+y.bandwidth()/2+4)
        .attr('fill','#e1e4e8').attr('font-size',11).text(m.user_value+'%');
    } else {
      svg.append('text')
        .attr('x',4).attr('y',y(m.label)+y.bandwidth()/2+4)
        .attr('fill','#484f58').attr('font-size',11).text('— insufficient data');
    }
  });
})();

// ── AI DISPLACEMENT OUTLOOK ──────────────────────────────────────────────
(function(){
  const data = D.ai_displacement_outlook;
  if(!data){
    document.querySelector('#sv-displacement').insertAdjacentHTML('afterend','<p class="no-data">Run /career-navigator:report to generate AI displacement data.</p>');
    return;
  }

  const panelW = document.querySelector('#sv-displacement').closest('.panel').clientWidth - 40;
  const ml=26, mr=24, mt=10, mb=22;
  const W = panelW - ml - mr;
  const H = 118;

  const exposureMin = (data.exposure_min_pct ?? null);
  const exposureMax = (data.exposure_max_pct ?? null);
  const valid = exposureMin !== null && exposureMax !== null && isFinite(exposureMin) && isFinite(exposureMax);
  if(!valid){
    document.querySelector('#sv-displacement').insertAdjacentHTML('afterend','<p class="no-data">AI displacement graph data is missing.</p>');
    return;
  }

  const x = d3.scaleLinear().domain([0,100]).range([0,W]);
  const yBar = 48;

  const svg = d3.select('#sv-displacement')
    .attr('width',panelW).attr('height',H+mt+mb)
    .append('g').attr('transform',`translate(${ml},${mt})`);

  svg.append('text')
    .attr('x',0).attr('y',18).attr('fill','#e1e4e8').attr('font-size',11)
    .text(`Overall risk: ${data.overall_risk || '—'}`);

  svg.append('rect')
    .attr('x',0).attr('y',yBar).attr('width',W).attr('height',16)
    .attr('fill','#21262d').attr('rx',6);

  const minX = x(Math.max(0, exposureMin));
  const maxX = x(Math.min(100, exposureMax));
  const w = Math.max(maxX - minX, 3);

  // Exposed tasks range
  svg.append('rect')
    .attr('x',minX).attr('y',yBar).attr('width',w).attr('height',16)
    .attr('fill','#d2a8ff').attr('opacity',0.9).attr('rx',6);

  svg.append('line').attr('x1',minX).attr('x2',minX).attr('y1',yBar-2).attr('y2',yBar+18).attr('stroke','#8b949e').attr('stroke-width',1);
  svg.append('line').attr('x1',maxX).attr('x2',maxX).attr('y1',yBar-2).attr('y2',yBar+18).attr('stroke','#8b949e').attr('stroke-width',1);

  const durableMin = data.durable_min_pct ?? (100 - exposureMax);
  const durableMax = data.durable_max_pct ?? (100 - exposureMin);

  svg.append('text')
    .attr('x',0).attr('y',yBar+34).attr('fill','#8b949e').attr('font-size',11)
    .text(`Exposed: ${Math.round(exposureMin)}–${Math.round(exposureMax)}%  ·  Durable: ${Math.round(durableMin)}–${Math.round(durableMax)}%`);
})();

// ── TRANSFERABLE STRENGTHS ───────────────────────────────────────────────
(function(){
  const raw = D.transferable_strengths || [];
  if(!raw.length){
    document.querySelector('#sv-strengths').insertAdjacentHTML('afterend','<p class="no-data">Run /career-navigator:report to generate transferable strengths data.</p>');
    return;
  }

  const items = raw.slice(0,6);
  const panelW = document.querySelector('#sv-strengths').closest('.panel').clientWidth - 40;
  const ml=155, mr=30, mt=10, mb=20;
  const W = panelW - ml - mr;
  const rh = 30, H = items.length * rh;

  const svg = d3.select('#sv-strengths')
    .attr('width',panelW).attr('height',H+mt+mb)
    .append('g').attr('transform',`translate(${ml},${mt})`);

  const x = d3.scaleLinear().domain([0,100]).range([0,W]);
  const y = d3.scaleBand().domain(items.map(i=>i.name)).range([0,H]).padding(.25);

  svg.append('g').call(d3.axisLeft(y).tickSize(0))
    .selectAll('text')
    .attr('fill','#8b949e').attr('font-size',11).attr('dx',0)
    .style('text-anchor','start')
    .each(function(d){
      const full = d;
      d3.select(this).text(truncate(full, 26)).attr('title', full).style('cursor','help');
    });
  svg.select('.domain').remove();

  const color = d3.scaleSequential(d3.interpolateRgb('#2d333b','#58a6ff')).domain([0,100]);

  items.forEach(it => {
    const score = Math.max(0, Math.min(100, Number(it.score_0_100 ?? 0)));
    const yPos = y(it.name);
    const w = Math.max(x(score), 3);

    svg.append('rect')
      .attr('x',0).attr('y',yPos).attr('width',w).attr('height',y.bandwidth())
      .attr('fill',color(score)).attr('rx',4).attr('opacity',0.9)
      .attr('cursor','pointer')
      .on('mouseover', e => {
        const dest = (it.destinations || []).slice(0,3).join(', ');
        const evidence = it.evidence ? `<br>${it.evidence}` : '';
        const html = `<strong>${it.name}</strong><br>Rating: ${it.rating || '—'}<br>Score: ${score}/100${dest ? `<br>Destinations: ${dest}` : ''}${evidence}`;
        showTip(html, e);
      })
      .on('mousemove', moveTip)
      .on('mouseout', hideTip);

    svg.append('text')
      .attr('x',w+6).attr('y',yPos+y.bandwidth()/2+4)
      .attr('fill','#e1e4e8').attr('font-size',11)
      .text(score.toFixed(0));
  });
})();

// ── CORPUS WEIGHTS ────────────────────────────────────────────────────────────
(function(){
  const units = D.experience_library_units;
  if(!units||!units.length){ return; }

  const ml=260, mr=60, mt=8, mb=20;
  const panelW = document.querySelector('#sv-experience-library').closest('.panel').clientWidth - 40;
  const W = panelW - ml - mr;
  const rh = 28, H = units.length * rh;

  const svg = d3.select('#sv-experience-library')
    .attr('width',panelW).attr('height',H+mt+mb)
    .append('g').attr('transform',`translate(${ml},${mt})`);

  const x = d3.scaleLinear().domain([0,1]).range([0,W]);
  const y = d3.scaleBand().domain(units.map(u=>u.label)).range([0,H]).padding(.3);

  svg.append('g').attr('transform',`translate(0,${H})`)
    .call(d3.axisBottom(x).ticks(5).tickFormat(d=>d.toFixed(1)))
    .selectAll('text').attr('fill','#8b949e').attr('font-size',10);
  svg.select('.domain').attr('stroke','#30363d');
  svg.selectAll('.tick line').attr('stroke','#30363d');

  svg.append('g').call(d3.axisLeft(y).tickSize(0))
    .selectAll('text')
    .attr('fill','#8b949e').attr('font-size',11).attr('dx',0)
    .style('text-anchor','start')
    .each(function(d){
      const full = d;
      d3.select(this).text(truncate(full, 40)).attr('title', full).style('cursor','help');
    });
  svg.select('.domain').remove();

  // neutral line at 0.5
  svg.append('line')
    .attr('x1',x(.5)).attr('x2',x(.5)).attr('y1',0).attr('y2',H)
    .attr('stroke','#30363d').attr('stroke-dasharray','4,3').attr('stroke-width',1);
  svg.append('text').attr('x',x(.5)+3).attr('y',-2)
    .attr('fill','#484f58').attr('font-size',9).text('neutral');

  const color = d3.scaleSequential(d3.interpolateRgb('#2d333b','#58a6ff')).domain([0.1,1]);

  units.forEach(u => {
    svg.append('rect')
      .attr('x',0).attr('y',y(u.label))
      .attr('width',Math.max(x(u.weight),3)).attr('height',y.bandwidth())
      .attr('fill',color(u.weight)).attr('rx',3).attr('cursor','pointer')
      .on('mouseover', e => showTip(`<strong>${u.label}</strong><br>Weight: ${u.weight.toFixed(2)}<br>${u.update_note||'No weight updates yet'}`,e))
      .on('mousemove',moveTip).on('mouseout',hideTip);

    svg.append('text')
      .attr('x',Math.max(x(u.weight),3)+5).attr('y',y(u.label)+y.bandwidth()/2+4)
      .attr('fill','#8b949e').attr('font-size',11).text(u.weight.toFixed(2));
  });
})();
</script>
</body>
</html>
```

---

### 3. Open in browser

After writing the file, open it in the user's default browser:

```bash
python3 -c "import webbrowser, os; webbrowser.open('file://' + os.path.abspath('{user_dir}/CareerNavigator/pipeline-dashboard.html'))"
```

### 4. Confirm

```
Dashboard generated → {user_dir}/CareerNavigator/pipeline-dashboard.html
Opening in browser.
```

If the file already exists, overwrite it — this is always a fresh snapshot of the current state.
