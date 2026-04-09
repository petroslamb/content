from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "atlas_data.json"
OUT_PATH = ROOT / "index.html"


def main() -> None:
    data = json.loads(DATA_PATH.read_text())
    payload = json.dumps(data, ensure_ascii=True)

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Editorial Atlas</title>
  <link rel="icon" href="data:,">
  <style>
    :root {{
      --bg: #f4efe6;
      --panel: #fbf7f0;
      --ink: #1f2a26;
      --muted: #5f6b64;
      --grid: #d7d0c2;
      --accent: #1f6b5c;
      --accent-2: #b85f3d;
      --accent-3: #9b8b3a;
      --shadow: 0 18px 45px rgba(25, 33, 30, 0.08);
      --sans: "Avenir Next", "Segoe UI", "Helvetica Neue", sans-serif;
      --serif: "Iowan Old Style", "Palatino Linotype", "Book Antiqua", Georgia, serif;
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      background:
        radial-gradient(circle at top right, rgba(184, 95, 61, 0.08), transparent 28%),
        radial-gradient(circle at left, rgba(31, 107, 92, 0.10), transparent 22%),
        var(--bg);
      color: var(--ink);
      font-family: var(--sans);
      line-height: 1.5;
    }}

    .shell {{
      max-width: 1380px;
      margin: 0 auto;
      padding: 36px 24px 64px;
    }}

    .hero {{
      display: grid;
      grid-template-columns: 1.5fr 1fr;
      gap: 18px;
      align-items: start;
      margin-bottom: 24px;
    }}

    .hero-card, .panel {{
      background: rgba(251, 247, 240, 0.94);
      border: 1px solid rgba(31, 42, 38, 0.08);
      border-radius: 22px;
      box-shadow: var(--shadow);
    }}

    .hero-card {{
      padding: 28px;
    }}

    .eyebrow {{
      margin: 0 0 8px;
      font-size: 12px;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: var(--accent);
      font-weight: 700;
    }}

    h1, h2, h3 {{
      margin: 0;
      font-family: var(--serif);
      font-weight: 700;
      line-height: 1.05;
    }}

    h1 {{
      font-size: clamp(2.2rem, 3vw, 3.6rem);
      margin-bottom: 12px;
    }}

    .hero-copy {{
      max-width: 58ch;
      color: var(--muted);
      font-size: 1.02rem;
    }}

    .hero-list {{
      margin-top: 18px;
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }}

    .hero-metric {{
      padding: 14px 16px;
      border-radius: 16px;
      background: linear-gradient(180deg, rgba(31, 107, 92, 0.08), rgba(31, 107, 92, 0.03));
      border: 1px solid rgba(31, 107, 92, 0.12);
    }}

    .hero-metric strong {{
      display: block;
      font-size: 1.45rem;
      color: var(--ink);
    }}

    .hero-metric span {{
      color: var(--muted);
      font-size: 0.92rem;
    }}

    .anchor-list {{
      padding: 24px;
    }}

    .anchor-list h2 {{
      font-size: 1.3rem;
      margin-bottom: 14px;
    }}

    .anchor-list ol {{
      margin: 0;
      padding-left: 20px;
    }}

    .anchor-list li {{
      margin-bottom: 10px;
      color: var(--muted);
    }}

    .layout {{
      display: grid;
      grid-template-columns: minmax(0, 1.8fr) minmax(320px, 0.9fr);
      gap: 18px;
      margin-bottom: 18px;
    }}

    .panel {{
      padding: 22px;
    }}

    .panel h2 {{
      font-size: 1.6rem;
      margin-bottom: 6px;
    }}

    .panel p.note {{
      margin: 0 0 16px;
      color: var(--muted);
      max-width: 68ch;
    }}

    svg {{
      width: 100%;
      height: auto;
      display: block;
    }}

    .detail-card {{
      min-height: 100%;
    }}

    .detail-meta {{
      margin-top: 18px;
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
    }}

    .meta-box {{
      padding: 12px;
      border-radius: 14px;
      background: rgba(31, 42, 38, 0.04);
    }}

    .meta-box strong {{
      display: block;
      font-size: 1.15rem;
    }}

    .chip {{
      display: inline-block;
      padding: 6px 10px;
      border-radius: 999px;
      background: rgba(184, 95, 61, 0.12);
      color: var(--accent-2);
      font-size: 0.85rem;
      font-weight: 700;
      margin: 14px 8px 0 0;
    }}

    .detail-copy {{
      margin-top: 18px;
      display: grid;
      gap: 14px;
    }}

    .detail-copy div {{
      padding-top: 12px;
      border-top: 1px solid rgba(31, 42, 38, 0.08);
    }}

    .detail-copy strong {{
      display: block;
      margin-bottom: 4px;
      color: var(--ink);
    }}

    .compact-detail {{
      margin: 14px 0 16px;
      padding: 14px;
      border-radius: 16px;
      background: rgba(31, 42, 38, 0.04);
      border: 1px solid rgba(31, 42, 38, 0.08);
    }}

    .compact-detail h3 {{
      margin: 0 0 6px;
      font-size: 1.12rem;
    }}

    .compact-detail p {{
      margin: 0;
      color: var(--muted);
      font-size: 0.94rem;
    }}

    .compact-grid {{
      margin-top: 10px;
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 8px;
    }}

    .compact-box {{
      padding: 9px 10px;
      border-radius: 12px;
      background: rgba(251, 247, 240, 0.86);
    }}

    .compact-box strong {{
      display: block;
      font-size: 1rem;
    }}

    .compact-box span {{
      color: var(--muted);
      font-size: 0.82rem;
    }}

    .heatmap-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.95rem;
    }}

    .heatmap-table th,
    .heatmap-table td {{
      padding: 10px 12px;
      border-bottom: 1px solid rgba(31, 42, 38, 0.08);
      text-align: left;
      vertical-align: middle;
    }}

    .heatmap-table th.num,
    .heatmap-table td.num {{
      text-align: center;
      width: 88px;
      font-variant-numeric: tabular-nums;
    }}

    .heat-cell {{
      border-radius: 10px;
      font-weight: 700;
    }}

    .heatmap-wrap {{
      overflow-x: auto;
    }}

    .vector-grid {{
      display: grid;
      grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr);
      gap: 18px;
      align-items: start;
    }}

    .vector-note {{
      color: var(--muted);
    }}

    .pull-table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 14px;
    }}

    .pull-table th,
    .pull-table td {{
      padding: 10px 12px;
      border-bottom: 1px solid rgba(31, 42, 38, 0.08);
      text-align: left;
      vertical-align: top;
    }}

    .footer-note {{
      margin-top: 20px;
      color: var(--muted);
      font-size: 0.9rem;
    }}

    .legend {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px 14px;
      margin-top: 10px;
      color: var(--muted);
      font-size: 0.9rem;
    }}

    .legend-dot {{
      display: inline-block;
      width: 10px;
      height: 10px;
      border-radius: 999px;
      margin-right: 6px;
      vertical-align: middle;
    }}

    .tab-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin: 0 0 18px;
    }}

    .tab-btn {{
      border: 1px solid rgba(31, 42, 38, 0.10);
      background: rgba(251, 247, 240, 0.78);
      color: var(--muted);
      padding: 11px 16px;
      border-radius: 999px;
      font: inherit;
      font-size: 0.95rem;
      font-weight: 700;
      cursor: pointer;
      transition: 120ms ease;
    }}

    .tab-btn:hover {{
      color: var(--ink);
      border-color: rgba(31, 107, 92, 0.22);
    }}

    .tab-btn.active {{
      background: var(--ink);
      color: #f9f5ee;
      border-color: var(--ink);
    }}

    .tab-panel {{
      display: none;
    }}

    .tab-panel.active {{
      display: block;
    }}

    .tab-grid {{
      display: grid;
      grid-template-columns: minmax(0, 1.45fr) minmax(300px, 0.9fr);
      gap: 18px;
      margin-bottom: 18px;
    }}

    .mini-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.95rem;
    }}

    .mini-table th,
    .mini-table td {{
      padding: 10px 12px;
      border-bottom: 1px solid rgba(31, 42, 38, 0.08);
      text-align: left;
      vertical-align: top;
    }}

    .mini-table td.num,
    .mini-table th.num {{
      text-align: center;
      width: 82px;
      font-variant-numeric: tabular-nums;
    }}

    .click-row {{
      cursor: pointer;
    }}

    .click-row:hover td {{
      background: rgba(31, 107, 92, 0.05);
    }}

    .selected-row td {{
      background: rgba(31, 107, 92, 0.10);
    }}

    .matrix-wrap {{
      overflow-x: auto;
    }}

    .matrix-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.92rem;
    }}

    .matrix-table th,
    .matrix-table td {{
      padding: 9px 10px;
      border-bottom: 1px solid rgba(31, 42, 38, 0.08);
      border-right: 1px solid rgba(31, 42, 38, 0.05);
      text-align: center;
      white-space: nowrap;
    }}

    .matrix-table th:first-child,
    .matrix-table td:first-child {{
      text-align: left;
      position: sticky;
      left: 0;
      background: rgba(251, 247, 240, 0.98);
      z-index: 1;
    }}

    .matrix-table tr.selected-row td,
    .matrix-table tr.selected-row td:first-child {{
      background: rgba(31, 107, 92, 0.10);
    }}

    .move-hit {{
      border-radius: 8px;
      font-weight: 700;
      color: var(--ink);
      background: rgba(31, 107, 92, 0.16);
    }}

    .move-miss {{
      color: #a9b0ab;
    }}

    .draft-head {{
      margin-bottom: 14px;
    }}

    .draft-head strong {{
      display: block;
      font-size: 1.05rem;
      color: var(--ink);
    }}

    .draft-head span {{
      color: var(--muted);
      font-size: 0.94rem;
    }}

    @media (max-width: 980px) {{
      .hero,
      .layout,
      .vector-grid,
      .tab-grid {{
        grid-template-columns: 1fr;
      }}

      .detail-meta {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }}
    }}

    @media (max-width: 640px) {{
      .shell {{
        padding: 18px 14px 42px;
      }}

      .hero-card,
      .panel,
      .anchor-list {{
        padding: 18px;
      }}

      .hero-list,
      .detail-meta,
      .compact-grid {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <section class="hero">
      <div class="hero-card">
        <p class="eyebrow">Editorial Atlas</p>
        <h1>Published essays as a navigable editorial system</h1>
        <p class="hero-copy">
          This viewer turns the archive into an operational map. The point is
          not ranking for its own sake. The point is to see what kinds of essay
          objects already exist, where they get their force, and which older
          essays should pull a new draft.
        </p>
        <div class="hero-list" id="hero-metrics"></div>
      </div>
      <aside class="hero-card anchor-list">
        <h2>Current anchor essays</h2>
        <ol id="anchor-list"></ol>
      </aside>
    </section>

    <nav class="tab-bar" aria-label="Atlas views">
      <button class="tab-btn active" data-tab="overview">Overview</button>
      <button class="tab-btn" data-tab="debate">Debate × Precision</button>
      <button class="tab-btn" data-tab="synthesis">Synthesis × Utility</button>
      <button class="tab-btn" data-tab="openings">Openings × Endings</button>
      <button class="tab-btn" data-tab="moves">Move Matrix</button>
    </nav>

    <section id="tab-overview" class="tab-panel active">
      <section class="layout">
        <div class="panel">
          <p class="eyebrow">View 1</p>
          <h2>Constellation</h2>
          <p class="note">
            X axis is traction. Y axis is craft. Dot size tracks publication
            power. Click a point to inspect the essay card. Overlapping essays get
            small plotted decimal offsets so the real score remains intact while
            the constellation stays legible.
          </p>
          <div id="scatter-root"></div>
          <div class="legend" id="constellation-legend"></div>
        </div>
        <div class="panel detail-card">
          <p class="eyebrow">Selected Essay</p>
          <h2 id="detail-title">The Transformer Attractor</h2>
          <p class="note" id="detail-subtitle"></p>
          <div class="detail-meta">
            <div class="meta-box">
              <span>Traction</span>
              <strong id="detail-traction">9</strong>
            </div>
            <div class="meta-box">
              <span>Craft</span>
              <strong id="detail-craft">9</strong>
            </div>
            <div class="meta-box">
              <span>Power</span>
              <strong id="detail-power">10</strong>
            </div>
          </div>
          <div id="detail-chips"></div>
          <div class="detail-copy">
            <div>
              <strong>Identity</strong>
              <span id="detail-identity"></span>
            </div>
            <div>
              <strong>Signature</strong>
              <span id="detail-signature"></span>
            </div>
            <div>
              <strong>Overpull risk</strong>
              <span id="detail-risk"></span>
            </div>
            <div>
              <strong>Section profile</strong>
              <span id="detail-sections"></span>
            </div>
          </div>
        </div>
      </section>

      <section class="panel" style="margin-bottom: 18px;">
        <p class="eyebrow">View 2</p>
        <h2>Section heatmap</h2>
        <p class="note">
          This view makes section borrowing visible. It shows where each essay
          gets its force rather than just where it lands overall.
        </p>
        <div class="heatmap-wrap">
          <table class="heatmap-table" id="heatmap-table">
            <thead>
              <tr>
                <th>Essay</th>
                <th class="num">Opening</th>
                <th class="num">Thesis</th>
                <th class="num">Development</th>
                <th class="num">Borders</th>
                <th class="num">Ending</th>
                <th class="num">Refs</th>
                <th>Power source</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </section>

      <section class="panel">
        <p class="eyebrow">View 3</p>
        <h2>Draft pull vector</h2>
        <div class="vector-grid">
          <div>
            <div class="draft-head" id="draft-head"></div>
            <p class="vector-note" id="draft-problem"></p>
            <div id="vector-root"></div>
          </div>
          <div>
            <table class="pull-table">
              <thead>
                <tr>
                  <th>Section</th>
                  <th>Pull essay</th>
                  <th>Desired strength</th>
                </tr>
              </thead>
              <tbody id="pull-table-body"></tbody>
            </table>
            <p class="footer-note">
              This vector view is not a ranking device. It is a design-time
              routing view for shaping a draft intentionally.
            </p>
          </div>
        </div>
      </section>
    </section>

    <section id="tab-debate" class="tab-panel">
      <div class="tab-grid">
        <div class="panel">
          <p class="eyebrow">Axis View</p>
          <h2>Debate × Precision</h2>
          <p class="note">
            This separates essays built to travel in public argument from essays
            built to hold sharper conceptual borders. It is the cleanest next
            view after the overview constellation.
          </p>
          <div id="debate-root"></div>
          <div class="legend" id="debate-legend"></div>
        </div>
        <div class="panel">
          <p class="eyebrow">Read</p>
          <h2>What this view clarifies</h2>
          <p class="note">
            `Transformer Attractor` and `Moltbook` sit far toward public
            argument. `Binding Gap` sits far toward precision. `Autonomy Tax`
            and `Illusion of the Swarm` are balanced enough to work as both
            strong public objects and controlled frameworks.
          </p>
          <div class="compact-detail" id="debate-detail"></div>
          <table class="mini-table" id="debate-table">
            <thead>
              <tr>
                <th>Essay</th>
                <th class="num">Debate</th>
                <th class="num">Precision</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </div>
    </section>

    <section id="tab-synthesis" class="tab-panel">
      <div class="tab-grid">
        <div class="panel">
          <p class="eyebrow">Axis View</p>
          <h2>Synthesis × Utility</h2>
          <p class="note">
            This separates archive-anchor surveys from operator-facing essays.
            It is useful when deciding whether a new draft wants to become a
            flagship essay, a synthesis essay, or a practical companion.
          </p>
          <div id="synthesis-root"></div>
          <div class="legend" id="synthesis-legend"></div>
        </div>
        <div class="panel">
          <p class="eyebrow">Read</p>
          <h2>Which essays dominate this tradeoff</h2>
          <div class="compact-detail" id="synthesis-detail"></div>
          <table class="mini-table" id="synthesis-table">
            <thead>
              <tr>
                <th>Essay</th>
                <th class="num">Synthesis</th>
                <th class="num">Utility</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
          <p class="footer-note">
            `What Actually Works` and `Illusion of the Swarm` are the archive's
            strongest synthesis anchors. `Autonomy Tax` and the `Operating
            Agents` set dominate the utility side.
          </p>
        </div>
      </div>
    </section>

    <section id="tab-openings" class="tab-panel">
      <div class="tab-grid">
        <div class="panel">
          <p class="eyebrow">Section View</p>
          <h2>Openings × Endings</h2>
          <p class="note">
            This compares how essays start and how they land. It helps diagnose
            drafts that ignite well but taper, or essays that only become strong
            late.
          </p>
          <div id="opening-ending-root"></div>
          <div class="legend" id="opening-ending-legend"></div>
        </div>
        <div class="panel">
          <p class="eyebrow">Read</p>
          <h2>Opening / ending profile</h2>
          <div class="compact-detail" id="openings-detail"></div>
          <table class="mini-table" id="opening-ending-table">
            <thead>
              <tr>
                <th>Essay</th>
                <th class="num">Opening</th>
                <th class="num">Ending</th>
                <th class="num">Gap</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </div>
    </section>

    <section id="tab-moves" class="tab-panel">
      <section class="panel">
        <p class="eyebrow">Pattern View</p>
        <h2>Move matrix</h2>
        <p class="note">
          This connects the visual atlas back to the reverse-engineered move
          library. It shows which archive essays exemplify which editorial
          moves, so the atlas can guide drafting rather than just describe the
          archive.
        </p>
        <div class="compact-detail" id="moves-detail"></div>
        <div class="matrix-wrap">
          <table class="matrix-table" id="move-matrix">
            <thead></thead>
            <tbody></tbody>
          </table>
        </div>
      </section>
    </section>
  </div>

  <script id="atlas-data" type="application/json">{payload}</script>
  <script>
    const atlas = JSON.parse(document.getElementById('atlas-data').textContent);
    const essays = [...atlas.essays];

    const MOVE_LABELS = {{
      failure_or_anomaly_cold_open: 'Cold open',
      contrarian_compression: 'Contrarian compression',
      coined_frame_with_borders: 'Coined frame',
      scroll_map: 'Scroll map',
      builder_first_doctrine: 'Builder doctrine',
      historical_synthesis: 'Historical synthesis',
      practical_heuristic_section: 'Practical heuristic',
      falsifiable_prediction_close: 'Prediction close',
      topical_narrative_hijack: 'Topical hijack',
      series_packaging: 'Series packaging',
      chapterized_technical_explainer: 'Chapterized explainer',
      doctrine_ending: 'Doctrine ending'
    }};

    const MOVE_ORDER = [
      'failure_or_anomaly_cold_open',
      'contrarian_compression',
      'coined_frame_with_borders',
      'scroll_map',
      'builder_first_doctrine',
      'historical_synthesis',
      'practical_heuristic_section',
      'falsifiable_prediction_close',
      'topical_narrative_hijack',
      'series_packaging',
      'chapterized_technical_explainer',
      'doctrine_ending'
    ];

    const drafts = [...(atlas.drafts || [])];
    const essayMap = new Map(essays.map(essay => [essay.title, essay]));
    let selectedEssayTitle = 'The Transformer Attractor';

    function metricColor(value) {{
      if (value >= 9) return '#1f6b5c';
      if (value >= 8) return '#497e68';
      if (value >= 7) return '#a97738';
      return '#b85f3d';
    }}

    function confidenceRank(confidence) {{
      return confidence === 'high' ? 3 : confidence === 'medium' ? 2 : 1;
    }}

    function confidenceStroke(confidence) {{
      if (confidence === 'high') return '0';
      if (confidence === 'medium') return '5 3';
      return '2 3';
    }}

    function confidenceOpacity(confidence) {{
      if (confidence === 'high') return 0.82;
      if (confidence === 'medium') return 0.72;
      return 0.62;
    }}

    function heatColor(value) {{
      const alpha = 0.10 + ((value - 5) / 5) * 0.28;
      return `rgba(31, 107, 92, ${{alpha.toFixed(3)}})`;
    }}

    function shortTitle(essay) {{
      return essay.short_label || essay.title;
    }}

    function clamp(value, min, max) {{
      return Math.max(min, Math.min(max, value));
    }}

    function buildPlottedEssays(source, xKey, yKey) {{
      const offsets = [
        {{ x: 0.00, y: 0.00, dx: 12, dy: -12, anchor: 'start' }},
        {{ x: 0.16, y: 0.18, dx: 12, dy: -10, anchor: 'start' }},
        {{ x: -0.18, y: 0.16, dx: -12, dy: -10, anchor: 'end' }},
        {{ x: 0.18, y: -0.16, dx: 12, dy: 18, anchor: 'start' }},
        {{ x: -0.18, y: -0.18, dx: -12, dy: 18, anchor: 'end' }},
        {{ x: 0.28, y: 0.00, dx: 14, dy: 4, anchor: 'start' }},
        {{ x: -0.28, y: 0.00, dx: -14, dy: 4, anchor: 'end' }},
        {{ x: 0.00, y: 0.28, dx: 0, dy: -16, anchor: 'middle' }},
        {{ x: 0.00, y: -0.28, dx: 0, dy: 22, anchor: 'middle' }},
        {{ x: 0.32, y: 0.20, dx: 14, dy: -14, anchor: 'start' }},
        {{ x: -0.32, y: 0.20, dx: -14, dy: -14, anchor: 'end' }},
        {{ x: 0.32, y: -0.22, dx: 14, dy: 20, anchor: 'start' }},
        {{ x: -0.32, y: -0.22, dx: -14, dy: 20, anchor: 'end' }}
      ];

      const groups = new Map();
      source.forEach((essay, idx) => {{
        const key = `${{essay[xKey]}}-${{essay[yKey]}}`;
        if (!groups.has(key)) groups.set(key, []);
        groups.get(key).push({{ essay, idx }});
      }});

      return source.map((essay, idx) => {{
        const key = `${{essay[xKey]}}-${{essay[yKey]}}`;
        const group = groups.get(key) || [{{ essay, idx }}];
        const position = group.findIndex(item => item.idx === idx);
        const o = offsets[position % offsets.length];
        return {{
          ...essay,
          plot_x: clamp(essay[xKey] + o.x, 5.12, 9.88),
          plot_y: clamp(essay[yKey] + o.y, 5.12, 9.88),
          label_dx: o.dx,
          label_dy: o.dy,
          label_anchor: o.anchor
        }};
      }});
    }}

    const plottedEssays = buildPlottedEssays(essays, 'traction', 'craft');

    function selectedEssay() {{
      return essayMap.get(selectedEssayTitle) || plottedEssays[0];
    }}

    function topAnchors() {{
      return essays
        .slice()
        .sort((a, b) => b.publication_power - a.publication_power || b.traction - a.traction)
        .slice(0, 6);
    }}

    function renderHero() {{
      const metricsRoot = document.getElementById('hero-metrics');
      const anchorRoot = document.getElementById('anchor-list');
      const metrics = [
        {{ label: 'Published essays', value: String(essays.length) }},
        {{ label: 'Top power score', value: String(Math.max(...essays.map(e => e.publication_power))) }},
        {{ label: 'Top traction score', value: String(Math.max(...essays.map(e => e.traction))) }},
        {{ label: 'Top craft score', value: String(Math.max(...essays.map(e => e.craft))) }}
      ];
      metricsRoot.innerHTML = metrics.map(m => `
        <div class="hero-metric">
          <strong>${{m.value}}</strong>
          <span>${{m.label}}</span>
        </div>
      `).join('');

      anchorRoot.innerHTML = topAnchors().map(e => `
        <li><strong>${{e.title}}</strong><br>${{e.identity}}</li>
      `).join('');
    }}

    function renderCompactDetail(targetId, essay) {{
      const root = document.getElementById(targetId);
      if (!root) return;
      root.innerHTML = `
        <h3>${{essay.short_label || essay.title}}</h3>
        <p>${{essay.identity}}</p>
        <div class="compact-grid">
          <div class="compact-box">
            <strong>${{essay.debate}}</strong>
            <span>debate</span>
          </div>
          <div class="compact-box">
            <strong>${{essay.precision}}</strong>
            <span>precision</span>
          </div>
          <div class="compact-box">
            <strong>${{essay.confidence}}</strong>
            <span>confidence</span>
          </div>
        </div>
      `;
    }}

    function renderDetail(essay) {{
      document.getElementById('detail-title').textContent = essay.title;
      document.getElementById('detail-subtitle').textContent = `${{essay.date}} | ${{essay.words}} words | confidence: ${{essay.confidence}}`;
      document.getElementById('detail-traction').textContent = essay.traction;
      document.getElementById('detail-craft').textContent = essay.craft;
      document.getElementById('detail-power').textContent = essay.publication_power;
      document.getElementById('detail-identity').textContent = essay.identity;
      document.getElementById('detail-signature').textContent = essay.signature;
      document.getElementById('detail-risk').textContent = essay.overpull_risk;
      document.getElementById('detail-sections').textContent =
        `opening ${{essay.opening}}, thesis ${{essay.thesis_lock}}, development ${{essay.development}}, borders ${{essay.borders}}, ending ${{essay.ending}}, refs ${{essay.reference_handling}}`;
      document.getElementById('detail-chips').innerHTML = `
        <span class="chip">${{essay.identity}}</span>
        <span class="chip">traction ${{essay.traction}}</span>
        <span class="chip">craft ${{essay.craft}}</span>
        <span class="chip">confidence ${{essay.confidence}}</span>
      `;
    }}

    function updateSelectionViews() {{
      const essay = selectedEssay();
      renderDetail(essay);
      renderCompactDetail('debate-detail', essay);
      renderCompactDetail('synthesis-detail', essay);
      renderCompactDetail('openings-detail', essay);
      renderCompactDetail('moves-detail', essay);
      document.querySelectorAll('[data-essay-title]').forEach(node => {{
        node.classList.toggle('selected-row', node.dataset.essayTitle === essay.title);
      }});
    }}

    function setSelectedEssay(title) {{
      if (!essayMap.has(title)) return;
      selectedEssayTitle = title;
      updateSelectionViews();
    }}

    function renderScatter() {{
      const root = document.getElementById('scatter-root');
      const legend = document.getElementById('constellation-legend');
      const width = 900;
      const height = 460;
      const margin = {{ top: 20, right: 28, bottom: 56, left: 58 }};
      const innerWidth = width - margin.left - margin.right;
      const innerHeight = height - margin.top - margin.bottom;
      const xMin = 5;
      const xMax = 10;
      const yMin = 5;
      const yMax = 10;

      const scaleX = value => margin.left + ((value - xMin) / (xMax - xMin)) * innerWidth;
      const scaleY = value => margin.top + innerHeight - ((value - yMin) / (yMax - yMin)) * innerHeight;

      let labels = '';
      let grid = '';
      for (let i = xMin; i <= xMax; i += 1) {{
        const x = scaleX(i);
        const y = scaleY(i);
        grid += `<line x1="${{x}}" y1="${{margin.top}}" x2="${{x}}" y2="${{margin.top + innerHeight}}" stroke="rgba(31,42,38,0.08)" />`;
        grid += `<line x1="${{margin.left}}" y1="${{y}}" x2="${{margin.left + innerWidth}}" y2="${{y}}" stroke="rgba(31,42,38,0.08)" />`;
        labels += `<text x="${{x}}" y="${{height - 18}}" font-size="12" text-anchor="middle" fill="#5f6b64">${{i}}</text>`;
        labels += `<text x="${{margin.left - 18}}" y="${{y + 4}}" font-size="12" text-anchor="middle" fill="#5f6b64">${{i}}</text>`;
      }}

      const pointMarkup = plottedEssays.map((essay, idx) => {{
        const x = scaleX(essay.plot_x);
        const y = scaleY(essay.plot_y);
        const r = 5 + essay.publication_power * 0.85;
        const fill = metricColor(essay.publication_power);
        const labelX = x + essay.label_dx;
        const labelY = y + essay.label_dy;
        const fillOpacity = confidenceOpacity(essay.confidence);
        const strokeDash = confidenceStroke(essay.confidence);
        const label = `
          <line x1="${{x}}" y1="${{y}}" x2="${{labelX}}" y2="${{labelY}}" stroke="rgba(31,42,38,0.14)" stroke-width="1" />
          <text x="${{labelX}}" y="${{labelY}}" font-size="10.5" font-weight="600" text-anchor="${{essay.label_anchor}}" fill="#1f2a26" paint-order="stroke" stroke="rgba(251,247,240,0.92)" stroke-width="4" stroke-linejoin="round">${{shortTitle(essay)}}</text>
        `;
        return `
          <g class="scatter-point" data-index="${{idx}}" style="cursor:pointer">
            <circle cx="${{x}}" cy="${{y}}" r="${{r}}" fill="${{fill}}" fill-opacity="${{fillOpacity}}" stroke="#f4efe6" stroke-width="2" stroke-dasharray="${{strokeDash}}">
              <title>${{essay.title}}</title>
            </circle>
            ${{label}}
          </g>
        `;
      }}).join('');

      root.innerHTML = `
        <svg viewBox="0 0 ${{width}} ${{height}}" role="img" aria-label="Editorial atlas constellation">
          <rect x="0" y="0" width="${{width}}" height="${{height}}" rx="18" fill="rgba(255,255,255,0.18)"></rect>
          ${{grid}}
          <line x1="${{margin.left}}" y1="${{margin.top + innerHeight}}" x2="${{margin.left + innerWidth}}" y2="${{margin.top + innerHeight}}" stroke="#1f2a26" stroke-width="1.5" />
          <line x1="${{margin.left}}" y1="${{margin.top}}" x2="${{margin.left}}" y2="${{margin.top + innerHeight}}" stroke="#1f2a26" stroke-width="1.5" />
          ${{labels}}
          <text x="${{margin.left + innerWidth / 2}}" y="${{height - 4}}" font-size="13" text-anchor="middle" fill="#1f2a26">Traction</text>
          <text x="18" y="${{margin.top + innerHeight / 2}}" font-size="13" text-anchor="middle" fill="#1f2a26" transform="rotate(-90 18 ${{margin.top + innerHeight / 2}})">Craft</text>
          ${{pointMarkup}}
        </svg>
      `;

      root.querySelectorAll('.scatter-point').forEach(node => {{
        node.addEventListener('click', () => {{
          const essay = plottedEssays[Number(node.dataset.index)];
          setSelectedEssay(essay.title);
        }});
      }});

      legend.innerHTML = `
        <span><span class="legend-dot" style="background:${{metricColor(9)}}"></span>power 9-10</span>
        <span><span class="legend-dot" style="background:${{metricColor(8)}}"></span>power 8</span>
        <span><span class="legend-dot" style="background:${{metricColor(7)}}"></span>power 7</span>
        <span><span class="legend-dot" style="background:${{metricColor(6)}}"></span>power 6</span>
        <span>solid = high confidence, dashed = lower confidence</span>
      `;
    }}

    function renderMetricScatter(rootId, legendId, xKey, yKey, xLabel, yLabel) {{
      const root = document.getElementById(rootId);
      const legend = document.getElementById(legendId);
      const width = 900;
      const height = 460;
      const margin = {{ top: 20, right: 28, bottom: 56, left: 58 }};
      const innerWidth = width - margin.left - margin.right;
      const innerHeight = height - margin.top - margin.bottom;
      const xMin = 5;
      const xMax = 10;
      const yMin = 5;
      const yMax = 10;
      const series = buildPlottedEssays(essays, xKey, yKey);

      const scaleX = value => margin.left + ((value - xMin) / (xMax - xMin)) * innerWidth;
      const scaleY = value => margin.top + innerHeight - ((value - yMin) / (yMax - yMin)) * innerHeight;

      let axisLabels = '';
      let grid = '';
      for (let i = xMin; i <= xMax; i += 1) {{
        const x = scaleX(i);
        const y = scaleY(i);
        grid += `<line x1="${{x}}" y1="${{margin.top}}" x2="${{x}}" y2="${{margin.top + innerHeight}}" stroke="rgba(31,42,38,0.08)" />`;
        grid += `<line x1="${{margin.left}}" y1="${{y}}" x2="${{margin.left + innerWidth}}" y2="${{y}}" stroke="rgba(31,42,38,0.08)" />`;
        axisLabels += `<text x="${{x}}" y="${{height - 18}}" font-size="12" text-anchor="middle" fill="#5f6b64">${{i}}</text>`;
        axisLabels += `<text x="${{margin.left - 18}}" y="${{y + 4}}" font-size="12" text-anchor="middle" fill="#5f6b64">${{i}}</text>`;
      }}

      const points = series.map(essay => {{
        const x = scaleX(essay.plot_x);
        const y = scaleY(essay.plot_y);
        const r = 5 + essay.publication_power * 0.85;
        const labelX = x + essay.label_dx;
        const labelY = y + essay.label_dy;
        const fillOpacity = confidenceOpacity(essay.confidence);
        const strokeDash = confidenceStroke(essay.confidence);
        return `
          <g class="metric-point" data-essay-title="${{essay.title}}" style="cursor:pointer">
            <circle cx="${{x}}" cy="${{y}}" r="${{r}}" fill="${{metricColor(essay.publication_power)}}" fill-opacity="${{fillOpacity}}" stroke="#f4efe6" stroke-width="2" stroke-dasharray="${{strokeDash}}">
              <title>${{essay.title}}</title>
            </circle>
            <line x1="${{x}}" y1="${{y}}" x2="${{labelX}}" y2="${{labelY}}" stroke="rgba(31,42,38,0.14)" stroke-width="1" />
            <text x="${{labelX}}" y="${{labelY}}" font-size="10.5" font-weight="600" text-anchor="${{essay.label_anchor}}" fill="#1f2a26" paint-order="stroke" stroke="rgba(251,247,240,0.92)" stroke-width="4" stroke-linejoin="round">${{shortTitle(essay)}}</text>
          </g>
        `;
      }}).join('');

      root.innerHTML = `
        <svg viewBox="0 0 ${{width}} ${{height}}" role="img" aria-label="${{xLabel}} by ${{yLabel}}">
          <rect x="0" y="0" width="${{width}}" height="${{height}}" rx="18" fill="rgba(255,255,255,0.18)"></rect>
          ${{grid}}
          <line x1="${{margin.left}}" y1="${{margin.top + innerHeight}}" x2="${{margin.left + innerWidth}}" y2="${{margin.top + innerHeight}}" stroke="#1f2a26" stroke-width="1.5" />
          <line x1="${{margin.left}}" y1="${{margin.top}}" x2="${{margin.left}}" y2="${{margin.top + innerHeight}}" stroke="#1f2a26" stroke-width="1.5" />
          ${{axisLabels}}
          <text x="${{margin.left + innerWidth / 2}}" y="${{height - 4}}" font-size="13" text-anchor="middle" fill="#1f2a26">${{xLabel}}</text>
          <text x="18" y="${{margin.top + innerHeight / 2}}" font-size="13" text-anchor="middle" fill="#1f2a26" transform="rotate(-90 18 ${{margin.top + innerHeight / 2}})">${{yLabel}}</text>
          ${{points}}
        </svg>
      `;

      if (legend) {{
        legend.innerHTML = `
          <span><span class="legend-dot" style="background:${{metricColor(9)}}"></span>power 9-10</span>
          <span><span class="legend-dot" style="background:${{metricColor(8)}}"></span>power 8</span>
          <span><span class="legend-dot" style="background:${{metricColor(7)}}"></span>power 7</span>
          <span><span class="legend-dot" style="background:${{metricColor(6)}}"></span>power 6</span>
          <span>solid = high confidence, dashed = lower confidence</span>
        `;
      }}

      root.querySelectorAll('.metric-point').forEach(node => {{
        node.addEventListener('click', () => setSelectedEssay(node.dataset.essayTitle));
      }});
    }}

    function renderHeatmap() {{
      const tbody = document.querySelector('#heatmap-table tbody');
      const rows = essays
        .slice()
        .sort((a, b) => b.publication_power - a.publication_power || b.traction - a.traction)
        .map(essay => {{
          const metrics = ['opening', 'thesis_lock', 'development', 'borders', 'ending', 'reference_handling'].map(key => {{
            const value = essay[key];
            return `<td class="num"><span class="heat-cell" style="display:inline-block;min-width:44px;padding:8px 10px;background:${{heatColor(value)}}">${{value}}</span></td>`;
          }}).join('');
          const pairs = [
            ['opening', essay.opening],
            ['thesis', essay.thesis_lock],
            ['development', essay.development],
            ['borders', essay.borders],
            ['ending', essay.ending],
            ['refs', essay.reference_handling]
          ];
          const powerSource = pairs.sort((a, b) => b[1] - a[1])[0][0];
          return `
            <tr class="click-row" data-essay-title="${{essay.title}}">
              <td><strong>${{essay.title}}</strong></td>
              ${{metrics}}
              <td>${{powerSource}}</td>
            </tr>
          `;
        }}).join('');
      tbody.innerHTML = rows;
      tbody.querySelectorAll('[data-essay-title]').forEach(node => {{
        node.addEventListener('click', () => setSelectedEssay(node.dataset.essayTitle));
      }});
    }}

    function renderMiniTable(tableId, rows, columns) {{
      const tbody = document.querySelector(`#${{tableId}} tbody`);
      tbody.innerHTML = rows.map(row => `
        <tr class="click-row" data-essay-title="${{row.title}}">
          ${{columns.map(col => {{
            const cls = col.num ? ' class="num"' : '';
            return `<td${{cls}}>${{typeof col.render === 'function' ? col.render(row) : row[col.key]}}</td>`;
          }}).join('')}}
        </tr>
      `).join('');
      tbody.querySelectorAll('[data-essay-title]').forEach(node => {{
        node.addEventListener('click', () => setSelectedEssay(node.dataset.essayTitle));
      }});
    }}

    function renderDebatePrecision() {{
      renderMetricScatter('debate-root', 'debate-legend', 'debate', 'precision', 'Debate', 'Precision');
      const rows = essays
        .slice()
        .sort((a, b) => (b.debate + b.precision) - (a.debate + a.precision) || b.debate - a.debate);
      renderMiniTable('debate-table', rows, [
        {{ key: 'title', render: row => `<strong>${{row.title}}</strong>` }},
        {{ key: 'debate', num: true }},
        {{ key: 'precision', num: true }}
      ]);
    }}

    function renderSynthesisUtility() {{
      renderMetricScatter('synthesis-root', 'synthesis-legend', 'synthesis', 'utility', 'Synthesis', 'Utility');
      const rows = essays
        .slice()
        .sort((a, b) => (b.synthesis + b.utility) - (a.synthesis + a.utility) || b.synthesis - a.synthesis);
      renderMiniTable('synthesis-table', rows, [
        {{ key: 'title', render: row => `<strong>${{row.title}}</strong>` }},
        {{ key: 'synthesis', num: true }},
        {{ key: 'utility', num: true }}
      ]);
    }}

    function renderOpeningsEndings() {{
      renderMetricScatter('opening-ending-root', 'opening-ending-legend', 'opening', 'ending', 'Opening', 'Ending');
      const rows = essays
        .slice()
        .sort((a, b) => Math.abs(b.opening - b.ending) - Math.abs(a.opening - a.ending) || b.opening - a.opening)
        .map(row => ({{
          ...row,
          gap: row.opening - row.ending
        }}));
      renderMiniTable('opening-ending-table', rows, [
        {{ key: 'title', render: row => `<strong>${{row.title}}</strong>` }},
        {{ key: 'opening', num: true }},
        {{ key: 'ending', num: true }},
        {{ key: 'gap', num: true, render: row => `${{row.gap > 0 ? '+' : ''}}${{row.gap}}` }}
      ]);
    }}

    function renderMoveMatrix() {{
      const table = document.getElementById('move-matrix');
      const thead = table.querySelector('thead');
      const tbody = table.querySelector('tbody');
      thead.innerHTML = `
        <tr>
          <th>Essay</th>
          ${{MOVE_ORDER.map(key => `<th>${{MOVE_LABELS[key]}}</th>`).join('')}}
        </tr>
      `;
      const rows = essays
        .slice()
        .sort((a, b) => b.publication_power - a.publication_power || b.traction - a.traction)
        .map(essay => `
          <tr class="click-row" data-essay-title="${{essay.title}}">
            <td><strong>${{essay.title}}</strong></td>
            ${{MOVE_ORDER.map(key => essay.moves.includes(key)
              ? `<td><span class="move-hit">●</span></td>`
              : `<td><span class="move-miss">·</span></td>`
            ).join('')}}
          </tr>
        `).join('');
      tbody.innerHTML = rows;
      tbody.querySelectorAll('[data-essay-title]').forEach(node => {{
        node.addEventListener('click', () => setSelectedEssay(node.dataset.essayTitle));
      }});
    }}

    function activateTab(target) {{
      document.querySelectorAll('.tab-btn').forEach(btn => {{
        btn.classList.toggle('active', btn.dataset.tab === target);
      }});
      document.querySelectorAll('.tab-panel').forEach(panel => {{
        panel.classList.toggle('active', panel.id === `tab-${{target}}`);
      }});
    }}

    function bindTabs() {{
      document.querySelectorAll('.tab-btn').forEach(btn => {{
        btn.addEventListener('click', () => activateTab(btn.dataset.tab));
      }});
    }}

    function renderVector() {{
      const draft = drafts[0];
      if (!draft) return;
      const root = document.getElementById('vector-root');
      const draftHead = document.getElementById('draft-head');
      const draftProblem = document.getElementById('draft-problem');
      const pullBody = document.getElementById('pull-table-body');

      draftHead.innerHTML = `
        <strong>${{draft.title}}</strong>
        <span>${{draft.one_line_identity}}</span>
        <span>current T/C ${{draft.current_position.traction}}/${{draft.current_position.craft}} → target T/C ${{draft.target_position.traction}}/${{draft.target_position.craft}}, precision ${{draft.current_position.precision}} → ${{draft.target_position.precision}}</span>
      `;
      draftProblem.textContent = draft.problem;
      pullBody.innerHTML = [
        ...draft.pulls.map(item => `
          <tr>
            <td>${{item.section}}</td>
            <td>${{item.essay}}</td>
            <td>${{item.desired_strength}}</td>
          </tr>
        `),
        ...draft.resists.map(item => `
          <tr>
            <td>Resist</td>
            <td>${{item.essay}}</td>
            <td>${{item.risk}}</td>
          </tr>
        `)
      ].join('');

      const positions = [
        {{ x: 28, y: 46, width: 190, height: 72 }},
        {{ x: 492, y: 42, width: 178, height: 72 }},
        {{ x: 26, y: 252, width: 208, height: 72 }},
        {{ x: 478, y: 252, width: 202, height: 72 }},
        {{ x: 250, y: 18, width: 190, height: 64 }}
      ];
      const nodeMap = new Map();
      draft.pulls.forEach(item => {{
        if (!nodeMap.has(item.essay)) nodeMap.set(item.essay, {{ type: 'pull', notes: [] }});
        nodeMap.get(item.essay).notes.push(item.section.toLowerCase());
      }});
      draft.resists.forEach(item => {{
        nodeMap.set(item.essay, {{ type: 'resist', notes: [item.risk] }});
      }});

      const nodes = [...nodeMap.entries()].slice(0, positions.length).map(([title, meta], idx) => {{
        const essay = essayMap.get(title);
        const pos = positions[idx];
        const cx = pos.x + pos.width / 2;
        const cy = pos.y + pos.height / 2;
        return {{
          title,
          short: essay ? shortTitle(essay) : title,
          subtitle: meta.type === 'resist'
            ? `resist: ${{meta.notes[0]}}`
            : meta.notes.join(' + '),
          type: meta.type,
          ...pos,
          cx,
          cy
        }};
      }});

      const rects = nodes.map(node => `
        <rect x="${{node.x}}" y="${{node.y}}" width="${{node.width}}" height="${{node.height}}" rx="16"
          fill="${{node.type === 'resist' ? 'rgba(184,95,61,0.08)' : 'rgba(31,107,92,0.08)'}}"
          stroke="${{node.type === 'resist' ? 'rgba(184,95,61,0.26)' : 'rgba(31,107,92,0.26)'}}"></rect>
        <text x="${{node.cx}}" y="${{node.y + 31}}" text-anchor="middle" font-size="18" font-family="var(--serif)" fill="#1f2a26">${{node.short}}</text>
        <text x="${{node.cx}}" y="${{node.y + 51}}" text-anchor="middle" font-size="12" fill="#5f6b64">${{node.subtitle}}</text>
      `).join('');

      const lines = nodes.map(node => `
        <line x1="${{node.cx}}" y1="${{node.cy}}" x2="345" y2="175"
          stroke="${{node.type === 'resist' ? '#b85f3d' : '#1f6b5c'}}"
          stroke-width="${{node.type === 'resist' ? '2.6' : '3.0'}}"
          stroke-dasharray="${{node.type === 'resist' ? '8 8' : '0'}}"
          marker-end="url(#${{node.type === 'resist' ? 'arrow-rust' : 'arrow-green'}})"></line>
      `).join('');

      root.innerHTML = `
        <svg viewBox="0 0 700 360" role="img" aria-label="Draft pull vector view">
          <defs>
            <marker id="arrow-green" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
              <path d="M0,0 L10,5 L0,10 z" fill="#1f6b5c"></path>
            </marker>
            <marker id="arrow-rust" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
              <path d="M0,0 L10,5 L0,10 z" fill="#b85f3d"></path>
            </marker>
          </defs>
          <rect x="250" y="130" width="190" height="90" rx="18" fill="rgba(31,107,92,0.10)" stroke="#1f6b5c" stroke-width="2"></rect>
          <text x="345" y="168" text-anchor="middle" font-family="var(--serif)" font-size="24" fill="#1f2a26">${{draft.title}}</text>
          <text x="345" y="194" text-anchor="middle" font-size="13" fill="#5f6b64">${{draft.one_line_identity}}</text>
          ${{rects}}
          ${{lines}}
        </svg>
      `;
    }}

    renderHero();
    bindTabs();
    renderScatter();
    renderHeatmap();
    renderVector();
    renderDebatePrecision();
    renderSynthesisUtility();
    renderOpeningsEndings();
    renderMoveMatrix();
    setSelectedEssay(selectedEssayTitle);
  </script>
</body>
</html>
"""

    OUT_PATH.write_text(html)


if __name__ == "__main__":
    main()
