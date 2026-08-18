---
name: pipeline-status-artifact
description: "Creates or updates a persistent Cowork live artifact showing the full job search pipeline — filterable table of all active applications, recommended roles, and closed entries. Refreshes automatically on every open: reads tracker.json, recommendations.json, and artifacts-index.json. Shows status badges, priority rating, resume links, and one-click tailor shortcuts. Also invocable via /career-navigator:pipeline-status-artifact."
triggers:
  - "create pipeline status artifact"
  - "set up live dashboard"
  - "job search status artifact"
  - "live pipeline view"
  - "create my pipeline artifact"
  - "pipeline status page"
  - "create live job search view"
  - "set up status page"
  - "pipeline artifact"
  - "/career-navigator:pipeline-status-artifact"
  - "/career-navigator:pipeline-artifact"
  - "/pipeline-status-artifact"
---

Create (or update) a persistent Cowork live artifact that shows the full job search
pipeline in a filterable table. Every time the user opens the artifact it re-reads
`tracker.json`, `recommendations.json`, and `artifacts-index.json` from disk, so
the view is always current without re-running a skill.

---

## 1. Verify Career Navigator setup

Application data uses the split layout defined in [references/tracker-schema.md](../../references/tracker-schema.md) — read it before any read or write.

Read `{user_dir}/CareerNavigator/tracker.json` and
`{user_dir}/CareerNavigator/recommendations.json` to confirm the files exist.

Every column this artifact renders (`id`, `company`, `role`, `status`, `priority`,
`location`, `job_link`, `follow_up_date`, `artifacts`) is a **summary row** field, so the
artifact loads exactly three files and never touches
`applications/<application_id>.json` or `contacts/<company-slug>.json`. That is the
performance win of the split — the table stays one read per file no matter how large the
pipeline gets. The row also carries `application`, `latest_stage`, `latest_stage_date`,
`notes_count`, `stage_count`, and `contact_count`, so a "last stage" or "contacts" column
can be added with no extra reads.

**If you ever extend this artifact to render per-application detail** — a stage timeline,
note excerpts, contact names — it must load each application's `detail_file` (and
`contacts_file`, filtered to entries whose `application` matches the row's `application`
label, deduped by `name`) explicitly, one read per application. Reading `tracker.json`
alone will silently produce empty timelines and blank contact cells: no error, just an
artifact that looks fine and shows nothing.

If both are missing, output:
> Pipeline artifact not set up: run `/career-navigator:launch` first to initialize Career Navigator.

---

## 2. Check for an existing pipeline-status artifact

Load and call `mcp__cowork__list_artifacts`. Look for any artifact whose name
contains "pipeline" or "job search" (case-insensitive).

**If a matching artifact is found:**
- Tell the user: "A pipeline status artifact already exists. Updating it with the
  latest template."
- Use `mcp__cowork__update_artifact` with the existing artifact's ID
- Skip to Step 4

---

## 3. Resolve user name

Read `{user_dir}/CareerNavigator/profile.md`. Extract the user's name from the
profile (typically the first heading or a `name:` field). Fall back to "Your" if
not found.

---

## 4. Build and create/update the artifact

Resolve `{user_dir}` to its actual absolute path on disk.

Call `mcp__cowork__create_artifact` (or `mcp__cowork__update_artifact`) with:

- **name**: `Job Search — Pipeline Status`
- **description**: `Full job search pipeline — filterable by status and section. Active applications, recommended roles, and closed entries. Resume links and tailor shortcuts.`
- **html**: the complete HTML below, after substituting all placeholders

### Placeholder substitutions

Before passing the HTML, do a literal string replacement:
- `{{TRACKER_PATH}}` → actual absolute path to tracker.json
  (e.g. `/Users/jane/career/CareerNavigator/tracker.json`)
- `{{RECS_PATH}}` → actual absolute path to recommendations.json
- `{{ARTIFACTS_PATH}}` → actual absolute path to artifacts-index.json
- `{{USER_NAME}}` → user's name from profile.md (e.g. `Jane Smith`)

### HTML template

```html
<!DOCTYPE html>
<script type="application/json" id="cowork-artifact-meta">
{
  "name": "Job Search — Pipeline Status",
  "schemaVersion": 1,
  "description": "Full job search pipeline — filterable by status and section. Active applications, recommended roles, and closed entries. Resume links and tailor shortcuts.",
  "mcpTools": [
    "mcp__filesystem__read_text_file"
  ],
  "mcpServerNames": [
    "filesystem"
  ]
}
</script>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Job Search — Pipeline Status</title>
<style>
:root { color-scheme: light; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #fff; color: #1a1a1a; padding: 20px 20px 48px; font-size: 13px; }
h1 { font-size: 16px; font-weight: 500; margin-bottom: 3px; }
.meta { font-size: 11px; color: #999; margin-bottom: 14px; }
.meta .synced { color: #10b981; font-weight: 500; }
.meta .sync-err { color: #f59e0b; font-weight: 500; }
.summary { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px; }
.chip { font-size: 11px; padding: 3px 10px; border-radius: 20px; font-weight: 500; cursor: default; }
.chip-active  { background: #d1fae5; color: #065f46; }
.chip-focus   { background: #ede9fe; color: #5b21b6; }
.chip-closed  { background: #f3f4f6; color: #4b5563; }
.controls { display: flex; gap: 10px; margin-bottom: 12px; align-items: center; flex-wrap: wrap; }
.controls label { font-size: 11px; color: #666; }
select { font-size: 11px; padding: 3px 8px; border: 0.5px solid #d1d5db; border-radius: 6px; background: #fff; color: #1a1a1a; cursor: pointer; }
table { width: 100%; border-collapse: collapse; font-size: 12px; }
col.col-co     { width: 15%; }
col.col-role   { width: 38%; }
col.col-stars  { width: 10%; }
col.col-status { width: 12%; }
col.col-loc    { width: 13%; }
col.col-resume { width: 12%; }
thead th { font-size: 10px; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; padding: 7px 8px; border-bottom: 1px solid #e5e7eb; background: #fafafa; text-align: left; position: sticky; top: 0; z-index: 2; white-space: nowrap; }
thead th.center { text-align: center; }
tbody tr.section-hdr td { background: #f3f4f6; font-size: 10px; font-weight: 600; color: #6b7280; letter-spacing: 0.06em; text-transform: uppercase; padding: 5px 8px; border-top: 1px solid #e5e7eb; }
tbody tr.data-row { border-bottom: 0.5px solid #f0f0f0; }
tbody tr.data-row:hover { background: #f9fafb; }
tbody tr.hidden { display: none; }
td { padding: 6px 8px; vertical-align: middle; }
td.center { text-align: center; }
a.co { font-weight: 500; color: #1a1a1a; text-decoration: none; border-bottom: 1px solid transparent; }
a.co:hover { border-bottom-color: #6b7280; }
a.role-link { color: #374151; text-decoration: none; border-bottom: 1px dotted #d1d5db; }
a.role-link:hover { color: #1a1a1a; border-bottom-color: #6b7280; }
span.role-nolink { color: #374151; }
.needs-action .role-text { font-weight: 600; }
.badge { display: inline-block; padding: 2px 7px; border-radius: 4px; font-size: 10px; font-weight: 600; white-space: nowrap; }
.b-applied     { background: #dbeafe; color: #1e40af; }
.b-screen      { background: #d1fae5; color: #065f46; }
.b-interview   { background: #d1fae5; color: #065f46; }
.b-offer       { background: #dcfce7; color: #15803d; }
.b-ghosted     { background: #fef3c7; color: #92400e; }
.b-rejected    { background: #fee2e2; color: #991b1b; }
.b-withdrawn, .b-declined, .b-expired { background: #f3f4f6; color: #4b5563; }
.b-considering { background: #fef9c3; color: #854d0e; }
.b-rec         { background: #ede9fe; color: #5b21b6; }
.b-pass        { background: #f3f4f6; color: #9ca3af; text-decoration: line-through; }
.stars { font-size: 11px; white-space: nowrap; letter-spacing: 1px; }
.loc-text { font-size: 11px; color: #6b7280; }
a.resume-link { display: inline-block; color: #16a34a; font-size: 12px; font-weight: 600; text-decoration: none; }
a.resume-link:hover { text-decoration: underline; }
.tailor-btn { font-size: 10px; color: #7c3aed; background: #ede9fe; border: none; border-radius: 4px; padding: 2px 6px; cursor: pointer; white-space: nowrap; font-family: inherit; }
.tailor-btn:hover { background: #ddd6fe; }
span.dash { color: #e5e7eb; font-size: 13px; }
#toast { position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%); background: #1a1a1a; color: #fff; padding: 8px 18px; border-radius: 8px; font-size: 12px; pointer-events: none; opacity: 0; transition: opacity 0.2s; z-index: 999; white-space: nowrap; }
#toast.show { opacity: 1; }
</style>
</head>
<body>
<h1>Job Search — Pipeline Status</h1>
<p class="meta">{{USER_NAME}} &nbsp;·&nbsp; <span id="sync-status">Loading…</span></p>
<div class="summary">
  <span class="chip chip-active" id="chip-active">— active</span>
  <span class="chip chip-focus"  id="chip-focus">— focus</span>
  <span class="chip chip-closed" id="chip-closed">— closed</span>
</div>
<div class="controls">
  <label>Filter:</label>
  <select id="f-status" onchange="applyFilter()">
    <option value="all">All rows</option>
    <option value="active">Active only</option>
    <option value="focus">Focus / Recommended</option>
    <option value="action">Needs action</option>
    <option value="closed">Closed / passed</option>
  </select>
  <label style="margin-left:6px">Resume:</label>
  <select id="f-resume" onchange="applyFilter()">
    <option value="all">Any</option>
    <option value="yes">Has resume</option>
    <option value="no">No resume yet</option>
  </select>
  <label style="margin-left:6px">Min rating:</label>
  <select id="f-stars" onchange="applyFilter()">
    <option value="0">Any</option>
    <option value="3">3+</option>
    <option value="4">4+</option>
    <option value="5">5 only</option>
  </select>
</div>
<table>
<colgroup>
  <col class="col-co"><col class="col-role"><col class="col-stars">
  <col class="col-status"><col class="col-loc"><col class="col-resume">
</colgroup>
<thead>
<tr>
  <th>Company</th>
  <th>Role</th>
  <th class="center" title="Priority rating">Rating</th>
  <th>Status</th>
  <th>Location</th>
  <th class="center" title="Tailored resume">Resume</th>
</tr>
</thead>
<tbody id="tbody"></tbody>
</table>
<div id="toast"></div>

<script>
// ── paths (embedded at artifact creation time) ──
var TRACKER_PATH   = '{{TRACKER_PATH}}';
var RECS_PATH      = '{{RECS_PATH}}';
var ARTIFACTS_PATH = '{{ARTIFACTS_PATH}}';

// ── helpers ──
function toast(msg, ms) {
  var el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  clearTimeout(el._t);
  el._t = setTimeout(function() { el.classList.remove('show'); }, ms || 3500);
}

function openResume(path) {
  window.open('file://' + path, '_blank');
}

function runTailor(company, role) {
  var cmd = '/career-navigator:tailor-resume ' + company + ' — ' + role;
  if (window.sendPrompt) {
    window.sendPrompt(cmd);
  } else {
    navigator.clipboard.writeText(cmd)
      .then(function() { toast('Copied — paste into chat to tailor resume', 4000); })
      .catch(function() { toast(cmd, 6000); });
  }
}

function getBaseUrl(jobLink) {
  if (!jobLink || jobLink === '#') return null;
  try { return new URL(jobLink).origin; } catch(e) { return null; }
}

function parsePriority(p) {
  if (p === null || p === undefined || p === '') return 0;
  if (typeof p === 'number') return Math.min(5, Math.max(0, Math.round(p)));
  var s = String(p).toLowerCase();
  if (s === 'critical') return 5;
  if (s === 'high')     return 4;
  if (s === 'medium' || s === 'normal') return 3;
  if (s === 'low')      return 2;
  return 0;
}

function isOverdue(followUpDate) {
  if (!followUpDate) return false;
  try {
    var d = new Date(followUpDate);
    var today = new Date(); today.setHours(0,0,0,0);
    return d <= today;
  } catch(e) { return false; }
}

// ── star renderer ──
function stars(n) {
  if (!n) return '<span class="dash">–</span>';
  var s = '';
  for (var i = 1; i <= 5; i++) {
    s += '<span style="color:' + (i <= n ? '#f59e0b' : '#e5e7eb') + '">★</span>';
  }
  return '<span class="stars">' + s + '</span>';
}

// ── badge ──
var BADGE_LABELS = {
  applied:'Applied', phone_screen:'Phone screen', screen:'Phone screen',
  interview:'Interview', offer:'Offer', accepted:'Accepted',
  ghosted:'Ghosted', rejected:'Rejected', withdrawn:'Withdrawn',
  declined_by_candidate:'Declined', expired:'Expired',
  considering:'Considering', pending_decision:'Recommended', pass:'Pass'
};
var BADGE_CLASS = {
  applied:'b-applied', phone_screen:'b-screen', screen:'b-screen',
  interview:'b-interview', offer:'b-offer', accepted:'b-screen',
  ghosted:'b-ghosted', rejected:'b-rejected', withdrawn:'b-withdrawn',
  declined_by_candidate:'b-declined', expired:'b-expired',
  considering:'b-considering', pending_decision:'b-rec', pass:'b-pass'
};
function badge(s) {
  var cls = BADGE_CLASS[s] || 'b-applied';
  var lbl = BADGE_LABELS[s] || s;
  return '<span class="badge ' + cls + '">' + lbl + '</span>';
}

// ── section labels ──
var SECTION_LABELS = {
  active: 'Active Applications',
  focus:  'Focus — Recommended & Considering',
  closed: 'Closed / Resolved / Passed'
};

function getSection(status) {
  var CLOSED  = ['ghosted','rejected','withdrawn','declined_by_candidate','expired','pass'];
  var ACTIVE  = ['applied','phone_screen','screen','interview','offer','accepted'];
  if (CLOSED.indexOf(status) !== -1) return 'closed';
  if (ACTIVE.indexOf(status) !== -1) return 'active';
  return 'focus'; // considering, pending_decision
}

// ── build resume lookup: company+role → file_path ──
function buildResumeLookup(artifactsData) {
  var lookup = {};
  if (!artifactsData) return lookup;
  var arr = artifactsData.artifacts || artifactsData || [];
  if (!Array.isArray(arr)) return lookup;
  arr.forEach(function(a) {
    if (a.type !== 'resume' && a.type !== 'cv') return;
    var key = (a.company || '').toLowerCase() + '|' + (a.role || '').toLowerCase();
    // Prefer more recent entries
    if (!lookup[key] || (a.date_created && a.date_created > (lookup[key].date || ''))) {
      lookup[key] = { path: a.file_path || a.path || a.filename, date: a.date_created };
    }
  });
  return lookup;
}

// ── rows ──
var ROWS = [];

function extractText(raw) {
  if (!raw) return null;
  if (typeof raw === 'string') return raw;
  if (Array.isArray(raw)) {
    return raw.map(function(b) { return (b && (b.text || b.content || '')); }).join('') || null;
  }
  var c = raw.content;
  if (typeof c === 'string') return c;
  if (Array.isArray(c)) {
    return c.map(function(b) { return (b && (b.text || b.content || '')); }).join('') || null;
  }
  if (typeof raw.text === 'string') return raw.text;
  return null;
}

async function loadData() {
  var syncEl = document.getElementById('sync-status');

  var tPromise = window.cowork.callMcpTool('mcp__filesystem__read_text_file', { path: TRACKER_PATH });
  var rPromise = window.cowork.callMcpTool('mcp__filesystem__read_text_file', { path: RECS_PATH });
  var aPromise = window.cowork.callMcpTool('mcp__filesystem__read_text_file', { path: ARTIFACTS_PATH });

  var trackerData = null, recsData = null, artifactsData = null, errors = [];

  try {
    var tr = await tPromise;
    var txt = extractText(tr);
    if (!txt) throw new Error('no text extracted');
    trackerData = JSON.parse(txt);
  } catch(e) { errors.push('tracker'); console.warn('tracker load failed:', e); }

  try {
    var rr = await rPromise;
    var txt = extractText(rr);
    if (!txt) throw new Error('no text extracted');
    recsData = JSON.parse(txt);
  } catch(e) { errors.push('recommendations'); console.warn('recs load failed:', e); }

  try {
    var ar = await aPromise;
    var txt = extractText(ar);
    if (!txt) throw new Error('no text extracted');
    artifactsData = JSON.parse(txt);
  } catch(e) { /* artifacts-index is optional */ }

  // tracker.json holds summary rows only — no notes[], stage_history[], or contacts[]
  var apps  = (trackerData && trackerData.applications)    || [];
  var recs  = (recsData    && recsData.recommendations)    || [];
  var resumeLookup = buildResumeLookup(artifactsData);

  // tracker IDs for deduplication
  var trackerIdSet = new Set(apps.map(function(a) { return a.id; }));

  var rows = [];

  // ── rows from tracker ──
  apps.forEach(function(app) {
    var status   = app.status || 'applied';
    var sec      = getSection(status);
    var rating   = parsePriority(app.priority);
    var baseUrl  = getBaseUrl(app.job_link);
    var needsAct = isOverdue(app.follow_up_date);
    var key      = (app.company || '').toLowerCase() + '|' + (app.role || '').toLowerCase();
    var resumeInfo = resumeLookup[key] || null;
    rows.push({
      id:          app.id,
      company:     app.company || '—',
      cUrl:        baseUrl,
      role:        app.role || '—',
      jUrl:        app.job_link || null,
      sec:         sec,
      status:      status,
      rating:      rating,
      needsAction: needsAct,
      location:    app.location || '',
      resumePath:  resumeInfo ? resumeInfo.path : null,
      source:      'tracker'
    });
  });

  // ── rows from recommendations ──
  recs.forEach(function(rec) {
    var status  = rec.status || 'considering';
    var sec     = getSection(status);
    var rating  = parsePriority(rec.priority);
    var baseUrl = getBaseUrl(rec.job_link);
    var key     = (rec.company || '').toLowerCase() + '|' + (rec.role || '').toLowerCase();
    var resumeInfo = resumeLookup[key] || null;
    rows.push({
      id:          rec.id,
      company:     rec.company || '—',
      cUrl:        baseUrl,
      role:        rec.role || '—',
      jUrl:        rec.job_link || null,
      sec:         sec,
      status:      status,
      rating:      rating,
      needsAction: false,
      location:    rec.location || '',
      resumePath:  resumeInfo ? resumeInfo.path : null,
      source:      'rec'
    });
  });

  // sort: section order → rating desc → company asc
  var secOrder = { active:0, focus:1, closed:2 };
  rows.sort(function(a, b) {
    if (secOrder[a.sec] !== secOrder[b.sec]) return secOrder[a.sec] - secOrder[b.sec];
    if (b.rating !== a.rating) return b.rating - a.rating;
    return a.company.localeCompare(b.company);
  });

  ROWS = rows;

  if (syncEl) {
    if (errors.length === 0) {
      var tu = (trackerData && trackerData.meta && trackerData.meta.last_updated) || '';
      var ru = (recsData    && recsData.meta    && recsData.meta.last_updated)    || '';
      var stamp = [tu && 'tracker ' + tu, ru && 'recs ' + ru].filter(Boolean).join(' · ');
      syncEl.innerHTML = '<span class="synced">Synced' + (stamp ? ' · ' + stamp : '') + '</span>';
    } else {
      syncEl.innerHTML = '<span class="sync-err">Partial load — ' + errors.join(', ') + ' unavailable</span>';
    }
  }

  render();
  updateChips();
}

// ── render ──
function render() {
  var tbody = document.getElementById('tbody');
  var html  = '';

  ['active','focus','closed'].forEach(function(sec) {
    var secRows = ROWS.filter(function(r) { return r.sec === sec; });
    if (!secRows.length) return;
    html += '<tr class="section-hdr" data-sec="' + sec + '"><td colspan="6">' + SECTION_LABELS[sec] + '</td></tr>';

    secRows.forEach(function(row) {
      // Company cell
      var co = row.cUrl
        ? '<a class="co" href="' + row.cUrl + '" target="_blank">' + esc(row.company) + '</a>'
        : '<span class="co">' + esc(row.company) + '</span>';

      // Role cell
      var rInner = row.jUrl
        ? '<a class="role-link" href="' + row.jUrl + '" target="_blank"><span class="role-text">' + esc(row.role) + '</span></a>'
        : '<span class="role-nolink"><span class="role-text">' + esc(row.role) + '</span></span>';

      // Location cell
      var locCell = row.location
        ? '<span class="loc-text">' + esc(row.location) + '</span>'
        : '<span class="dash">–</span>';

      // Resume cell
      var resumeCell;
      if (row.resumePath) {
        var sp = row.resumePath.replace(/'/g, "\\'");
        resumeCell = '<a class="resume-link" href="file://' + sp + '" target="_blank" title="Open resume">✓ view</a>';
      } else if (row.sec !== 'closed') {
        var sc = row.company.replace(/'/g, "\\'");
        var sr = row.role.replace(/'/g, "\\'").replace(/&amp;/g, '&');
        resumeCell = '<button class="tailor-btn" onclick="runTailor(\'' + sc + '\',\'' + sr + '\')" title="Tailor a resume for this role">tailor ↗</button>';
      } else {
        resumeCell = '<span class="dash">–</span>';
      }

      var rowClass = 'data-row' + (row.needsAction ? ' needs-action' : '');
      html += '<tr class="' + rowClass + '"'
        + ' data-sec="'    + row.sec           + '"'
        + ' data-status="' + row.status        + '"'
        + ' data-resume="' + (row.resumePath ? 'yes' : 'no') + '"'
        + ' data-rating="' + row.rating        + '"'
        + ' data-action="' + (row.needsAction ? '1' : '0') + '">'
        + '<td>' + co + '</td>'
        + '<td class="' + (row.needsAction ? 'needs-action' : '') + '">' + rInner + '</td>'
        + '<td class="center">' + stars(row.rating) + '</td>'
        + '<td>' + badge(row.status) + '</td>'
        + '<td>' + locCell + '</td>'
        + '<td class="center">' + resumeCell + '</td>'
        + '</tr>';
    });
  });

  tbody.innerHTML = html;
}

function esc(s) {
  return String(s || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ── filter ──
function applyFilter() {
  var sf       = document.getElementById('f-status').value;
  var rf       = document.getElementById('f-resume').value;
  var minstars = parseInt(document.getElementById('f-stars').value, 10);
  var secVis   = {};

  document.querySelectorAll('tbody tr.data-row').forEach(function(r) {
    var sec = r.dataset.sec, res = r.dataset.resume;
    var rat = parseInt(r.dataset.rating, 10);
    var act = r.dataset.action === '1';
    var show = true;

    if      (sf === 'active') show = sec === 'active';
    else if (sf === 'focus')  show = sec === 'focus';
    else if (sf === 'action') show = act;
    else if (sf === 'closed') show = sec === 'closed';

    if (rf === 'yes' && res !== 'yes') show = false;
    if (rf === 'no'  && res !== 'no')  show = false;
    if (minstars > 0 && rat < minstars) show = false;

    r.classList.toggle('hidden', !show);
    if (show) secVis[sec] = true;
  });

  document.querySelectorAll('tbody tr.section-hdr').forEach(function(h) {
    h.classList.toggle('hidden', !secVis[h.dataset.sec]);
  });

  updateChips();
}

function updateChips() {
  var vis  = Array.from(document.querySelectorAll('tbody tr.data-row:not(.hidden)'));
  var nAct = vis.filter(function(r) { return r.dataset.sec === 'active'; }).length;
  var nFoc = vis.filter(function(r) { return r.dataset.sec === 'focus';  }).length;
  var nClo = vis.filter(function(r) { return r.dataset.sec === 'closed'; }).length;
  document.getElementById('chip-active').textContent = nAct + ' active';
  document.getElementById('chip-focus').textContent  = nFoc + ' focus';
  document.getElementById('chip-closed').textContent = nClo + ' closed';
}

// ── boot ──
render();
updateChips();
loadData();
</script>
</body>
</html>
```

---

## 5. Confirm to the user

After the artifact is created or updated:

```
✅ Pipeline status artifact ready.

Opens a live, filterable table of your full job search pipeline.
It re-reads your tracker and recommendations automatically each time you open it.

  Active:  submitted applications (applied → offer)
  Focus:   recommended roles and roles under consideration
  Closed:  rejected, withdrawn, ghosted, passed

The Resume column shows a view link when a tailored resume exists,
or a "tailor ↗" shortcut to invoke /career-navigator:tailor-resume from chat.
```

---

## Guardrails

- The three path placeholders (`{{TRACKER_PATH}}`, `{{RECS_PATH}}`, `{{ARTIFACTS_PATH}}`)
  **must** be replaced with absolute, fully resolved paths before the HTML is passed
  to `mcp__cowork__create_artifact` — never leave a `{{...}}` literal in the output
- Always use `mcp__cowork__update_artifact` if an existing pipeline artifact is found
  rather than creating a duplicate
- The artifact is read-only: it never writes to tracker.json or any other file
- The artifact reads summary rows only; it must not attempt to fetch
  `applications/*.json` or `contacts/*.json` per row from the browser — a table-sized fan-out
  of filesystem reads is exactly what the split layout is meant to avoid
- `artifacts-index.json` is optional — if it fails to load, the Resume column shows
  "tailor ↗" for all non-closed rows (graceful degradation)
- `sendPrompt()` is the preferred mechanism for the tailor button; clipboard fallback
  is used only if `window.sendPrompt` is not available
