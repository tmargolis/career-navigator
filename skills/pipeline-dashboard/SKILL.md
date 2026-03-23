---
name: pipeline-dashboard
description: >
  Generates a self-contained interactive D3 pipeline dashboard as an HTML
  file and opens it in the browser. Shows application timeline, pipeline
  funnel with conversion rates, benchmark comparisons against industry
  norms, and corpus performance weights. Can be invoked standalone or as
  the final step of the analyst report.
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
| `{user_dir}/tracker/tracker.json` | Applications, stage history, pipeline summary |
| `{user_dir}/corpus/index.json` | Experience units with performance weights and update log |
| `{user_dir}/artifacts-index.json` | Generated artifacts with ATS scores |

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
  "corpus_units": [
    {
      "label": "{title} — {company} ({dates})",
      "weight": {float 0.1–1.0},
      "update_note": "{most recent weight_update_log rationale, or null}"
    }
  ]
}
```

**Computing benchmark values:**
- Use the same method as analyst Operation 4 — calculate from `tracker.json` and compare against the norm tables for the user's level and company size mix
- If a metric has fewer than 3 resolved data points, set `user_value` to `null`
- Use the norm ranges from the analyst benchmark tables (Director level, enterprise/mid-market mix, Chicago/remote geography as appropriate for the user's profile)

**Confidence tier:** count applications where `outcome` != `"pending"` — use analyst Op 4 thresholds (0–4: Preliminary, 5–14: Directional, 15–29: Moderate, 30+: High)

**Corpus units:** read `units[]` from `corpus/index.json`. For `update_note`, use the most recent entry from `weight_update_log` for that unit (match by `unit_id`), or `null` if none.

---

### 2. Write the HTML file

Write the assembled dashboard to `{user_dir}/pipeline-dashboard.html` using the exact template below. Replace `/*DATA_PLACEHOLDER*/` with the serialized JSON object from Step 1.

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
    <div class="panel wide"><h2>Corpus Performance Weights</h2><svg id="sv-corpus"></svg></div>
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
    .selectAll('text').attr('fill','#8b949e').attr('font-size',11).attr('dx',-6);
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
      .attr('cx',x(a.t0)).attr('cy',y(key)+y.bandwidth()/2).attr('r',5)
      .attr('fill',SC[a.status]||'#484f58').attr('cursor','pointer')
      .on('mouseover', e => showTip(`<strong>${a.company}</strong><br>${a.role}<br>Applied: ${a.date_applied}<br>Status: <span style="color:${SC[a.status]||'#8b949e'}">${a.status}</span>`,e))
      .on('mousemove', moveTip).on('mouseout', hideTip);
  });

  // legend
  const statuses = [...new Set(apps.map(a=>a.status))];
  const lg = svg.append('g').attr('transform',`translate(0,${H+mb-4})`);
  let lx = 0;
  statuses.forEach(s => {
    lg.append('circle').attr('cx',lx+4).attr('cy',0).attr('r',4).attr('fill',SC[s]||'#484f58');
    lg.append('text').attr('x',lx+12).attr('y',4).attr('fill','#8b949e').attr('font-size',10).text(s);
    lx += 80;
  });
})();

// ── FUNNEL ───────────────────────────────────────────────────────────────────
(function(){
  const stages = ['considering','applied','phone_screen','interview','offer','accepted'];
  const labels = ['Considering','Applied','Phone Screen','Interview','Offer','Accepted'];
  const all = D.applications;

  const stageOrder = s => stages.indexOf(s) === -1 ? stages.length : stages.indexOf(s);
  const counts = stages.map(s => all.filter(a => stageOrder(a.status) >= stages.indexOf(s)).length);

  const ml=96, mr=40, mt=8, mb=8;
  const panelW = document.querySelector('#sv-funnel').closest('.panel').clientWidth - 40;
  const W = panelW - ml - mr;
  const rh = 34, H = stages.length * rh;

  const svg = d3.select('#sv-funnel')
    .attr('width',panelW).attr('height',H+mt+mb)
    .append('g').attr('transform',`translate(${ml},${mt})`);

  const x = d3.scaleLinear().domain([0, Math.max(1, counts[0])]).range([0, W]);
  const y = d3.scaleBand().domain(labels).range([0,H]).padding(.28);

  svg.append('g').call(d3.axisLeft(y).tickSize(0))
    .selectAll('text').attr('fill','#8b949e').attr('font-size',11).attr('dx',-6);
  svg.select('.domain').remove();

  labels.forEach((label, i) => {
    svg.append('rect')
      .attr('x',0).attr('y',y(label)).attr('width',Math.max(x(counts[i]),4)).attr('height',y.bandwidth())
      .attr('fill',SC[stages[i]]||'#484f58').attr('rx',3).attr('opacity',.82);

    svg.append('text')
      .attr('x',Math.max(x(counts[i]),4)+6).attr('y',y(label)+y.bandwidth()/2+4)
      .attr('fill','#8b949e').attr('font-size',11).text(counts[i]);

    if(i > 0 && counts[i-1] > 0){
      const rate = Math.round(counts[i]/counts[i-1]*100);
      svg.append('text')
        .attr('x',W).attr('y',y(label)-3)
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
    .selectAll('text').attr('fill','#8b949e').attr('font-size',11).attr('dx',-6);
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

// ── CORPUS WEIGHTS ────────────────────────────────────────────────────────────
(function(){
  const units = D.corpus_units;
  if(!units||!units.length){ return; }

  const ml=260, mr=60, mt=8, mb=20;
  const panelW = document.querySelector('#sv-corpus').closest('.panel').clientWidth - 40;
  const W = panelW - ml - mr;
  const rh = 28, H = units.length * rh;

  const svg = d3.select('#sv-corpus')
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
    .selectAll('text').attr('fill','#8b949e').attr('font-size',11).attr('dx',-6);
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
python3 -c "import webbrowser, os; webbrowser.open('file://' + os.path.abspath('{user_dir}/pipeline-dashboard.html'))"
```

### 4. Confirm

```
Dashboard generated → {user_dir}/pipeline-dashboard.html
Opening in browser.
```

If the file already exists, overwrite it — this is always a fresh snapshot of the current state.
