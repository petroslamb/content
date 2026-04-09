document.addEventListener("DOMContentLoaded", () => {
  const root = document.querySelector("[data-editorial-atlas]");
  const dataNode = document.getElementById("editorial-atlas-data");
  if (!root || !dataNode) return;

  const atlas = JSON.parse(dataNode.textContent);
  const models = atlas.models || {};
  
  // State variables that change per model
  let essays = [];
  let essayMap = new Map();
  let selectedEssayTitle = "";
  let routingCenterTitle = "";

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
  const moveCodes = {
    failure_or_anomaly_cold_open: "CO",
    contrarian_compression: "CC",
    coined_frame_with_borders: "CF",
    scroll_map: "SM",
    builder_first_doctrine: "BD",
    historical_synthesis: "HS",
    practical_heuristic_section: "PH",
    falsifiable_prediction_close: "PC",
    topical_narrative_hijack: "TH",
    series_packaging: "SP",
    chapterized_technical_explainer: "CE",
    doctrine_ending: "DE",
  };
  const moveDescriptions = {
    failure_or_anomaly_cold_open: "Opens by surfacing a failure, anomaly, or surprising tension before explanation.",
    contrarian_compression: "States a sharp contrarian claim in a compressed, portable form early in the piece.",
    coined_frame_with_borders: "Introduces a named concept or frame and then defines its boundaries clearly.",
    scroll_map: "Gives the reader a visible roadmap of the argument so the essay feels navigable while reading.",
    builder_first_doctrine: "Translates the argument into advice or doctrine aimed at builders and operators.",
    historical_synthesis: "Compresses several papers, periods, or strands of work into one integrated line of argument.",
    practical_heuristic_section: "Includes a concrete heuristic, filter, or scoring rule that a reader can reuse.",
    falsifiable_prediction_close: "Ends with a prediction or testable claim that sharpens the thesis.",
    topical_narrative_hijack: "Uses a current event, trend, or public object as the entry point into the deeper argument.",
    series_packaging: "Clearly frames the piece as part of a larger sequence, package, or recurring structure.",
    chapterized_technical_explainer: "Organizes the piece as a staged explainer with chapter-like progression.",
    doctrine_ending: "Closes with a takeaway doctrine or operating rule rather than only summary.",
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

  const tooltipNode = document.getElementById("atlas-tooltip");

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

  function essayMetricSummary(essay) {
    return `${essay.title}. Traction ${essay.traction}, craft ${essay.craft}, publication power ${essay.publication_power}, debate ${essay.debate}, precision ${essay.precision}, synthesis ${essay.synthesis}, utility ${essay.utility}.`;
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

  function summarizeDiff(center, candidate, focusKeys = ["traction", "craft", "precision"], protectedKeys = ["synthesis", "utility"]) {
    const focus = focusKeys
      .map((key) => ({ key, delta: (candidate[key] || 0) - (center[key] || 0) }))
      .filter((item) => item.delta > 0)
      .sort((left, right) => right.delta - left.delta)
      .slice(0, 2)
      .map((item) => `+${item.delta} ${item.key}`)
      .join(", ");
    const tradeoff = protectedKeys
      .map((key) => ({ key, delta: (candidate[key] || 0) - (center[key] || 0) }))
      .filter((item) => item.delta < 0)
      .sort((left, right) => left.delta - right.delta)
      .slice(0, 1)
      .map((item) => `${item.delta} ${item.key}`)
      .join(", ");
    if (focus && tradeoff) return `${focus}; watch ${tradeoff}`;
    return focus || tradeoff || "nearby profile";
  }

  function strongerNeighbors(center) {
    return essays
      .filter((essay) => essay.title !== center.title)
      .map((essay) => {
        const targetGain =
          Math.max(0, (essay.traction || 0) - (center.traction || 0)) +
          Math.max(0, (essay.craft || 0) - (center.craft || 0)) +
          Math.max(0, (essay.precision || 0) - (center.precision || 0));
        const protectedLoss =
          Math.max(0, (center.synthesis || 0) - (essay.synthesis || 0)) +
          Math.max(0, (center.utility || 0) - (essay.utility || 0));
        const score =
          targetGain * 2.8 +
          ((essay.publication_power || 0) - (center.publication_power || 0)) -
          protectedLoss * 1.7 -
          distance(center, essay) * 0.75;
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
        relation: "Stronger essay",
        priority: index,
        essay: item.essay.title,
        note: summarizeDiff(center, item.essay),
        shortReason: "nearby stronger",
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
          relation: "Slot donor",
          priority: slot.value,
          essay: donor.essay.title,
          note: `${slot.label} ${center[slot.key]} → ${donor.essay[slot.key]}`,
          shortReason: slot.label,
        };
      })
      .filter(Boolean)
      .slice(0, 3);
  }

  function riskNotes(center, neighbors, donors) {
    const candidateTitles = new Set([
      ...neighbors.map((item) => item.essay),
      ...donors.map((item) => item.essay),
    ]);

    return essays
      .filter((essay) => essay.title !== center.title && candidateTitles.has(essay.title) && essay.overpull_risk)
      .map((essay) => {
        const similarity = distance(center, essay);
        const temptation =
          Math.max(0, (essay.traction || 0) - (center.traction || 0)) +
          Math.max(0, (essay.craft || 0) - (center.craft || 0)) +
          Math.max(0, (essay.publication_power || 0) - (center.publication_power || 0));
        return { essay, score: temptation - similarity * 0.25 };
      })
      .sort((left, right) => right.score - left.score)
      .slice(0, 2)
      .map((item, index) => ({
        relation: "Risk",
        priority: index,
        essay: item.essay.title,
        note: item.essay.overpull_risk,
        shortReason: "over-copy risk",
      }));
  }

  function buildImprovementModel(center) {
    const neighbors = strongerNeighbors(center);
    const donors = sectionDonors(center);
    const risks = riskNotes(center, neighbors, donors);
    const strongest = strongestSections(center).map((slot) => `${slot.label.toLowerCase()} ${slot.value}`).join(", ");
    const weakest = formatWeakSections(center);

    return {
      neighbors,
      donors,
      risks,
      summary: `Weakest slots: ${weakest}. Current strengths: ${strongest}.`,
    };
  }

  function renderCompactDetail(targetId, essay) {
    const node = document.getElementById(targetId);
    if (!node || !essay) return;
    node.innerHTML = `
      <h3>${shortTitle(essay)}</h3>
      <p>${essay.identity}</p>
      <div class="atlas-compact-grid">
        <div class="atlas-compact-box atlas-tooltip-target" data-tooltip="Debate ${essay.debate}: how naturally this essay invites public argument, reaction, or discussion."><strong>${essay.debate}</strong><span>debate</span></div>
        <div class="atlas-compact-box atlas-tooltip-target" data-tooltip="Precision ${essay.precision}: how clearly this essay defines borders, scope, and concept control."><strong>${essay.precision}</strong><span>precision</span></div>
        <div class="atlas-compact-box atlas-tooltip-target" data-tooltip="Confidence ${essay.confidence}: how directly and deeply this essay was read during the scoring pass."><strong>${essay.confidence}</strong><span>confidence</span></div>
      </div>
    `;
  }

  function compareRead(essay) {
    const statements = [];
    if (essay.debate >= 8 && essay.precision >= 8) {
      statements.push("balanced between public tension and conceptual control");
    } else if (essay.debate > essay.precision) {
      statements.push("tilts toward public argument more than conceptual discipline");
    } else if (essay.precision > essay.debate) {
      statements.push("tilts toward conceptual discipline more than public argument");
    }

    if (essay.synthesis >= essay.utility) {
      statements.push("leans more toward synthesis than immediate operator utility");
    } else {
      statements.push("leans more toward operator use than synthesis density");
    }

    const openingGap = essay.opening - essay.ending;
    if (openingGap >= 2) {
      statements.push("is more ignition-heavy than landing-heavy");
    } else if (openingGap <= -2) {
      statements.push("lands harder than it opens");
    } else {
      statements.push("has a relatively balanced opening and ending profile");
    }

    return statements.join("; ");
  }

  function renderComparePanel(essay) {
    renderCompactDetail("atlas-compare-detail", essay);
    const debateNode = document.getElementById("atlas-compare-debate");
    const synthesisNode = document.getElementById("atlas-compare-synthesis");
    const openingNode = document.getElementById("atlas-compare-opening");
    const readNode = document.getElementById("atlas-compare-read");
    if (!debateNode || !synthesisNode || !openingNode || !readNode) return;

    debateNode.textContent = `debate ${essay.debate}, precision ${essay.precision}`;
    synthesisNode.textContent = `synthesis ${essay.synthesis}, utility ${essay.utility}`;
    openingNode.textContent = `opening ${essay.opening}, ending ${essay.ending}, gap ${essay.opening - essay.ending > 0 ? "+" : ""}${essay.opening - essay.ending}`;
    readNode.textContent = compareRead(essay);
    debateNode.classList.add("atlas-tooltip-target");
    synthesisNode.classList.add("atlas-tooltip-target");
    openingNode.classList.add("atlas-tooltip-target");
    readNode.classList.add("atlas-tooltip-target");
    debateNode.dataset.tooltip = `Debate ${essay.debate}, precision ${essay.precision}. This view shows how much the essay trades public argument for conceptual control.`;
    synthesisNode.dataset.tooltip = `Synthesis ${essay.synthesis}, utility ${essay.utility}. This view shows whether the essay behaves more like an archive anchor or an operator-facing object.`;
    openingNode.dataset.tooltip = `Opening ${essay.opening}, ending ${essay.ending}. Positive gap means the essay opens stronger than it lands; negative gap means the close is stronger than the ignition.`;
    readNode.dataset.tooltip = compareRead(essay);
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
      <span class="atlas-chip atlas-tooltip-target" data-tooltip="Editorial identity: ${essay.identity}.">${essay.identity}</span>
      <span class="atlas-chip atlas-tooltip-target" data-tooltip="Traction ${essay.traction}: how well this essay works as a public object.">traction ${essay.traction}</span>
      <span class="atlas-chip atlas-tooltip-target" data-tooltip="Craft ${essay.craft}: how strong this essay is as prose and essay architecture.">craft ${essay.craft}</span>
      <span class="atlas-chip atlas-tooltip-target" data-tooltip="Confidence ${essay.confidence}: how stable this score is within the current atlas pass.">confidence ${essay.confidence}</span>
    `;
  }

  function updateSelectionViews() {
    const essay = selectedEssay();
    renderDetail(essay);
    renderComparePanel(essay);
    renderCompactDetail("atlas-moves-detail", essay);
    document.querySelectorAll("[data-essay-title]").forEach((node) => {
      node.classList.toggle("selected-row", node.dataset.essayTitle === essay.title);
    });
    bindTooltips();
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
        <g class="atlas-scatter-point atlas-tooltip-target" data-essay-title="${essay.title}" data-tooltip="${essayMetricSummary(essay)} ${xLabel} ${essay[xKey]}, ${yLabel} ${essay[yKey]}." style="cursor:pointer">
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
    bindTooltips();
  }

  function renderHeatmap() {
    const tbody = document.querySelector("#atlas-heatmap-table tbody");
    const rows = essays
      .slice()
      .sort((a, b) => b.publication_power - a.publication_power || b.traction - a.traction)
      .map((essay) => {
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
            ${["opening", "thesis_lock", "development", "borders", "ending", "reference_handling"]
              .map((key) => `<td class="num"><span class="atlas-heat-cell atlas-tooltip-target" data-tooltip="${essay.title}: ${key.replace(/_/g, " ")} score ${essay[key]}.">${essay[key]}</span></td>`)
              .join("")}
            <td><span class="atlas-tooltip-target" data-tooltip="${essay.title}: strongest section slot is ${powerSource}.">${powerSource}</span></td>
          </tr>
        `;
      })
      .join("");
    tbody.innerHTML = rows;
    tbody.querySelectorAll("[data-essay-title]").forEach((node) => {
      node.addEventListener("click", () => setSelectedEssay(node.dataset.essayTitle));
    });
    bindTooltips();
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
    bindTooltips();
  }

  function renderMoveMatrix() {
    const keyNode = document.getElementById("atlas-move-key");
    const table = document.getElementById("atlas-move-matrix");
    const thead = table.querySelector("thead");
    const tbody = table.querySelector("tbody");
    if (keyNode) {
      keyNode.innerHTML = moveOrder
        .map((key) => `<span class="atlas-move-key-item atlas-tooltip-target" data-tooltip="${moveLabels[key]}: ${moveDescriptions[key]}"><span class="atlas-move-key-code">${moveCodes[key]}</span><span>${moveLabels[key]}</span></span>`)
        .join("");
    }
    thead.innerHTML = `<tr><th>Essay</th>${moveOrder.map((key) => `<th class="atlas-tooltip-target" data-tooltip="${moveLabels[key]}: ${moveDescriptions[key]}">${moveCodes[key]}</th>`).join("")}</tr>`;
    tbody.innerHTML = essays
      .slice()
      .sort((a, b) => b.publication_power - a.publication_power || b.traction - a.traction)
      .map((essay) => `
        <tr class="atlas-click-row" data-essay-title="${essay.title}">
          <td><strong>${essay.title}</strong></td>
          ${moveOrder.map((key) => essay.moves.includes(key)
            ? `<td class="atlas-tooltip-target" data-tooltip="${moveLabels[key]}: ${moveDescriptions[key]}"><span class="atlas-move-hit">●</span></td>`
            : `<td class="atlas-tooltip-target" data-tooltip="${moveLabels[key]}: ${moveDescriptions[key]}"><span class="atlas-move-miss">·</span></td>`).join("")}
        </tr>
      `).join("");
    tbody.querySelectorAll("[data-essay-title]").forEach((node) => {
      node.addEventListener("click", () => setSelectedEssay(node.dataset.essayTitle));
    });
    bindTooltips();
  }

  function bindTooltips() {
    if (!tooltipNode) return;
    const show = (event) => {
      const target = event.currentTarget;
      const text = target.dataset.tooltip;
      if (!text) return;
      tooltipNode.textContent = text;
      tooltipNode.classList.add("visible");
      tooltipNode.setAttribute("aria-hidden", "false");
      moveTooltip(event);
    };
    const hide = () => {
      tooltipNode.classList.remove("visible");
      tooltipNode.setAttribute("aria-hidden", "true");
    };
    document.querySelectorAll(".atlas-tooltip-target").forEach((node) => {
      if (node.dataset.tooltipBound === "true") return;
      node.dataset.tooltipBound = "true";
      node.addEventListener("mouseenter", show);
      node.addEventListener("mouseleave", hide);
      node.addEventListener("mousemove", moveTooltip);
      node.addEventListener("focus", show);
      node.addEventListener("blur", hide);
    });
  }

  function moveTooltip(event) {
    if (!tooltipNode || !tooltipNode.classList.contains("visible")) return;
    const offset = 14;
    const width = tooltipNode.offsetWidth || 220;
    const height = tooltipNode.offsetHeight || 48;
    const maxX = window.innerWidth - width - 12;
    const maxY = window.innerHeight - height - 12;
    const x = Math.min(event.clientX + offset, maxX);
    const y = Math.min(event.clientY + offset, maxY);
    tooltipNode.style.left = `${Math.max(12, x)}px`;
    tooltipNode.style.top = `${Math.max(12, y)}px`;
  }

  function renderRoutingControls() {
    const centerSelect = document.getElementById("atlas-routing-center");
    if (!centerSelect) return;

    centerSelect.innerHTML = essays
      .slice()
      .sort((left, right) => left.title.localeCompare(right.title))
      .map((essay) => `<option value="${essay.title}">${essay.title}</option>`)
      .join("");
    centerSelect.value = routingCenterTitle;
    centerSelect.addEventListener("change", (event) => {
      setRoutingCenter(event.target.value);
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
      ...model.risks.map((item) => ({ ...item, kind: "risk" })),
    ];
    tbody.innerHTML = rows.map((item) => `
      <tr class="atlas-click-row atlas-tooltip-target" data-essay-title="${item.essay}" data-tooltip="${item.relation}: ${item.essay}. ${item.note}">
        <td><span class="atlas-route-badge atlas-route-badge--${item.kind}">${item.relation}</span></td>
        <td><strong>${item.essay}</strong></td>
        <td>${item.note}</td>
      </tr>
    `).join("");
    tbody.querySelectorAll("[data-essay-title]").forEach((node) => {
      node.addEventListener("click", () => setSelectedEssay(node.dataset.essayTitle));
    });
    bindTooltips();
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
    model.risks.forEach((item) => addNode(item, "risk"));

    const positions = {
      risk: [
        { x: 272, y: 20, width: 236, height: 66 },
        { x: 518, y: 36, width: 236, height: 66 },
      ],
      neighbor: [
        { x: 36, y: 118, width: 228, height: 76 },
        { x: 518, y: 118, width: 228, height: 76 },
      ],
      donor: [
        { x: 28, y: 310, width: 230, height: 76 },
        { x: 275, y: 334, width: 230, height: 76 },
        { x: 522, y: 310, width: 230, height: 76 },
      ],
    };

    const nodes = [];
    ["risk", "neighbor", "donor"].forEach((kind) => {
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
      risk: {
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
      <svg viewBox="0 0 780 430" role="img" aria-label="Essay improvement panel">
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
        <text x="390" y="236" text-anchor="middle" font-size="13" fill="#64584a">weak slots, donors, stronger essays, risks</text>
        <text x="390" y="256" text-anchor="middle" font-size="12" fill="#64584a">${center.identity}</text>
        ${rects}
        ${lines}
      </svg>
    `;
    rootNode.querySelectorAll(".atlas-vector-node").forEach((node) => {
      node.addEventListener("click", () => setSelectedEssay(node.dataset.essayTitle));
      const match = nodes.find((item) => item.title === node.dataset.essayTitle);
      if (match) {
        node.classList.add("atlas-tooltip-target");
        node.dataset.tooltip = `${match.short}: ${match.subtitle}`;
      }
    });
    bindTooltips();
  }

  function renderRoutingTool() {
    const center = routingCenterEssay();
    if (!center) return;
    const model = buildImprovementModel(center);
    const strongerList = model.neighbors.map((item) => shortTitle(essayMap.get(item.essay) || { title: item.essay })).join(", ");
    const donorList = model.donors.map((item) => item.shortReason).join(", ");

    document.getElementById("atlas-draft-head").innerHTML = `
      <strong>${center.title}</strong>
      <span>${center.identity}</span>
      <span>traction/craft ${center.traction}/${center.craft}, precision ${center.precision}, synthesis ${center.synthesis}, utility ${center.utility}</span>
    `;
    document.getElementById("atlas-draft-problem").textContent =
      `${model.summary} Best donor slots: ${donorList || "none identified"}. Closest stronger essays: ${strongerList || "none identified"}.`;
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

  function bindSubtabs() {
    document.querySelectorAll(".atlas-subtab-btn").forEach((button) => {
      button.addEventListener("click", () => {
        const target = button.dataset.subtab;
        document.querySelectorAll(".atlas-subtab-btn").forEach((node) => {
          node.classList.toggle("active", node.dataset.subtab === target);
        });
        document.querySelectorAll(".atlas-subtab-panel").forEach((panel) => {
          panel.classList.toggle("active", panel.id === `atlas-subtab-${target}`);
        });
      });
    });
  }

  function loadModel(modelId) {
    const model = models[modelId];
    if (!model) return;

    // Update state
    essays = [...(model.essays || [])];
    essayMap = new Map(essays.map((essay) => [essay.title, essay]));
    
    // Set default selections for this model
    selectedEssayTitle = essayMap.has("The Transformer Attractor")
      ? "The Transformer Attractor"
      : essays[0]?.title;
    routingCenterTitle = selectedEssayTitle;

    // Update Hero Metrics
    if (model.stats) {
      document.getElementById("stat-total-essays").textContent = model.stats.totalEssays;
      document.getElementById("stat-top-power").textContent = model.stats.topPower;
      document.getElementById("stat-top-traction").textContent = model.stats.topTraction;
      document.getElementById("stat-top-craft").textContent = model.stats.topCraft;
    }

    // Update Anchor List
    const anchorList = document.getElementById("atlas-anchor-list");
    if (anchorList && model.top_anchors) {
      anchorList.innerHTML = model.top_anchors
        .map(essay => `<li><strong>${essay.title}</strong><br>${essay.identity}</li>`)
        .join("");
    }

    // Refresh Visualizations
    renderScatter("atlas-scatter-root", "traction", "craft", "Traction", "Craft", essays);
    renderHeatmap();
    renderRoutingControls();
    renderRoutingTool();

    renderScatter("atlas-debate-root", "debate", "precision", "Debate", "Precision", essays);
    renderMiniTable("atlas-debate-table", essays.slice().sort((a, b) => (b.debate + b.precision) - (a.debate + a.precision) || b.debate - a.debate), [
      { key: "title", render: (row) => `<strong>${row.title}</strong>` },
      { key: "debate", num: true },
      { key: "precision", num: true },
    ]);

    renderScatter("atlas-synthesis-root", "synthesis", "utility", "Synthesis", "Utility", essays);
    renderMiniTable("atlas-synthesis-table", essays.slice().sort((a, b) => (b.synthesis + b.utility) - (a.synthesis + a.utility) || b.synthesis - a.synthesis), [
      { key: "title", render: (row) => `<strong>${row.title}</strong>` },
      { key: "synthesis", num: true },
      { key: "utility", num: true },
    ]);

    renderScatter("atlas-opening-ending-root", "opening", "ending", "Opening", "Ending", essays);
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
    updateSelectionViews();
  }

  function init() {
    renderLegend("atlas-constellation-legend");
    renderLegend("atlas-debate-legend");
    renderLegend("atlas-synthesis-legend");
    renderLegend("atlas-opening-ending-legend");
    
    bindTabs();
    bindSubtabs();

    const modelSelector = document.getElementById("atlas-model-selector");
    if (modelSelector) {
      modelSelector.addEventListener("change", (e) => loadModel(e.target.value));
      loadModel(modelSelector.value);
    } else {
      loadModel(atlas.defaultModel || Object.keys(models)[0]);
    }
  }

  init();
});
