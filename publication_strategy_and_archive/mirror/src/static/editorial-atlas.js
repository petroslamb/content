document.addEventListener("DOMContentLoaded", () => {
  const root = document.querySelector("[data-editorial-atlas]");
  const dataNode = document.getElementById("editorial-atlas-data");
  if (!root || !dataNode) return;

  const atlas = JSON.parse(dataNode.textContent);
  const essays = [...(atlas.essays || [])];
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
  const wholeKeys = ["traction", "craft", "debate", "precision", "synthesis", "utility"];
  const sectionKeys = [
    { key: "opening", label: "Opening" },
    { key: "thesis_lock", label: "Thesis Lock" },
    { key: "development", label: "Development" },
    { key: "borders", label: "Borders / Counterpressure" },
    { key: "ending", label: "Ending" },
    { key: "reference_handling", label: "Reference Handling" },
  ];
  const goalConfig = {
    improve_overall: {
      label: "Improve overall",
      summary: "Find nearby stronger publication objects without changing the essay's type too much.",
      targetKeys: ["traction", "craft", "precision"],
      protectedKeys: ["synthesis", "utility"],
      targetDeltas: { traction: 1, craft: 1, precision: 1 },
    },
    increase_traction: {
      label: "Increase traction",
      summary: "Push the essay toward a stronger public object without throwing away its reasoning quality.",
      targetKeys: ["traction", "debate"],
      protectedKeys: ["craft", "precision"],
      targetDeltas: { traction: 1, debate: 1, craft: 1 },
    },
    increase_precision: {
      label: "Increase precision",
      summary: "Tighten borders and concept control while preserving enough spread to stay alive publicly.",
      targetKeys: ["precision", "craft"],
      protectedKeys: ["traction", "synthesis"],
      targetDeltas: { precision: 1, craft: 1 },
    },
    increase_synthesis: {
      label: "Increase synthesis",
      summary: "Deepen integration and historical / research compression without becoming dead survey weight.",
      targetKeys: ["synthesis", "craft"],
      protectedKeys: ["traction", "precision"],
      targetDeltas: { synthesis: 1, craft: 1, utility: 1 },
    },
    increase_utility: {
      label: "Increase utility",
      summary: "Make the essay more operational and reusable without collapsing it into a thinner checklist object.",
      targetKeys: ["utility", "traction"],
      protectedKeys: ["precision", "craft"],
      targetDeltas: { utility: 1, traction: 1, precision: 1 },
    },
    patch_weak_sections: {
      label: "Patch weak sections",
      summary: "Keep the essay's basic identity but repair the slots where it is visibly underpowered.",
      targetKeys: ["craft", "precision"],
      protectedKeys: ["synthesis", "debate"],
      targetDeltas: { craft: 1, precision: 1 },
    },
  };

  let selectedEssayTitle = essayMap.has("The Transformer Attractor")
    ? "The Transformer Attractor"
    : essays[0]?.title;
  let routingCenterTitle = selectedEssayTitle;
  let routingGoalKey = "improve_overall";

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

  function roundMetric(value) {
    return Math.round(value);
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
      const offset = offsets[position % offsets.length];
      return {
        ...essay,
        plot_x: clamp(essay[xKey] + offset.x, 5.12, 9.88),
        plot_y: clamp(essay[yKey] + offset.y, 5.12, 9.88),
        label_dx: offset.dx,
        label_dy: offset.dy,
        label_anchor: offset.anchor,
      };
    });
  }

  function selectedEssay() {
    return essayMap.get(selectedEssayTitle) || essays[0];
  }

  function routingCenterEssay() {
    return essayMap.get(routingCenterTitle) || selectedEssay();
  }

  function distance(left, right, keys = wholeKeys) {
    return Math.sqrt(keys.reduce((sum, key) => sum + ((left[key] || 0) - (right[key] || 0)) ** 2, 0));
  }

  function weakestSections(essay, limit = 3) {
    return sectionKeys
      .map((slot) => ({ ...slot, value: essay[slot.key] }))
      .sort((left, right) => left.value - right.value || left.label.localeCompare(right.label))
      .slice(0, limit);
  }

  function strongestSections(essay, limit = 2) {
    return sectionKeys
      .map((slot) => ({ ...slot, value: essay[slot.key] }))
      .sort((left, right) => right.value - left.value || left.label.localeCompare(right.label))
      .slice(0, limit);
  }

  function formatWeakSections(essay) {
    return weakestSections(essay)
      .map((slot) => `${slot.label.toLowerCase()} ${slot.value}`)
      .join(", ");
  }

  function summarizeDiff(center, candidate, focusKeys, protectedKeys) {
    const focus = focusKeys
      .map((key) => ({ key, delta: (candidate[key] || 0) - (center[key] || 0) }))
      .filter((item) => item.delta !== 0)
      .sort((left, right) => Math.abs(right.delta) - Math.abs(left.delta))
      .slice(0, 2)
      .map((item) => `${item.delta > 0 ? "+" : ""}${item.delta} ${item.key}`)
      .join(", ");
    const tradeoff = protectedKeys
      .map((key) => ({ key, delta: (candidate[key] || 0) - (center[key] || 0) }))
      .filter((item) => item.delta < 0)
      .sort((left, right) => left.delta - right.delta)
      .slice(0, 1)
      .map((item) => `${item.delta} ${item.key}`)
      .join(", ");
    if (focus && tradeoff) return `${focus}; tradeoff ${tradeoff}`;
    return focus || tradeoff || "nearby profile";
  }

  function buildTargetPosition(center, goalKey) {
    const goal = goalConfig[goalKey];
    const target = { ...center };
    Object.entries(goal.targetDeltas || {}).forEach(([key, delta]) => {
      target[key] = clamp((target[key] || 0) + delta, 1, 10);
    });

    if (goalKey === "patch_weak_sections") {
      const weak = weakestSections(center);
      if (weak.some((slot) => ["opening", "thesis_lock", "ending"].includes(slot.key) && slot.value <= 7)) {
        target.traction = clamp(target.traction + 1, 1, 10);
      }
      if (weak.some((slot) => ["borders", "reference_handling"].includes(slot.key) && slot.value <= 7)) {
        target.precision = clamp(target.precision + 1, 1, 10);
      }
      if (weak.some((slot) => ["development", "reference_handling"].includes(slot.key) && slot.value <= 7)) {
        target.synthesis = clamp(target.synthesis + 1, 1, 10);
      }
    }

    return {
      traction: target.traction,
      craft: target.craft,
      debate: target.debate,
      precision: target.precision,
      synthesis: target.synthesis,
      utility: target.utility,
    };
  }

  function strongerNeighbors(center, goalKey) {
    const goal = goalConfig[goalKey];
    return essays
      .filter((essay) => essay.title !== center.title)
      .map((essay) => {
        const targetGain = goal.targetKeys.reduce((sum, key) => sum + ((essay[key] || 0) - (center[key] || 0)), 0);
        const protectedLoss = goal.protectedKeys.reduce(
          (sum, key) => sum + Math.max(0, (center[key] || 0) - (essay[key] || 0)),
          0,
        );
        const score =
          targetGain * 3 +
          ((essay.publication_power || 0) - (center.publication_power || 0)) * 1.1 -
          protectedLoss * 2.2 -
          distance(center, essay) * 0.55;
        return {
          essay,
          targetGain,
          protectedLoss,
          score,
        };
      })
      .filter((item) => item.targetGain > 0 && item.score > -1.5)
      .sort((left, right) => right.score - left.score)
      .slice(0, 2)
      .map((item, index) => ({
        relation: "Stronger neighbor",
        priority: index,
        essay: item.essay.title,
        note: summarizeDiff(center, item.essay, goal.targetKeys, goal.protectedKeys),
        shortReason: "nearby stronger object",
      }));
  }

  function sectionDonors(center) {
    const used = new Set();
    return weakestSections(center)
      .map((slot) => {
        const donor = essays
          .filter((essay) => essay.title !== center.title)
          .map((essay) => {
            const sectionGain = (essay[slot.key] || 0) - (center[slot.key] || 0);
            const score = sectionGain * 3 - distance(center, essay) * 0.35 + (essay.publication_power || 0) * 0.12;
            return { essay, sectionGain, score };
          })
          .filter((item) => item.sectionGain > 0)
          .sort((left, right) => right.score - left.score)
          .find((item) => !used.has(item.essay.title)) || null;

        if (!donor) return null;
        used.add(donor.essay.title);
        return {
          relation: "Section donor",
          priority: slot.value,
          essay: donor.essay.title,
          note: `${slot.label} ${center[slot.key]} → ${donor.essay[slot.key]}`,
          shortReason: slot.label.toLowerCase(),
        };
      })
      .filter(Boolean)
      .slice(0, 3);
  }

  function resists(center, goalKey) {
    const goal = goalConfig[goalKey];
    return essays
      .filter((essay) => essay.title !== center.title)
      .map((essay) => {
        const targetGain = goal.targetKeys.reduce((sum, key) => sum + ((essay[key] || 0) - (center[key] || 0)), 0);
        const protectedLoss = goal.protectedKeys.reduce(
          (sum, key) => sum + Math.max(0, (center[key] || 0) - (essay[key] || 0)),
          0,
        );
        const riskWeight = essay.overpull_risk ? 1 : 0;
        const score = targetGain * 0.9 + protectedLoss * 2 + distance(center, essay) * 0.35 + riskWeight;
        return { essay, targetGain, protectedLoss, score };
      })
      .filter((item) => item.targetGain > 0 && item.protectedLoss >= 1)
      .sort((left, right) => right.score - left.score)
      .slice(0, 2)
      .map((item, index) => ({
        relation: "Resist",
        priority: index,
        essay: item.essay.title,
        note: item.essay.overpull_risk || summarizeDiff(center, item.essay, goal.targetKeys, goal.protectedKeys),
        shortReason: "tempting but distorting",
      }));
  }

  function buildRoutingModel(center, goalKey) {
    const goal = goalConfig[goalKey];
    const targetPosition = buildTargetPosition(center, goalKey);
    const neighbors = strongerNeighbors(center, goalKey);
    const donors = sectionDonors(center);
    const resistNodes = resists(center, goalKey);
    const strongest = strongestSections(center).map((slot) => `${slot.label.toLowerCase()} ${slot.value}`).join(", ");
    const weakest = formatWeakSections(center);

    return {
      goal,
      targetPosition,
      neighbors,
      donors,
      resistNodes,
      summary:
        `${goal.summary} Weakest slots: ${weakest}. Current strengths: ${strongest}.`,
    };
  }

  function renderCompactDetail(targetId, essay) {
    const node = document.getElementById(targetId);
    if (!node || !essay) return;
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
    if (!essay) return;
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

  function setRoutingCenter(title) {
    if (!essayMap.has(title)) return;
    routingCenterTitle = title;
    const select = document.getElementById("atlas-routing-center");
    if (select) select.value = title;
    setSelectedEssay(title);
    renderRoutingTool();
  }

  function setRoutingGoal(goalKey) {
    if (!goalConfig[goalKey]) return;
    routingGoalKey = goalKey;
    const select = document.getElementById("atlas-routing-goal");
    if (select) select.value = goalKey;
    renderRoutingTool();
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
        const powerSource = [...pairs].sort((left, right) => right[1] - left[1])[0][0];
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
    if (!tbody) return;
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

  function renderRoutingControls() {
    const centerSelect = document.getElementById("atlas-routing-center");
    const goalSelect = document.getElementById("atlas-routing-goal");
    if (!centerSelect || !goalSelect) return;

    centerSelect.innerHTML = essays
      .slice()
      .sort((left, right) => left.title.localeCompare(right.title))
      .map((essay) => `<option value="${essay.title}">${essay.title}</option>`)
      .join("");
    centerSelect.value = routingCenterTitle;
    centerSelect.addEventListener("change", (event) => {
      setRoutingCenter(event.target.value);
    });

    goalSelect.innerHTML = Object.entries(goalConfig)
      .map(([key, goal]) => `<option value="${key}">${goal.label}</option>`)
      .join("");
    goalSelect.value = routingGoalKey;
    goalSelect.addEventListener("change", (event) => {
      setRoutingGoal(event.target.value);
    });

    const button = document.getElementById("atlas-use-selected");
    if (button) {
      button.addEventListener("click", () => {
        setRoutingCenter(selectedEssayTitle);
      });
    }
  }

  function renderRoutingTable(model) {
    const tbody = document.getElementById("atlas-pull-table-body");
    if (!tbody) return;
    const rows = [
      ...model.neighbors.map((item) => ({ ...item, kind: "neighbor" })),
      ...model.donors.map((item) => ({ ...item, kind: "donor" })),
      ...model.resistNodes.map((item) => ({ ...item, kind: "resist" })),
    ];
    tbody.innerHTML = rows.map((item) => `
      <tr class="atlas-click-row" data-essay-title="${item.essay}">
        <td><span class="atlas-route-badge atlas-route-badge--${item.kind}">${item.relation}</span></td>
        <td><strong>${item.essay}</strong></td>
        <td>${item.note}</td>
      </tr>
    `).join("");
    tbody.querySelectorAll("[data-essay-title]").forEach((node) => {
      node.addEventListener("click", () => setSelectedEssay(node.dataset.essayTitle));
    });
  }

  function renderRoutingDiagram(center, model) {
    const nodeMap = new Map();
    const addNode = (item, kind) => {
      if (!nodeMap.has(item.essay)) {
        nodeMap.set(item.essay, { kinds: new Set(), notes: [] });
      }
      nodeMap.get(item.essay).kinds.add(kind);
      nodeMap.get(item.essay).notes.push(item.shortReason || item.note);
    };
    model.neighbors.forEach((item) => addNode(item, "neighbor"));
    model.donors.forEach((item) => addNode(item, "donor"));
    model.resistNodes.forEach((item) => addNode(item, "resist"));

    const positions = {
      resist: [
        { x: 260, y: 20, width: 220, height: 66 },
        { x: 514, y: 38, width: 220, height: 66 },
      ],
      neighbor: [
        { x: 42, y: 110, width: 220, height: 72 },
        { x: 520, y: 110, width: 220, height: 72 },
      ],
      donor: [
        { x: 32, y: 302, width: 224, height: 72 },
        { x: 278, y: 328, width: 224, height: 72 },
        { x: 524, y: 302, width: 224, height: 72 },
      ],
    };

    const nodes = [];
    ["resist", "neighbor", "donor"].forEach((kind) => {
      const matching = [...nodeMap.entries()]
        .filter(([, meta]) => meta.kinds.has(kind))
        .slice(0, positions[kind].length);
      matching.forEach(([title, meta], index) => {
        const essay = essayMap.get(title);
        const pos = positions[kind][index];
        nodes.push({
          ...pos,
          kind,
          title,
          short: essay ? shortTitle(essay) : title,
          subtitle: meta.notes.slice(0, 2).join(" · "),
          cx: pos.x + pos.width / 2,
          cy: pos.y + pos.height / 2,
        });
      });
    });

    const styleMap = {
      resist: {
        fill: "rgba(184,95,61,0.08)",
        stroke: "rgba(184,95,61,0.26)",
        line: "#b85f3d",
        dash: "8 8",
        marker: "atlas-arrow-rust",
      },
      neighbor: {
        fill: "rgba(31,107,92,0.08)",
        stroke: "rgba(31,107,92,0.26)",
        line: "#1f6b5c",
        dash: "0",
        marker: "atlas-arrow-green",
      },
      donor: {
        fill: "rgba(169,119,56,0.1)",
        stroke: "rgba(169,119,56,0.32)",
        line: "#a97738",
        dash: "2 5",
        marker: "atlas-arrow-gold",
      },
    };

    const rects = nodes.map((node) => {
      const style = styleMap[node.kind];
      return `
        <g class="atlas-vector-node" data-essay-title="${node.title}">
          <rect x="${node.x}" y="${node.y}" width="${node.width}" height="${node.height}" rx="16"
            fill="${style.fill}" stroke="${style.stroke}"></rect>
          <text x="${node.cx}" y="${node.y + 29}" text-anchor="middle" font-size="18" font-family="var(--serif)" fill="#1f1a14">${node.short}</text>
          <text x="${node.cx}" y="${node.y + 49}" text-anchor="middle" font-size="12" fill="#64584a">${node.subtitle}</text>
        </g>
      `;
    }).join("");

    const lines = nodes.map((node) => {
      const style = styleMap[node.kind];
      return `
        <line x1="${node.cx}" y1="${node.cy}" x2="390" y2="220"
          stroke="${style.line}"
          stroke-width="${node.kind === "neighbor" ? "3" : "2.7"}"
          stroke-dasharray="${style.dash}"
          marker-end="url(#${style.marker})"></line>
      `;
    }).join("");

    const rootNode = document.getElementById("atlas-vector-root");
    rootNode.innerHTML = `
      <svg viewBox="0 0 780 430" role="img" aria-label="Essay routing vector view">
        <defs>
          <marker id="atlas-arrow-green" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
            <path d="M0,0 L10,5 L0,10 z" fill="#1f6b5c"></path>
          </marker>
          <marker id="atlas-arrow-rust" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
            <path d="M0,0 L10,5 L0,10 z" fill="#b85f3d"></path>
          </marker>
          <marker id="atlas-arrow-gold" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
            <path d="M0,0 L10,5 L0,10 z" fill="#a97738"></path>
          </marker>
        </defs>
        <rect x="275" y="176" width="230" height="92" rx="18" fill="rgba(31,107,92,0.10)" stroke="#1f6b5c" stroke-width="2"></rect>
        <text x="390" y="212" text-anchor="middle" font-family="var(--serif)" font-size="24" fill="#1f1a14">${center.title}</text>
        <text x="390" y="236" text-anchor="middle" font-size="13" fill="#64584a">${goalConfig[routingGoalKey].label}</text>
        <text x="390" y="256" text-anchor="middle" font-size="12" fill="#64584a">${center.identity}</text>
        ${rects}
        ${lines}
      </svg>
    `;
    rootNode.querySelectorAll(".atlas-vector-node").forEach((node) => {
      node.addEventListener("click", () => setSelectedEssay(node.dataset.essayTitle));
    });
  }

  function renderRoutingTool() {
    const center = routingCenterEssay();
    if (!center) return;
    const model = buildRoutingModel(center, routingGoalKey);
    const goal = model.goal;

    document.getElementById("atlas-draft-head").innerHTML = `
      <strong>${center.title}</strong>
      <span>${center.identity}</span>
      <span>${goal.label}: current T/C ${center.traction}/${center.craft} → target ${model.targetPosition.traction}/${model.targetPosition.craft}; precision ${center.precision} → ${model.targetPosition.precision}; utility ${center.utility} → ${model.targetPosition.utility}</span>
    `;
    document.getElementById("atlas-draft-problem").textContent = model.summary;
    renderRoutingTable(model);
    renderRoutingDiagram(center, model);
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

  function init() {
    renderScatter("atlas-scatter-root", "traction", "craft", "Traction", "Craft", essays);
    renderLegend("atlas-constellation-legend");
    renderHeatmap();
    renderRoutingControls();
    renderRoutingTool();

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
    renderMiniTable(
      "atlas-opening-ending-table",
      essays
        .slice()
        .sort((a, b) => Math.abs(b.opening - b.ending) - Math.abs(a.opening - a.ending) || b.opening - a.opening)
        .map((row) => ({ ...row, gap: row.opening - row.ending })),
      [
        { key: "title", render: (row) => `<strong>${row.title}</strong>` },
        { key: "opening", num: true },
        { key: "ending", num: true },
        { key: "gap", num: true, render: (row) => `${row.gap > 0 ? "+" : ""}${row.gap}` },
      ],
    );

    renderMoveMatrix();
    bindTabs();
    updateSelectionViews();
  }

  init();
});
