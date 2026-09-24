---
name: pipeline-status
description: >
  Generates the Career Navigator pipeline status page: a filterable,
  collapsible table of every active application, focus/recommended role,
  closed outcome, and passed-on role, with an embedded application timeline.
  Writes {user_dir}/CareerNavigator/pipeline-status.html (plus pipeline-data.js
  and timeline.html) and opens it in the browser. Reads tracker.json,
  recommendations.json, and passed.json — always a fresh snapshot on request,
  and can be scheduled to refresh nightly via /career-navigator:setup-schedule.
  Also invocable via /career-navigator:pipeline-status.
triggers:
  - "show my pipeline status"
  - "generate pipeline status page"
  - "refresh pipeline dashboard"
  - "show me my pipeline"
  - "open the pipeline status page"
  - "pipeline status"
  - "regenerate pipeline status"
  - "/career-navigator:pipeline-status"
  - "/pipeline-status"
---

Generate the pipeline status page — a static, self-contained HTML dashboard covering the user's full job search pipeline — and open it in their browser.

---

## 1. Verify Career Navigator setup

Application data uses the split layout defined in [references/tracker-schema.md](../../references/tracker-schema.md) — read it before any read or write.

Read `{user_dir}/CareerNavigator/tracker.json`, `{user_dir}/CareerNavigator/recommendations.json`, and `{user_dir}/CareerNavigator/passed.json`. All three are core files created by `/career-navigator:launch`.

If any is missing, output:
> Pipeline status not set up: run `/career-navigator:launch` first to initialize Career Navigator.

Then stop.

---

## 2. Read and normalize the data

- **`tracker.json`** — summary rows only. For each row with `stage_count` > 0, load its `detail_file` under `applications/` for `stage_history[]` (needed for the closed-section duration calc). Rows with `stage_count: 0` need no extra read.
- **`recommendations.json`** — pre-application roles, `status: "considering"` (or `"recommended"` if `priority` is `"high"` — normalize this the same way as the historical generator: if a `considering`/`recommended` record's status doesn't match its priority tier, correct it in place and write the file back).
- **`passed.json`** — roles explicitly passed on (`status: "pass"`).

Slim each record down to what the page renders — do not embed full stage history, notes, or contacts:

- **Applications**: `company`, `role`, `status`, `job_link`, `priority`, `date_applied`, `follow_up_date`, `location`, `next_step`, and `stage_history` reduced to `[{date}, ...]` (dates only, for duration math).
- **Recommendations / passed**: `company`, `role`, `status`, `job_link`, `priority`, `date_added` (fall back through `date_discovered` → `added_date` → first note date → first stage_history date, in that order, using whichever is present first), `date_researched`, `location`, `next_step`, and the same slimmed `stage_history`.

---

## 3. Write `pipeline-data.js`

Write `{user_dir}/CareerNavigator/pipeline-data.js` as a plain JS file (not JSON) with four global assignments, using today's date:

```js
// Career Navigator pipeline data — generated {YYYY-MM-DD}
var TRACKER_DATA = {"applications": [...slimmed applications...]};
var RECS_DATA = {"recommendations": [...slimmed recommendations...]};
var PASSED_DATA = {"passed": [...slimmed passed...]};
var PIPELINE_GENERATED = "{YYYY-MM-DD}";
```

Always overwrite — this is a fresh snapshot every time.

---

## 4. Write `pipeline-status.html`

Write `{user_dir}/CareerNavigator/pipeline-status.html` using the template below. Replace `{{USER_NAME}}` with the user's name from `profile.md` (fall back to `"Your"` if not found). The page loads its data from the co-located `pipeline-data.js` via `<script src="pipeline-data.js">` and embeds `timeline.html` in an iframe — both must exist in the same directory.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Job Search — Pipeline Status</title>
<script src="pipeline-data.js"></script>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #fff; color: #1a1a1a; padding: 20px 20px 48px; font-size: 13px; }
h1 { font-size: 16px; font-weight: 500; margin-bottom: 3px; }
.meta { font-size: 11px; color: #999; margin-bottom: 14px; }
.page-head { display: flex; align-items: baseline; gap: 10px; margin-bottom: 14px; flex-wrap: wrap; }
.page-head h1 { margin-bottom: 0; }
.page-head .meta { margin-bottom: 0; }
.stamp { color: #10b981; font-weight: 500; }
.summary { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px; margin-top: 5px; }
.chip { font-size: 11px; padding: 3px 10px; border-radius: 20px; font-weight: 500; }
.chip-active { background: #d1fae5; color: #065f46; }
.chip-focus  { background: #ede9fe; color: #5b21b6; }
.chip-closed { background: #f3f4f6; color: #4b5563; }
.chip-passed { background: #f9fafb; color: #9ca3af; }
.controls { display: flex; gap: 10px; margin-bottom: 12px; align-items: center; flex-wrap: wrap; }
.controls label { font-size: 11px; color: #666; }
select { font-size: 11px; padding: 3px 8px; border: 0.5px solid #d1d5db; border-radius: 6px; background: #fff; color: #1a1a1a; cursor: pointer; }
table { width: 100%; border-collapse: collapse; font-size: 12px; }
col.col-co     { width: 15%; }
col.col-role   { width: 34%; }
col.col-stars  { width: 10%; }
col.col-status { width: 12%; }
col.col-date   { width: 10%; }
col.col-loc    { width: 19%; }
thead th { font-size: 10px; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; padding: 7px 8px; border-bottom: 1px solid #e5e7eb; background: #fafafa; text-align: left; position: sticky; top: 0; z-index: 2; white-space: nowrap; }
thead th.center { text-align: center; }
tbody tr.section-hdr td { background: #f3f4f6; font-size: 10px; font-weight: 600; color: #6b7280; letter-spacing: 0.06em; text-transform: uppercase; padding: 5px 8px; border-top: 1px solid #e5e7eb; cursor: pointer; user-select: none; }
tbody tr.section-hdr:hover td { background: #eceef1; }
.caret { display: inline-block; width: 10px; margin-right: 3px; color: #9ca3af; font-size: 9px; transition: transform 0.12s ease; }
tbody tr.section-hdr.collapsed .caret { transform: rotate(-90deg); }
tbody tr.data-row.sec-collapsed { display: none; }
tbody tr.data-row { border-bottom: 0.5px solid #f0f0f0; }
tbody tr.data-row:hover { background: #f9fafb; }
tbody tr.hidden { display: none; }
td { padding: 6px 8px; vertical-align: middle; }
td.center { text-align: center; }
a.co { font-weight: 500; color: #1a1a1a; text-decoration: none; border-bottom: 1px solid transparent; }
a.co:hover { border-bottom-color: #6b7280; }
a.role-link { color: #374151; text-decoration: none; border-bottom: 1px dotted #d1d5db; }
a.role-link:hover { color: #1a1a1a; border-bottom-color: #6b7280; }
.role-plain { color: #374151; }
.role-bold { font-weight: 600; color: #374151; }
.badge { display: inline-block; padding: 2px 7px; border-radius: 4px; font-size: 10px; font-weight: 600; white-space: nowrap; }
.b-applied   { background: #dbeafe; color: #1e40af; }
.b-screen    { background: #d1fae5; color: #065f46; }
.b-interview { background: #d1fae5; color: #065f46; }
.b-offer     { background: #dcfce7; color: #15803d; }
.b-ghosted   { background: #fef3c7; color: #92400e; }
.b-rejected  { background: #fee2e2; color: #991b1b; }
.b-withdrawn, .b-declined, .b-expired { background: #f3f4f6; color: #4b5563; }
.b-considering { background: #fef9c3; color: #854d0e; }
.b-rec       { background: #ede9fe; color: #5b21b6; }
.b-pass      { background: #f3f4f6; color: #9ca3af; text-decoration: line-through; }
.b-referred  { background: #e0e7ff; color: #3730a3; }
.b-exec      { background: #bbf7d0; color: #166534; }
.stars { font-size: 11px; white-space: nowrap; }
.loc-text  { font-size: 11px; color: #6b7280; }
.date-val  { font-size: 11px; color: #374151; white-space: nowrap; }
.date-dur  { font-size: 11px; color: #9ca3af; white-space: nowrap; }
.date-disc { font-size: 11px; color: #7c3aed; white-space: nowrap; }
span.dash  { color: #d1d5db; }
.no-data   { padding: 32px 8px; color: #9ca3af; font-size: 12px; }
.badge[data-next] { cursor: help; }
#status-tip { position: fixed; z-index: 50; max-width: 300px; background: #1a1a1a; color: #f9fafb; font-size: 11px; line-height: 1.45; padding: 8px 10px; border-radius: 6px; box-shadow: 0 6px 18px rgba(0,0,0,0.22); pointer-events: none; display: none; }
.tl-embed { width: 100%; border: 0.5px solid #e5e7eb; border-radius: 8px; margin-bottom: 1px; overflow: hidden; }
iframe#tl-frame { display: block; width: 100%; height: 450px; border: 0; }
</style>
</head>
<body>
<div id="status-tip"></div>
<div class="page-head">
  <h1>Job Search — Pipeline Status</h1>
  <p class="meta">{{USER_NAME}} &nbsp;·&nbsp; <span class="stamp" id="gen-stamp">Loading…</span></p>
</div>
<div class="tl-embed">
  <iframe id="tl-frame" src="timeline.html" title="Application pipeline timeline" scrolling="no" loading="lazy"></iframe>
</div>
<div class="summary">
  <span class="chip chip-active" id="chip-active">— active</span>
  <span class="chip chip-focus"  id="chip-focus">— focus</span>
  <span class="chip chip-closed" id="chip-closed">— closed</span>
  <span class="chip chip-passed" id="chip-passed">— passed</span>
</div>
<div class="controls">
  <label>Filter:</label>
  <select id="f-status" onchange="applyFilter()">
    <option value="all">All rows</option>
    <option value="active">Active only</option>
    <option value="focus">Focus / Recommended</option>
    <option value="action">Needs action</option>
    <option value="closed">Closed</option>
    <option value="passed">Passed</option>
  </select>
  <label style="margin-left:6px">Min rating:</label>
  <select id="f-stars" onchange="applyFilter()">
    <option value="0">Any</option>
    <option value="3">3+</option>
    <option value="4">4+</option>
    <option value="5">5 only</option>
  </select>
</div>
<script>
(function(){
  var f=document.getElementById('tl-frame');
  function fit(){try{var d=f.contentDocument||f.contentWindow.document;var h=Math.max(d.body.scrollHeight,d.documentElement.scrollHeight);if(h)f.style.height=(h+8)+'px';}catch(e){}}
  f.addEventListener('load',function(){fit();setTimeout(fit,150);setTimeout(fit,600);});
})();
</script>
<table>
<colgroup>
  <col class="col-co"><col class="col-role"><col class="col-stars">
  <col class="col-status"><col class="col-date"><col class="col-loc">
</colgroup>
<thead><tr>
  <th>Company</th>
  <th>Role</th>
  <th class="center" title="Priority rating">Rating</th>
  <th>Status</th>
  <th>Date</th>
  <th>Location</th>
</tr></thead>
<tbody id="tbody"></tbody>
</table>
<script>
var MONTHS=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
function fmtDate(s){if(!s)return null;try{var p=s.split('-');return MONTHS[+p[1]-1]+' '+ +p[2];}catch(e){return s;}}
function daysBetween(a,b){if(!a||!b)return null;try{var d=Math.round((new Date(b+'T00:00:00')-new Date(a+'T00:00:00'))/86400000);return d>=0?d:null;}catch(e){return null;}}
function durationLabel(d){if(d===null)return null;if(d===0)return '<1d';if(d<14)return d+'d';var w=Math.round(d/7);if(w<9)return w+'w';return Math.round(d/30.4)+'mo';}
function parsePriority(p){if(!p&&p!==0)return 0;if(typeof p==='number')return Math.min(5,Math.max(0,Math.round(p)));var s=String(p).toLowerCase();if(s==='critical')return 5;if(s==='high')return 4;if(s==='medium'||s==='normal')return 3;if(s==='low')return 2;return 0;}
function isOverdue(d){if(!d)return false;try{var dt=new Date(d+'T00:00:00'),t=new Date();t.setHours(0,0,0,0);return dt<=t;}catch(e){return false;}}
function getBaseUrl(u){if(!u||u==='#')return null;try{return new URL(u).origin;}catch(e){return null;}}
function stars(n){if(!n)return '<span class="dash">–</span>';var s='';for(var i=1;i<=5;i++)s+='<span style="color:'+(i<=n?'#f59e0b':'#e5e7eb')+'">&#9733;</span>';return '<span class="stars">'+s+'</span>';}
var BL={applied:'Applied',referred:'Referred',phone_screen:'Phone screen',screen:'Phone screen',interview:'Interview',executive_round_scheduled:'Exec round scheduled',executive_round_complete:'Exec round done',offer:'Offer',accepted:'Accepted',ghosted:'Ghosted',rejected:'Rejected',withdrawn:'Withdrawn',declined_by_candidate:'Declined',expired:'Expired',considering:'Considering',recommended:'Recommended',pending_decision:'Recommended',pass:'Pass'};
var BC={applied:'b-applied',referred:'b-referred',phone_screen:'b-screen',screen:'b-screen',interview:'b-interview',executive_round_scheduled:'b-exec',executive_round_complete:'b-exec',offer:'b-offer',accepted:'b-screen',ghosted:'b-ghosted',rejected:'b-rejected',withdrawn:'b-withdrawn',declined_by_candidate:'b-declined',expired:'b-expired',considering:'b-considering',recommended:'b-rec',pending_decision:'b-rec',pass:'b-pass'};
function badge(s,next){var attr=next?' data-next="'+esc(next)+'"':'';return '<span class="badge '+(BC[s]||'b-applied')+'"'+attr+'>'+(BL[s]||s)+'</span>';}
var ACTIVE_S=['applied','referred','phone_screen','screen','interview','executive_round_scheduled','executive_round_complete','offer','accepted'];
var CLOSED_S=['ghosted','rejected','declined_by_candidate'];
var PASSED_S=['withdrawn','expired','pass'];
function getSection(s){if(PASSED_S.indexOf(s)!==-1)return 'passed';if(CLOSED_S.indexOf(s)!==-1)return 'closed';if(ACTIVE_S.indexOf(s)!==-1)return 'active';return 'focus';}
function esc(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
var SL={active:'Active Applications',focus:'Focus — Recommended & Considering',closed:'Closed',passed:'Passed'};
var COLLAPSED={active:false,focus:true,closed:true,passed:true};
var ROWS=[];

function buildRows(){
  var rows=[];
  var apps=(typeof TRACKER_DATA!=='undefined'&&TRACKER_DATA.applications)||[];
  var recs=(typeof RECS_DATA!=='undefined'&&RECS_DATA.recommendations)||[];
  apps.forEach(function(app){
    var status=app.status||'applied',sec=getSection(status);
    var sh=app.stage_history||[];
    var start=app.date_applied||(sh[0]&&sh[0].date)||'';
    var sortDate,dateCell;
    if(sec==='closed'){
      var end=(sh[sh.length-1]&&sh[sh.length-1].date)||start;
      sortDate=end;
      var dur=durationLabel(daysBetween(start,end));
      dateCell=dur?'<span class="date-dur">'+esc(dur)+'</span>':'<span class="dash">–</span>';
    }else{
      sortDate=start;
      var fd=fmtDate(start);
      dateCell=fd?'<span class="date-val">'+esc(fd)+'</span>':'<span class="dash">–</span>';
    }
    rows.push({company:app.company||'—',cUrl:getBaseUrl(app.job_link),role:app.role||'—',jUrl:app.job_link||null,sec:sec,status:status,rating:parsePriority(app.priority),needsAction:isOverdue(app.follow_up_date),location:app.location||'',dateCell:dateCell,sortDate:sortDate,nextStep:app.next_step||null});
  });
  recs.forEach(function(rec){
    var status=rec.status||'considering',sec=getSection(status);
    var sortDate,dateCell;
    if(sec==='closed'){
      sortDate=rec.date_researched||rec.date_added||'';
      var sh=rec.stage_history||[];
      var start=rec.date_added||'';
      var end=(sh[sh.length-1]&&sh[sh.length-1].date)||sortDate;
      var dur=durationLabel(daysBetween(start,end));
      dateCell=dur?'<span class="date-dur">'+esc(dur)+'</span>':'<span class="dash">–</span>';
    }else{
      sortDate=rec.date_added||'';
      var fd=fmtDate(rec.date_added);
      dateCell=fd?'<span class="date-disc">'+esc(fd)+'</span>':'<span class="dash">–</span>';
    }
    rows.push({company:rec.company||'—',cUrl:getBaseUrl(rec.job_link),role:rec.role||'—',jUrl:rec.job_link||null,sec:sec,status:status,rating:parsePriority(rec.priority),needsAction:false,location:rec.location||'',dateCell:dateCell,sortDate:sortDate,nextStep:rec.next_step||null});
  });
  var passed=(typeof PASSED_DATA!=='undefined'&&PASSED_DATA.passed)||[];
  passed.forEach(function(p){
    var sh=p.stage_history||[];
    var start=p.date_added||'';
    var end=(sh[sh.length-1]&&sh[sh.length-1].date)||p.date_researched||start;
    var dur=durationLabel(daysBetween(start,end));
    var dateCell=dur?'<span class="date-dur">'+esc(dur)+'</span>':'<span class="dash">–</span>';
    rows.push({company:p.company||'—',cUrl:getBaseUrl(p.job_link),role:p.role||'—',jUrl:p.job_link||null,sec:'passed',status:'pass',rating:parsePriority(p.priority),needsAction:false,location:p.location||'',dateCell:dateCell,sortDate:end,nextStep:p.next_step||null});
  });
  var so={active:0,focus:1,closed:2,passed:3};
  rows.sort(function(a,b){
    if(so[a.sec]!==so[b.sec])return so[a.sec]-so[b.sec];
    var da=a.sortDate||'',db=b.sortDate||'';
    if(da!==db)return da>db?-1:1;
    return a.company.localeCompare(b.company);
  });
  ROWS=rows;
}

function render(){
  var tbody=document.getElementById('tbody'),html='';
  ['active','focus','closed','passed'].forEach(function(sec){
    var sr=ROWS.filter(function(r){return r.sec===sec;});
    if(!sr.length)return;
    var col=COLLAPSED[sec];
    html+='<tr class="section-hdr'+(col?' collapsed':'')+'" data-sec="'+sec+'"><td colspan="6"><span class="caret">&#9662;</span>'+SL[sec]+' ('+sr.length+')</td></tr>';
    sr.forEach(function(row){
      var co=row.cUrl?'<a class="co" href="'+row.cUrl+'" target="_blank">'+esc(row.company)+'</a>':'<span class="co">'+esc(row.company)+'</span>';
      var roleSpan='<span class="'+(row.needsAction?'role-bold':'role-plain')+'">'+esc(row.role)+'</span>';
      var rInner=row.jUrl?'<a class="role-link" href="'+row.jUrl+'" target="_blank">'+roleSpan+'</a>':roleSpan;
      var locCell=row.location?'<span class="loc-text">'+esc(row.location)+'</span>':'<span class="dash">–</span>';
      html+='<tr class="data-row'+(COLLAPSED[row.sec]?' sec-collapsed':'')+'" data-sec="'+row.sec+'" data-status="'+row.status+'" data-rating="'+row.rating+'" data-action="'+(row.needsAction?'1':'0')+'">'
        +'<td>'+co+'</td><td>'+rInner+'</td>'
        +'<td class="center">'+stars(row.rating)+'</td>'
        +'<td>'+badge(row.status,row.nextStep)+'</td>'
        +'<td>'+row.dateCell+'</td>'
        +'<td>'+locCell+'</td></tr>';
    });
  });
  document.getElementById('tbody').innerHTML=html||'<tr><td colspan="6" class="no-data">No data — make sure pipeline-data.js is in the same folder.</td></tr>';
}

function applyFilter(){
  var sf=document.getElementById('f-status').value;
  var ms=parseInt(document.getElementById('f-stars').value,10);
  var sv={};
  document.querySelectorAll('tbody tr.data-row').forEach(function(r){
    var show=true;
    if(sf==='active')show=r.dataset.sec==='active';
    else if(sf==='focus')show=r.dataset.sec==='focus';
    else if(sf==='action')show=r.dataset.action==='1';
    else if(sf==='closed')show=r.dataset.sec==='closed';
    else if(sf==='passed')show=r.dataset.sec==='passed';
    if(ms>0&&parseInt(r.dataset.rating,10)<ms)show=false;
    r.classList.toggle('hidden',!show);
    if(show)sv[r.dataset.sec]=true;
  });
  document.querySelectorAll('tbody tr.section-hdr').forEach(function(h){h.classList.toggle('hidden',!sv[h.dataset.sec]);});
  updateChips();
}

function updateChips(){
  var vis=Array.from(document.querySelectorAll('tbody tr.data-row:not(.hidden)'));
  document.getElementById('chip-active').textContent=vis.filter(function(r){return r.dataset.sec==='active';}).length+' active';
  document.getElementById('chip-focus').textContent=vis.filter(function(r){return r.dataset.sec==='focus';}).length+' focus';
  document.getElementById('chip-closed').textContent=vis.filter(function(r){return r.dataset.sec==='closed';}).length+' closed';
  document.getElementById('chip-passed').textContent=vis.filter(function(r){return r.dataset.sec==='passed';}).length+' passed';
}

var stampEl=document.getElementById('gen-stamp');
stampEl.textContent=typeof PIPELINE_GENERATED!=='undefined'?'Generated '+PIPELINE_GENERATED:'data loaded';
buildRows();render();updateChips();

document.getElementById('tbody').addEventListener('click',function(e){
  var h=e.target.closest('tr.section-hdr');
  if(!h)return;
  var sec=h.dataset.sec;
  var collapsed=h.classList.toggle('collapsed');
  COLLAPSED[sec]=collapsed;
  document.querySelectorAll('tbody tr.data-row[data-sec="'+sec+'"]').forEach(function(r){
    r.classList.toggle('sec-collapsed',collapsed);
  });
});

var tipEl=document.getElementById('status-tip');
function positionTip(e){
  var x=e.clientX+14,y=e.clientY+14;
  var maxX=window.innerWidth-310,maxY=window.innerHeight-90;
  if(x>maxX)x=e.clientX-314;
  if(y>maxY)y=e.clientY-40;
  tipEl.style.left=x+'px';
  tipEl.style.top=y+'px';
}
document.getElementById('tbody').addEventListener('mouseover',function(e){
  var t=e.target.closest('.badge[data-next]');
  if(!t)return;
  tipEl.textContent=t.getAttribute('data-next');
  tipEl.style.display='block';
  positionTip(e);
});
document.getElementById('tbody').addEventListener('mousemove',function(e){
  if(tipEl.style.display==='block'&&e.target.closest('.badge[data-next]'))positionTip(e);
});
document.getElementById('tbody').addEventListener('mouseout',function(e){
  var t=e.target.closest('.badge[data-next]');
  if(!t)return;
  tipEl.style.display='none';
});
</script>
</body>
</html>
```

---

## 5. Generate the embedded timeline

Run the plugin's timeline generator against the user's data directory:

```bash
python3 {plugin_dir}/scripts/build_timeline.py {user_dir}/CareerNavigator
```

This reads `tracker.json` (respecting the split `detail_file`/`contacts_file` schema) and writes `{user_dir}/CareerNavigator/timeline.html`, which `pipeline-status.html` embeds via iframe.

---

## 6. Open in browser

```bash
python3 -c "import webbrowser, os; webbrowser.open('file://' + os.path.abspath('{user_dir}/CareerNavigator/pipeline-status.html'))"
```

## 7. Confirm

```
Pipeline status generated → {user_dir}/CareerNavigator/pipeline-status.html
Opening in browser.
```

If the files already exist, overwrite them — this is always a fresh snapshot.

---

## Guardrails

- Never fabricate data. If `tracker.json`, `recommendations.json`, or `passed.json` is missing, direct the user to `/career-navigator:launch` and stop.
- `pipeline-data.js` is a plain JS globals file, not JSON — do not wrap it in `export` or ES module syntax; `pipeline-status.html` loads it via a plain `<script src>` tag.
- Keep `pipeline-data.js`, `pipeline-status.html`, and `timeline.html` co-located in `{user_dir}/CareerNavigator/` — the page's iframe and script-src references are relative paths.
- This skill can be run on demand or scheduled nightly via `/career-navigator:setup-schedule` (dashboard-refresh option) — either path performs the exact same steps.
