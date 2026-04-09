document.addEventListener("DOMContentLoaded", () => {
  const root = document.querySelector("[data-editorial-atlas]");
  const dataNode = document.getElementById("editorial-atlas-data");
  if (!root || !dataNode) return;

  const atlas = JSON.parse(dataNode.textContent);
  const essays = [...(atlas.essays || [])];
  const drafts = [...(atlas.drafts || [])];
  const essayMap = new Map(essays.map((essay) => [essay.title, essay]));
  const moveLabels = {
    failure_or_anomaly_cold_open: "Cold open",
    contrarian_compression: "Contrarian compression",
    coined_frame_with_borders: "Coined frame",
    scroll_map: "Scroll map",
    builder_first_doctrine: "Builder doctrine",
    historical_synthesis: "Historical synthesis",
    practical_heuristic_section: "Practical heuristic",
    falsifiable_prediction_close: "Prediction close",
    topical_narrative_hijack: "Topical hijack",
    series_packaging: "Series packaging",
    chapterized_technical_explainer: "Chapterized explainer",
    doctrine_ending: "Doctrine ending",
  };
  const moveOrder = Object.keys(moveLabels);
  let selectedEssayTitle = "The Transformer Attractor";

  function metricColor(value) {
    if (value >= 9) return "#1f6b5c";
    if (value >= 8) return "#497e68";
    if (value >= 7) return "#a97738";
    return "#b85f3d";
  }

  function confidenceStroke(confidence) {
    if (confidence === "high") return "0";
    if (confidence === "medium") return "5 3";
    return "2 3";
  }

  function confidenceOpacity(confidence) {
    if (confidence === "high") return 0.82;
    if (confidence === "medium") return 0.72;
    return 0.62;
  }

  function heatColor(value) {
    const alpha = 0.1 + ((value - 5) / 5) * 0.28;
    return `rgba(31, 107, 92, ${alpha.toFixed(3)})`;
  }

  function shortTitle(essay) {
    return essay.short_label || essay.title;
  }

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function buildPlottedEssays(source, xKey, yKey) {
    const offsets = [
      { x: 0.0, y: 0.0, dx: 12, dy: -12, anchor: "start" },
      { x: 0.16, y: 0.18, dx: 12, dy: -10, anchor: "start" },
      { x: -0.18, y: 0.16, dx: -12, dy: -10, anchor: "end" },
      { x: 0.18, y: -0.16, dx: 12, dy: 18, anchor: "start" },
      { x: -0.18, y: -0.18, dx: -12, dy: 18, anchor: "end" },
      { x: 0.28, y: 0.0, dx: 14, dy: 4, anchor: "start" },
      { x: -0.28, y: 0.0, dx: -14, dy: 4, anchor: "end" },
      { x: 0.0, y: 0.28, dx: 0, dy: -16, anchor: "middle" },
      { x: 0.0, y: -0.28, dx: 0, dy: 22, anchor: "middle" },
      { x: 0.32, y: 0.2, dx: 14, dy: -14, anchor: "start" },
      { x: -0.32, y: 0.2, dx: -14, dy: -14, anchor: "end" },
      { x: 0.32, y: -0.22, dx: 14, dy: 20, anchor: "start" },
      { x: -0.32, y: -0.22, dx: -14, dy: 20, anchor: "end" },
    ];

    const groups = new Map();
    source.forEach((essay, idx) => {
      const key = `${essay[xKey]}-${essay[yKey]}`;
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push({ essay, idx });
    });

    return source.map((essay, idx) => {
      const key = `${essay[xKey]}-${essay[yKey]}`;
      const group = groups.get(key) || [{ essay, idx }];
      const position = group.findIndex((item) => item.idx === idx);
      const o = offsets[position % offsets.length];
      return {
        ...essay,
        plot_x: clamp(essay[xKey] + o.x, 5.12, 9.88),
        plot_y: clamp(essay[yKey] + o.y, 5.12, 9.88),
        label_dx: o.dx,
        label_dy: o.dy,
        label_anchor: o.anchor,
      };
    });
  }

  const plottedEssays = buildPlottedEssays(essays, "traction", "craft");

  function selectedEssay() {
    return essayMap.get(selectedEssayTitle) || plottedEssays[0];
  }

  function renderCompactDetail(targetId, essay) {
    const node = document.getElementById(targetId);
    if (!node) return;
    node.innerHTML = `
      <h3>${shortTitle(essay)}</h3>
      <p>${essay.identity}</p>
      <div class="atlas-compact-grid">
        <div class="atlas-compact-box"><strong>${essay.debate}</strong><span>debate</span></div>
        <div class="atlas-compact-box"><strong>${essay.precision}</strong><span>precision</span></div>
        <div class="atlas-compact-box"><strong>${essay.confidence}</strong><span>confidence</span></div>
      </div>
    `;
  }

  function renderDetail(essay) {
    document.getElementById("atlas-detail-title").textContent = essay.title;
    document.getElementById("atlas-detail-subtitle").textContent = `${essay.date} | ${essay.words} words | confidence: ${essay.confidence}`;
    document.getElementById("atlas-detail-traction").textContent = essay.traction;
    document.getElementById("atlas-detail-craft").textContent = essay.craft;
    document.getElementById("atlas-detail-power").textContent = essay.publication_power;
    document.getElementById("atlas-detail-identity").textContent = essay.identity;
    document.getElementById("atlas-detail-signature").textContent = essay.signature;
    document.getElementById("atlas-detail-risk").textContent = essay.overpull_risk;
    document.getElementById("atlas-detail-sections").textContent =
      `opening ${essay.opening}, thesis ${essay.thesis_lock}, development ${essay.development}, borders ${essay.borders}, ending ${essay.ending}, refs ${essay.reference_handling}`;
    document.getElementById("atlas-detail-chips").innerHTML = `
      <span class="atlas-chip">${essay.identity}</span>
      <span class="atlas-chip">traction ${essay.traction}</span>
      <span class="atlas-chip">craft ${essay.craft}</span>
      <span class="atlas-chip">confidence ${essay.confidence}</span>
    `;
  }

  function updateSelectionViews() {
    const essay = selectedEssay();
    renderDetail(essay);
    renderCompactDetail("atlas-debate-detail", essay);
    renderCompactDetail("atlas-synthesis-detail", essay);
    renderCompactDetail("atlas-openings-detail", essay);
    renderCompactDetail("atlas-moves-detail", essay);
    document.querySelectorAll("[data-essay-title]").forEach((node) => {
      node.classList.toggle("selected-row", node.dataset.essayTitle === essay.title);
    });
  }

  function setSelectedEssay(title) {
    if (!essayMap.has(title)) return;
    selectedEssayTitle = title;
    updateSelectionViews();
  }

  function renderLegend(targetId) {
    const node = document.getElementById(targetId);
    if (!node) return;
    node.innerHTML = `
      <span><span class="atlas-legend-dot" style="background:${metricColor(9)}"></span>power 9-10</span>
      <span><span class="atlas-legend-dot" style="background:${metricColor(8)}"></span>power 8</span>
      <span><span class="atlas-legend-dot" style="background:${metricColor(7)}"></span>power 7</span>
      <span><span class="atlas-legend-dot" style="background:${metricColor(6)}"></span>power 6</span>
      <span>solid = high confidence, dashed = lower confidence</span>
    `;
  }

  function renderScatter(rootId, xKey, yKey, xLabel, yLabel, source = essays) {
    const rootNode = document.getElementById(rootId);
    if (!rootNode) return;
    const series = buildPlottedEssays(source, xKey, yKey);
    const width = 900;
    const height = 460;
    const margin = { top: 20, right: 28, bottom: 56, left: 58 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;
    const scaleX = (value) => margin.left + ((value - 5) / 5) * innerWidth;
    const scaleY = (value) => margin.top + innerHeight - ((value - 5) / 5) * innerHeight;

    let grid = "";
    let labels = "";
    for (let i = 5; i <= 10; i += 1) {
      const x = scaleX(i);
      const y = scaleY(i);
      grid += `<line x1="${x}" y1="${margin.top}" x2="${x}" y2="${margin.top + innerHeight}" stroke="rgba(31,42,38,0.08)" />`;
      grid += `<line x1="${margin.left}" y1="${y}" x2="${margin.left + innerWidth}" y2="${y}" stroke="rgba(31,42,38,0.08)" />`;
      labels += `<text x="${x}" y="${height - 18}" font-size="12" text-anchor="middle" fill="#64584a">${i}</text>`;
      labels += `<text x="${margin.left - 18}" y="${y + 4}" font-size="12" text-anchor="middle" fill="#64584a">${i}</text>`;
    }

    const points = series.map((essay) => {
      const x = scaleX(essay.plot_x);
      const y = scaleY(essay.plot_y);
      const r = 5 + essay.publication_power * 0.85;
      const labelX = x + essay.label_dx;
      const labelY = y + essay.label_dy;
      return `
        <g class="atlas-scatter-point" data-essay-title="${essay.title}" style="cursor:pointer">
          <circle cx="${x}" cy="${y}" r="${r}" fill="${metricColor(essay.publication_power)}" fill-opacity="${confidenceOpacity(essay.confidence)}" stroke="#fff8f0" stroke-width="2" stroke-dasharray="${confidenceStroke(essay.confidence)}">
            <title>${essay.title}</title>
          </circle>
          <line x1="${x}" y1="${y}" x2="${labelX}" y2="${labelY}" stroke="rgba(31,42,38,0.14)" stroke-width="1" />
          <text x="${labelX}" y="${labelY}" font-size="10.5" font-weight="600" text-anchor="${essay.label_anchor}" fill="#1f1a14" paint-order="stroke" stroke="rgba(255,251,245,0.92)" stroke-width="4" stroke-linejoin="round">${shortTitle(essay)}</text>
        </g>
      `;
    }).join("");

    rootNode.innerHTML = `
      <svg viewBox="0 0 ${width} ${height}" role="img" aria-label="${xLabel} by ${yLabel}">
        <rect x="0" y="0" width="${width}" height="${height}" rx="18" fill="rgba(255,255,255,0.18)"></rect>
        ${grid}
        <line x1="${margin.left}" y1="${margin.top + innerHeight}" x2="${margin.left + innerWidth}" y2="${margin.top + innerHeight}" stroke="#1f1a14" stroke-width="1.5" />
        <line x1="${margin.left}" y1="${margin.top}" x2="${margin.left}" y2="${margin.top + innerHeight}" stroke="#1f1a14" stroke-width="1.5" />
        ${labels}
        <text x="${margin.left + innerWidth / 2}" y="${height - 4}" font-size="13" text-anchor="middle" fill="#1f1a14">${xLabel}</text>
        <text x="18" y="${margin.top + innerHeight / 2}" font-size="13" text-anchor="middle" fill="#1f1a14" transform="rotate(-90 18 ${margin.top + innerHeight / 2})">${yLabel}</text>
        ${points}
      </svg>
    `;

    rootNode.querySelectorAll(".atlas-scatter-point").forEach((node) => {
      node.addEventListener("click", () => setSelectedEssay(node.dataset.essayTitle));
    });
  }

  function renderHeatmap() {
    const tbody = document.querySelector("#atlas-heatmap-table tbody");
    const rows = essays
      .slice()
      .sort((a, b) => b.publication_power - a.publication_power || b.traction - a.traction)
      .map((essay) => {
        const metrics = ["opening", "thesis_lock", "development", "borders", "ending", "reference_handling"]
          .map((key) => `<td class="num"><span class="atlas-heat-cell" style="background:${heatColor(essay[key])}">${essay[key]}</span></td>`)
          .join("");
        const pairs = [
          ["opening", essay.opening],
          ["thesis", essay.thesis_lock],
          ["development", essay.development],
          ["borders", essay.borders],
          ["ending", essay.ending],
          ["refs", essay.reference_handling],
        ];
        const powerSource = [...pairs].sort((a, b) => b[1] - a[1])[0][0];
        return `
          <tr class="atlas-click-row" data-essay-title="${essay.title}">
            <td><strong>${essay.title}</strong></td>
            ${metrics}
            <td>${powerSource}</td>
          </tr>
        `;
      })
      .join("");
    tbody.innerHTML = rows;
    tbody.querySelectorAll("[data-essay-title]").forEach((node) => {
      node.addEventListener("click", () => setSelectedEssay(node.dataset.essayTitle));
    });
  }

  function renderMiniTable(tableId, rows, columns) {
    const tbody = document.querySelector(`#${tableId} tbody`);
    tbody.innerHTML = rows.map((row) => `
      <tr class="atlas-click-row" data-essay-title="${row.title}">
        ${columns.map((col) => `<td${col.num ? ' class="num"' : ""}>${typeof col.render === "function" ? col.render(row) : row[col.key]}</td>`).join("")}
      </tr>
    `).join("");
    tbody.querySelectorAll("[data-essay-title]").forEach((node) => {
      node.addEventListener("click", () => setSelectedEssay(node.dataset.essayTitle));
    });
  }

  function renderMoveMatrix() {
    const table = document.getElementById("atlas-move-matrix");
    const thead = table.querySelector("thead");
    const tbody = table.querySelector("tbody");
    thead.innerHTML = `<tr><th>Essay</th>${moveOrder.map((key) => `<th>${moveLabels[key]}</th>`).join("")}</tr>`;
    tbody.innerHTML = essays
      .slice()
      .sort((a, b) => b.publication_power - a.publication_power || b.traction - a.traction)
      .map((essay) => `
        <tr class="atlas-click-row" data-essay-title="${essay.title}">
          <td><strong>${essay.title}</strong></td>
          ${moveOrder.map((key) => essay.moves.includes(key)
            ? `<td><span class="atlas-move-hit">●</span></td>`
            : `<td><span class="atlas-move-miss">·</span></td>`).join("")}
        </tr>
      `).join("");
    tbody.querySelectorAll("[data-essay-title]").forEach((node) => {
      node.addEventListener("click", () => setSelectedEssay(node.dataset.essayTitle));
    });
  }

  function bindTabs() {
    document.querySelectorAll(".atlas-tab-btn").forEach((button) => {
      button.addEventListener("click", () => {
        const target = button.dataset.tab;
        document.querySelectorAll(".atlas-tab-btn").forEach((node) => {
          node.classList.toggle("active", node.dataset.tab === target);
        });
        document.querySelectorAll(".atlas-tab-panel").forEach((panel) => {
          panel.classList.toggle("active", panel.id === `atlas-tab-${target}`);
        });
      });
    });
  }

  function renderVector() {
    const draft = drafts[0];
    if (!draft) return;
    document.getElementById("atlas-draft-head").innerHTML = `
      <strong>${draft.title}</strong>
      <span>${draft.one_line_identity}</span>
      <span>current T/C ${draft.current_position.traction}/${draft.current_position.craft} → target T/C ${draft.target_position.traction}/${draft.target_position.craft}, precision ${draft.current_position.precision} → ${draft.target_position.precision}</span>
    `;
    document.getElementById("atlas-draft-problem").textContent = draft.problem;
    document.getElementById("atlas-pull-table-body").innerHTML = [
      ...draft.pulls.map((item) => `<tr><td>${item.section}</td><td>${item.essay}</td><td>${item.desired_strength}</td></tr>`),
      ...draft.resists.map((item) => `<tr><td>Resist</td><td>${item.essay}</td><td>${item.risk}</td></tr>`),
    ].join("");

    const positions = [
      { x: 28, y: 46, width: 190, height: 72 },
      { x: 492, y: 42, width: 178, height: 72 },
      { x: 26, y: 252, width: 208, height: 72 },
      { x: 478, y: 252, width: 202, height: 72 },
      { x: 250, y: 18, width: 190, height: 64 },
    ];
    const nodeMap = new Map();
    draft.pulls.forEach((item) => {
      if (!nodeMap.has(item.essay)) nodeMap.set(item.essay, { type: "pull", notes: [] });
      nodeMap.get(item.essay).notes.push(item.section.toLowerCase());
    });
    draft.resists.forEach((item) => nodeMap.set(item.essay, { type: "resist", notes: [item.risk] }));
    const nodes = [...nodeMap.entries()].slice(0, positions.length).map(([title, meta], idx) => {
      const essay = essayMap.get(title);
      const pos = positions[idx];
      return {
        ...pos,
        title,
        short: essay ? shortTitle(essay) : title,
        subtitle: meta.type === "resist" ? `resist: ${meta.notes[0]}` : meta.notes.join(" + "),
        type: meta.type,
        cx: pos.x + pos.width / 2,
        cy: pos.y + pos.height / 2,
      };
    });
    const rects = nodes.map((node) => `
      <rect x="${node.x}" y="${node.y}" width="${node.width}" height="${node.height}" rx="16"
        fill="${node.type === "resist" ? "rgba(184,95,61,0.08)" : "rgba(31,107,92,0.08)"}"
        stroke="${node.type === "resist" ? "rgba(184,95,61,0.26)" : "rgba(31,107,92,0.26)"}"></rect>
      <text x="${node.cx}" y="${node.y + 31}" text-anchor="middle" font-size="18" font-family="var(--serif)" fill="#1f1a14">${node.short}</text>
      <text x="${node.cx}" y="${node.y + 51}" text-anchor="middle" font-size="12" fill="#64584a">${node.subtitle}</text>
    `).join("");
    const lines = nodes.map((node) => `
      <line x1="${node.cx}" y1="${node.cy}" x2="345" y2="175"
        stroke="${node.type === "resist" ? "#b85f3d" : "#1f6b5c"}"
        stroke-width="${node.type === "resist" ? "2.6" : "3.0"}"
        stroke-dasharray="${node.type === "resist" ? "8 8" : "0"}"
        marker-end="url(#${node.type === "resist" ? "atlas-arrow-rust" : "atlas-arrow-green"})"></line>
    `).join("");
    document.getElementById("atlas-vector-root").innerHTML = `
      <svg viewBox="0 0 700 360" role="img" aria-label="Draft pull vector view">
        <defs>
          <marker id="atlas-arrow-green" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
            <path d="M0,0 L10,5 L0,10 z" fill="#1f6b5c"></path>
          </marker>
          <marker id="atlas-arrow-rust" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
            <path d="M0,0 L10,5 L0,10 z" fill="#b85f3d"></path>
          </marker>
        </defs>
        <rect x="250" y="130" width="190" height="90" rx="18" fill="rgba(31,107,92,0.10)" stroke="#1f6b5c" stroke-width="2"></rect>
        <text x="345" y="168" text-anchor="middle" font-family="var(--serif)" font-size="24" fill="#1f1a14">${draft.title}</text>
        <text x="345" y="194" text-anchor="middle" font-size="13" fill="#64584a">${draft.one_line_identity}</text>
        ${rects}
        ${lines}
      </svg>
    `;
  }

  function init() {
    renderScatter("atlas-scatter-root", "traction", "craft", "Traction", "Craft", essays);
    renderLegend("atlas-constellation-legend");
    renderHeatmap();
    renderVector();

    renderScatter("atlas-debate-root", "debate", "precision", "Debate", "Precision", essays);
    renderLegend("atlas-debate-legend");
    renderMiniTable("atlas-debate-table", essays.slice().sort((a, b) => (b.debate + b.precision) - (a.debate + a.precision) || b.debate - a.debate), [
      { key: "title", render: (row) => `<strong>${row.title}</strong>` },
      { key: "debate", num: true },
      { key: "precision", num: true },
    ]);

    renderScatter("atlas-synthesis-root", "synthesis", "utility", "Synthesis", "Utility", essays);
    renderLegend("atlas-synthesis-legend");
    renderMiniTable("atlas-synthesis-table", essays.slice().sort((a, b) => (b.synthesis + b.utility) - (a.synthesis + a.utility) || b.synthesis - a.synthesis), [
      { key: "title", render: (row) => `<strong>${row.title}</strong>` },
      { key: "synthesis", num: true },
      { key: "utility", num: true },
    ]);

    renderScatter("atlas-opening-ending-root", "opening", "ending", "Opening", "Ending", essays);
    renderLegend("atlas-opening-ending-legend");
    renderMiniTable("atlas-opening-ending-table", essays.slice().sort((a, b) => Math.abs(b.opening - b.ending) - Math.abs(a.opening - a.ending) || b.opening - a.opening).map((row) => ({ ...row, gap: row.opening - row.ending })), [
      { key: "title", render: (row) => `<strong>${row.title}</strong>` },
      { key: "opening", num: true },
      { key: "ending", num: true },
      { key: "gap", num: true, render: (row) => `${row.gap > 0 ? "+" : ""}${row.gap}` },
    ]);

    renderMoveMatrix();
    bindTabs();
    setSelectedEssay(selectedEssayTitle);
  }

  init();
});
