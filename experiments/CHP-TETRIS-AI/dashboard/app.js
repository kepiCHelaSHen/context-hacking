/* ================================================================
   CHP TETRIS AI — Mission Control  |  app.js
   Vanilla JS — WebSocket client, renderers, controls.
   ================================================================ */

"use strict";

// ============================================================================
// State
// ============================================================================

const state = {
  turn: 0,
  maxTurns: 20,
  mode: "VALIDATION",
  running: false,
  baseline: null,
  bestScore: 0,
  scores: [],           // [{turn, mean, std}]
  deadEndTurns: [],
  fpTurns: [],
  previousCode: "",
  currentWeights: null,
  gateScores: { frozen: 0, architecture: 0, scientific: 0, drift: 0 },
  sigmaSeeds: [],
  sigmaCV: 0,
  deadEndCount: 0,
  fpCount: 0,
  consecutivePasses: 0,
  totalTokens: 0,
};


// ============================================================================
// DOM references
// ============================================================================

const dom = {
  turnCurrent:    document.getElementById("turn-current"),
  turnMax:        document.getElementById("turn-max"),
  modeBadge:      document.getElementById("mode-badge"),
  liveIndicator:  document.getElementById("live-indicator"),
  speedSelect:    document.getElementById("speed-select"),
  btnDemo:        document.getElementById("btn-start-demo"),
  btnLive:        document.getElementById("btn-start-live"),
  btnStop:        document.getElementById("btn-stop"),
  btnReset:       document.getElementById("btn-reset"),
  gameCanvas:     document.getElementById("game-canvas"),
  gameGen:        document.getElementById("game-gen"),
  statLines:      document.getElementById("stat-lines"),
  statPieces:     document.getElementById("stat-pieces"),
  statScore:      document.getElementById("stat-score"),
  weightsBody:    document.querySelector("#weights-table tbody"),
  scoreChart:     document.getElementById("score-chart"),
  decisionLog:    document.getElementById("decision-log"),
  logCount:       document.getElementById("log-count"),
  codeContent:    document.getElementById("code-content"),
  codeStatus:     document.getElementById("code-status"),
  gateBars:       document.getElementById("gate-bars"),
  sigmaSeeds:     document.getElementById("sigma-seeds"),
  sigmaCV:        document.getElementById("sigma-cv"),
  healthStats:    document.getElementById("health-stats"),
  improvement:    document.getElementById("improvement"),
};

const ctx = dom.gameCanvas.getContext("2d");


// ============================================================================
// Tetris piece colors (0 = empty)
// ============================================================================

const PIECE_COLORS = [
  "#f5f5f5", // 0 — empty
  "#00bcd4", // 1 — I (cyan)
  "#ffeb3b", // 2 — O (yellow)
  "#9c27b0", // 3 — T (purple)
  "#4caf50", // 4 — S (green)
  "#f44336", // 5 — Z (red)
  "#2196f3", // 6 — J (blue)
  "#ff9800", // 7 — L (orange)
];


// ============================================================================
// WebSocket connection
// ============================================================================

let ws = null;
let reconnectTimer = null;

function connect() {
  const proto = location.protocol === "https:" ? "wss:" : "ws:";
  ws = new WebSocket(`${proto}//${location.host}/ws`);

  ws.onopen = () => {
    if (reconnectTimer) { clearInterval(reconnectTimer); reconnectTimer = null; }
    updateIndicator("connected");
  };

  ws.onclose = () => {
    updateIndicator("disconnected");
    if (!reconnectTimer) {
      reconnectTimer = setInterval(connect, 2000);
    }
  };

  ws.onerror = () => {
    // onclose will fire after this
  };

  ws.onmessage = (e) => {
    try {
      handleMessage(JSON.parse(e.data));
    } catch (err) {
      console.error("Message parse error:", err, e.data);
    }
  };
}

function updateIndicator(status) {
  const el = dom.liveIndicator;
  el.className = "indicator";
  switch (status) {
    case "connected":
      el.textContent = "\u25CF CONNECTED";
      el.classList.add("indicator-connected");
      break;
    case "running":
      el.textContent = "\u25CF RUNNING";
      el.classList.add("indicator-running");
      break;
    case "disconnected":
      el.textContent = "\u25CF DISCONNECTED";
      el.classList.add("indicator-disconnected");
      break;
    default:
      el.textContent = "\u25CF IDLE";
      el.classList.add("indicator-idle");
  }
}


// ============================================================================
// Message handler
// ============================================================================

function handleMessage(msg) {
  switch (msg.type) {
    case "turn_start":      onTurnStart(msg);      break;
    case "health_check":    onHealthCheck(msg);     break;
    case "council_result":  onCouncilResult(msg);   break;
    case "code_update":     onCodeUpdate(msg);      break;
    case "weights_update":  onWeightsUpdate(msg);   break;
    case "game_results":    onGameResults(msg);     break;
    case "sigma_gate":      onSigmaGate(msg);       break;
    case "critic_verdict":  onCriticVerdict(msg);   break;
    case "reviewer_verdict":onReviewerVerdict(msg); break;
    case "turn_complete":   onTurnComplete(msg);    break;
    case "game_start":      onGameStart(msg);       break;
    case "game_move":       onGameMove(msg);        break;
    case "game_over":       onGameOver(msg);        break;
    case "dead_end":        onDeadEnd(msg);         break;
    case "false_positive":  onFalsePositive(msg);   break;
    case "mode_change":     onModeChange(msg);      break;
    case "exit":            onExit(msg);            break;
    case "reset":           onReset(msg);           break;
    case "demo_complete":   onDemoComplete(msg);    break;
    case "error":           onError(msg);           break;
  }
}


// ============================================================================
// Event handlers
// ============================================================================

function onTurnStart(msg) {
  state.turn = msg.turn || state.turn + 1;
  if (msg.max_turns) state.maxTurns = msg.max_turns;
  state.running = true;
  dom.turnCurrent.textContent = state.turn;
  dom.turnMax.textContent = state.maxTurns;
  updateIndicator("running");
  updateButtons(true);

  addLogEntry("blue", state.turn, "Turn started", `Mode: ${state.mode}`);
}

function onHealthCheck(msg) {
  const icon = msg.passed ? "\u2713" : "\u2717";
  const color = msg.passed ? "green" : "red";
  addLogEntry(color, state.turn,
    `Health check: ${msg.agent} ${icon}`,
    msg.passed ? "Agent responsive" : "Agent NOT responsive"
  );
}

function onCouncilResult(msg) {
  addLogEntry("blue", state.turn,
    `Council: ${msg.n_succeeded} model(s) responded`,
    msg.drift_flagged ? "Drift flagged by council" : "No drift flagged"
  );
}

function onCodeUpdate(msg) {
  if (msg.code) {
    updateCodePanel(msg.code);
  }
}

function onWeightsUpdate(msg) {
  if (msg.weights) {
    updateWeightsTable(msg.weights);
  }
}

function onGameResults(msg) {
  const turnScores = msg.scores || [];
  const mean = msg.mean || 0;
  const std = turnScores.length > 1 ? calcStd(turnScores) : 0;

  state.scores.push({ turn: state.turn, mean, std });

  if (state.baseline === null) {
    state.baseline = mean;
  }

  updateScoreChart();
  addLogEntry("blue", state.turn,
    `Games complete: mean=${mean.toFixed(1)}, CV=${(msg.cv || 0).toFixed(4)}`,
    `${turnScores.length} seeds, scores: [${turnScores.map(s => s.toFixed(0)).join(", ")}]`
  );
}

function onSigmaGate(msg) {
  state.sigmaSeeds = msg.seeds || [];
  state.sigmaCV = msg.cv || 0;
  renderSigmaSeeds(state.sigmaSeeds);
  dom.sigmaCV.textContent = `CV: ${state.sigmaCV.toFixed(4)} (threshold: ${(msg.threshold || 0.15).toFixed(2)}) ${msg.passed ? "\u2713 PASS" : "\u2717 FAIL"}`;
  dom.sigmaCV.style.color = msg.passed ? "var(--green)" : "var(--red)";
}

function onCriticVerdict(msg) {
  const gates = msg.gates || {};
  state.gateScores = {
    frozen:       gates.frozen || 0,
    architecture: gates.architecture || 0,
    scientific:   gates.scientific || 0,
    drift:        gates.drift || 0,
  };
  renderGateBars();

  const color = msg.verdict === "PASS" ? "green" : "red";
  const blocking = (msg.blocking || []);
  addLogEntry(color, state.turn,
    `Critic: ${msg.verdict}`,
    blocking.length > 0
      ? `Blocking: ${blocking.join("; ")}`
      : "No blocking issues"
  );
}

function onReviewerVerdict(msg) {
  const color = msg.verdict === "APPROVE" ? "green"
    : msg.verdict === "APPROVE WITH NOTES" ? "orange"
    : "red";
  const issues = (msg.issues || []);
  addLogEntry(color, state.turn,
    `Reviewer: ${msg.verdict}`,
    issues.length > 0
      ? issues.map(i => `[${i.severity}] ${i.description}`).join("; ")
      : "No issues"
  );
}

function onTurnComplete(msg) {
  state.turn = msg.turn || state.turn;
  dom.turnCurrent.textContent = state.turn;

  const accepted = msg.accepted;
  if (accepted) {
    state.consecutivePasses++;
    state.bestScore = msg.best_score || state.bestScore;
    if (msg.weights) {
      state.currentWeights = msg.weights;
      updateWeightsTable(msg.weights);
      updateCodePanel(generateCodeDisplay(msg.weights));
    }
  } else {
    state.consecutivePasses = 0;
  }

  // Update improvement in footer
  if (state.baseline !== null && state.baseline > 0) {
    const pct = ((state.bestScore - state.baseline) / state.baseline * 100).toFixed(0);
    const sign = pct >= 0 ? "+" : "";
    dom.improvement.textContent = `Improvement: ${sign}${pct}% (best: ${state.bestScore.toFixed(1)})`;
    dom.improvement.style.color = pct >= 0 ? "var(--green)" : "var(--red)";
  }

  if (msg.mode) {
    state.mode = msg.mode;
    updateModeBadge();
  }

  renderHealthStats();

  const color = accepted ? "green" : "red";
  const meanStr = msg.new_mean != null ? msg.new_mean.toFixed(1) : "?";
  const bestStr = msg.best_score != null ? msg.best_score.toFixed(1) : "?";
  addLogEntry(color, state.turn,
    accepted ? `Turn ACCEPTED (mean: ${meanStr})` : `Turn REJECTED`,
    accepted
      ? `New best: ${bestStr}`
      : msg.reason || `Mean ${meanStr} did not improve over best ${bestStr}`
  );
}

function onGameStart(msg) {
  dom.gameGen.textContent = msg.seed != null ? `Seed ${msg.seed}` : "";
  dom.statLines.textContent = "0";
  dom.statPieces.textContent = "0";
  dom.statScore.textContent = "0";
  clearCanvas();
}

function onGameMove(msg) {
  if (msg.board) renderBoard(msg.board);
  if (msg.lines != null) dom.statLines.textContent = msg.lines;
  if (msg.pieces != null) dom.statPieces.textContent = msg.pieces;
  if (msg.score != null) dom.statScore.textContent = msg.score;
}

function onGameOver(msg) {
  if (msg.lines != null) dom.statLines.textContent = msg.lines;
  if (msg.score != null) dom.statScore.textContent = msg.score;
}

function onDeadEnd(msg) {
  state.deadEndCount++;
  state.deadEndTurns.push(msg.turn || state.turn);
  updateScoreChart();
  addLogEntry("red", msg.turn || state.turn,
    "DEAD END recorded",
    msg.description || "Weight vector marked as dead end"
  );
  renderHealthStats();
}

function onFalsePositive(msg) {
  state.fpCount++;
  state.fpTurns.push(msg.turn || state.turn);
  updateScoreChart();
  addLogEntry("orange", msg.turn || state.turn,
    "FALSE POSITIVE caught",
    msg.description || "Score improvement was not real"
  );
  renderHealthStats();
}

function onModeChange(msg) {
  state.mode = msg.to || state.mode;
  updateModeBadge();
  addLogEntry("blue", msg.turn || state.turn,
    `Mode: ${msg.from} \u2192 ${msg.to}`,
    ""
  );
}

function onExit(msg) {
  state.running = false;
  updateIndicator("connected");
  updateButtons(false);
  addLogEntry("blue", msg.turn || state.turn,
    `EXIT: ${msg.reason}`,
    "Optimization loop ended"
  );
}

function onDemoComplete() {
  state.running = false;
  updateIndicator("connected");
  updateButtons(false);
  addLogEntry("blue", state.turn, "Demo replay complete", "");
}

function onError(msg) {
  addLogEntry("red", state.turn,
    `Error: ${msg.message || "Unknown error"}`, ""
  );
}

function onReset() {
  resetState();
  resetUI();
  addLogEntry("blue", 0, "Reset", "All state cleared");
}


// ============================================================================
// Renderers
// ============================================================================

// --- Game Canvas ---

function clearCanvas() {
  ctx.fillStyle = "#fafafa";
  ctx.fillRect(0, 0, dom.gameCanvas.width, dom.gameCanvas.height);
  drawGrid();
}

function renderBoard(board) {
  const cols = 10;
  const rows = 20;
  const cellW = dom.gameCanvas.width / cols;
  const cellH = dom.gameCanvas.height / rows;

  ctx.fillStyle = "#fafafa";
  ctx.fillRect(0, 0, dom.gameCanvas.width, dom.gameCanvas.height);

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const val = board[r * cols + c] || 0;
      if (val > 0) {
        ctx.fillStyle = PIECE_COLORS[val] || PIECE_COLORS[1];
        ctx.fillRect(c * cellW, r * cellH, cellW, cellH);
        // Inner border for depth
        ctx.fillStyle = "rgba(255,255,255,0.25)";
        ctx.fillRect(c * cellW, r * cellH, cellW, 1);
        ctx.fillRect(c * cellW, r * cellH, 1, cellH);
        ctx.fillStyle = "rgba(0,0,0,0.1)";
        ctx.fillRect(c * cellW + cellW - 1, r * cellH, 1, cellH);
        ctx.fillRect(c * cellW, r * cellH + cellH - 1, cellW, 1);
      }
    }
  }

  drawGrid();
}

function drawGrid() {
  const cols = 10;
  const rows = 20;
  const cellW = dom.gameCanvas.width / cols;
  const cellH = dom.gameCanvas.height / rows;

  ctx.strokeStyle = "#e8e8e8";
  ctx.lineWidth = 0.5;
  for (let r = 0; r <= rows; r++) {
    ctx.beginPath();
    ctx.moveTo(0, r * cellH);
    ctx.lineTo(dom.gameCanvas.width, r * cellH);
    ctx.stroke();
  }
  for (let c = 0; c <= cols; c++) {
    ctx.beginPath();
    ctx.moveTo(c * cellW, 0);
    ctx.lineTo(c * cellW, dom.gameCanvas.height);
    ctx.stroke();
  }
}


// --- Weights Table ---

let previousWeights = {};

function updateWeightsTable(weights) {
  if (!weights) return;
  const tbody = dom.weightsBody;
  tbody.innerHTML = "";

  const featureNames = [
    "aggregate_height", "complete_lines", "holes", "bumpiness",
    "well_depth", "tetris_readiness", "column_transitions", "row_transitions"
  ];

  for (const name of featureNames) {
    const val = weights[name] != null ? weights[name] : 0;
    const tr = document.createElement("tr");

    const tdName = document.createElement("td");
    tdName.textContent = name.replace(/_/g, " ");
    tr.appendChild(tdName);

    const tdVal = document.createElement("td");
    tdVal.textContent = val.toFixed(3);
    if (val > 0) tdVal.className = "weight-positive";
    else if (val < 0) tdVal.className = "weight-negative";
    else tdVal.className = "weight-zero";

    // Flash if changed
    if (previousWeights[name] != null && previousWeights[name] !== val) {
      tr.classList.add("weight-flash");
    }

    tr.appendChild(tdVal);
    tbody.appendChild(tr);
  }

  previousWeights = { ...weights };
  state.currentWeights = weights;
}


// --- Score Chart (SVG) ---

function updateScoreChart() {
  const svg = dom.scoreChart;
  const data = state.scores;
  if (data.length === 0) return;

  // Measure the parent for responsive sizing
  const rect = svg.parentElement.getBoundingClientRect();
  const width = Math.max(rect.width - 24, 200);
  const height = Math.max(rect.height - 50, 100);

  const pad = { top: 16, right: 16, bottom: 28, left: 48 };
  const plotW = width - pad.left - pad.right;
  const plotH = height - pad.top - pad.bottom;

  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);

  // Determine scale
  let yMin = Infinity, yMax = -Infinity;
  for (const d of data) {
    const lo = d.mean - d.std;
    const hi = d.mean + d.std;
    if (lo < yMin) yMin = lo;
    if (hi > yMax) yMax = hi;
  }
  if (yMin === yMax) { yMin -= 1; yMax += 1; }
  const yRange = yMax - yMin;
  yMin -= yRange * 0.1;
  yMax += yRange * 0.1;

  const xMin = data.length > 1 ? data[0].turn : data[0].turn - 1;
  const xMax = data.length > 1 ? data[data.length - 1].turn : data[0].turn + 1;

  function sx(turn) { return pad.left + ((turn - xMin) / (xMax - xMin)) * plotW; }
  function sy(val)  { return pad.top + (1 - (val - yMin) / (yMax - yMin)) * plotH; }

  let html = "";

  // Grid lines (horizontal)
  const yTicks = niceScale(yMin, yMax, 5);
  for (const v of yTicks) {
    const y = sy(v);
    html += `<line x1="${pad.left}" y1="${y}" x2="${width - pad.right}" y2="${y}" class="chart-grid-line"/>`;
    html += `<text x="${pad.left - 4}" y="${y + 3}" text-anchor="end" class="chart-axis-label">${v.toFixed(0)}</text>`;
  }

  // X-axis labels
  for (const d of data) {
    const x = sx(d.turn);
    html += `<text x="${x}" y="${height - 4}" text-anchor="middle" class="chart-axis-label">${d.turn}</text>`;
  }

  // Variance band (mean +/- std)
  if (data.length > 1) {
    let bandPath = `M ${sx(data[0].turn)} ${sy(data[0].mean + data[0].std)}`;
    for (let i = 1; i < data.length; i++) {
      bandPath += ` L ${sx(data[i].turn)} ${sy(data[i].mean + data[i].std)}`;
    }
    for (let i = data.length - 1; i >= 0; i--) {
      bandPath += ` L ${sx(data[i].turn)} ${sy(data[i].mean - data[i].std)}`;
    }
    bandPath += " Z";
    html += `<path d="${bandPath}" class="chart-band"/>`;
  }

  // Score line
  if (data.length > 1) {
    let linePath = `M ${sx(data[0].turn)} ${sy(data[0].mean)}`;
    for (let i = 1; i < data.length; i++) {
      linePath += ` L ${sx(data[i].turn)} ${sy(data[i].mean)}`;
    }
    html += `<path d="${linePath}" class="chart-line"/>`;
  }

  // Dots
  for (let i = 0; i < data.length; i++) {
    const d = data[i];
    const x = sx(d.turn);
    const y = sy(d.mean);
    const isDead = state.deadEndTurns.includes(d.turn);
    const isFP = state.fpTurns.includes(d.turn);
    const isCurrent = i === data.length - 1;

    if (isDead) {
      html += `<circle cx="${x}" cy="${y}" r="5" class="chart-dot-dead-end"/>`;
    } else if (isFP) {
      html += `<circle cx="${x}" cy="${y}" r="5" class="chart-dot-fp"/>`;
    } else if (isCurrent) {
      html += `<circle cx="${x}" cy="${y}" r="5" class="chart-dot-current"/>`;
    } else {
      html += `<circle cx="${x}" cy="${y}" r="3" class="chart-dot"/>`;
    }
  }

  svg.innerHTML = html;
}


// --- Decision Log ---

let logEntryCount = 0;

function addLogEntry(color, turn, description, outcome) {
  logEntryCount++;
  const entry = document.createElement("div");
  entry.className = `log-entry log-entry-${color}`;
  entry.innerHTML = `
    <div><span class="log-turn">T${turn}</span><span class="log-desc">${escapeHtml(description)}</span></div>
    ${outcome ? `<div class="log-outcome">${escapeHtml(outcome)}</div>` : ""}
  `;
  dom.decisionLog.appendChild(entry);
  dom.decisionLog.scrollTop = dom.decisionLog.scrollHeight;
  dom.logCount.textContent = `${logEntryCount}`;
}


// --- Code Panel ---

let typewriterTimer = null;

function updateCodePanel(code) {
  if (typewriterTimer) clearInterval(typewriterTimer);

  const prev = state.previousCode;
  state.previousCode = code;
  dom.codeStatus.textContent = "updating";

  const lines = code.split("\n");
  const prevLines = prev ? prev.split("\n") : [];

  // Determine changed lines for diff highlighting
  const changedIndices = new Set();
  for (let i = 0; i < lines.length; i++) {
    if (i >= prevLines.length || lines[i] !== prevLines[i]) {
      changedIndices.add(i);
    }
  }

  // Build highlighted HTML
  const htmlLines = lines.map((line, i) => {
    const lineNum = `<span class="code-line-number">${i + 1}</span>`;
    const highlighted = highlightSyntax(line);
    const cls = changedIndices.has(i) && prev ? " code-line-added" : "";
    return `<span class="code-line${cls}">${lineNum}${highlighted}</span>`;
  });

  // Typewriter effect: reveal line by line
  const el = dom.codeContent;
  let visibleCount = 0;
  const allHtml = htmlLines.join("\n");

  // If short code, just show it immediately
  if (htmlLines.length <= 3) {
    el.innerHTML = allHtml;
    dom.codeStatus.textContent = "";
    return;
  }

  el.innerHTML = "";
  typewriterTimer = setInterval(() => {
    visibleCount++;
    if (visibleCount >= htmlLines.length) {
      el.innerHTML = allHtml;
      clearInterval(typewriterTimer);
      typewriterTimer = null;
      dom.codeStatus.textContent = "";
      return;
    }
    el.innerHTML = htmlLines.slice(0, visibleCount).join("\n");
  }, 60);
}

function highlightSyntax(line) {
  let s = escapeHtml(line);

  // Comments
  s = s.replace(/(#.*)$/, '<span class="syn-comment">$1</span>');

  // Strings (simple, single or double quoted — before keywords)
  s = s.replace(/((&quot;|&#x27;).*?\2)/g, '<span class="syn-string">$1</span>');

  // Keywords
  s = s.replace(/\b(def|return|if|else|elif|for|while|import|from|class|and|or|not|in|is|None|True|False)\b/g,
    '<span class="syn-keyword">$1</span>');

  // Numbers (floats and ints)
  s = s.replace(/\b(\d+\.?\d*)\b/g, '<span class="syn-number">$1</span>');

  // Function calls — word followed by (
  s = s.replace(/\b([a-zA-Z_]\w*)\s*\(/g, '<span class="syn-func">$1</span>(');

  return s;
}


// --- Protocol Health: Gate Bars ---

const GATE_CONFIG = [
  { key: "frozen",       label: "Frozen",     threshold: 1.0  },
  { key: "architecture", label: "Arch",       threshold: 0.85 },
  { key: "scientific",   label: "Scientific", threshold: 0.85 },
  { key: "drift",        label: "Drift",      threshold: 0.85 },
];

function renderGateBars() {
  let html = "";
  for (const g of GATE_CONFIG) {
    const val = state.gateScores[g.key] || 0;
    const pct = Math.min(val, 1.0) * 100;
    const pass = val >= g.threshold;
    const threshPct = g.threshold * 100;
    html += `
      <div class="gate-bar">
        <span class="gate-label">${g.label}</span>
        <div class="gate-track">
          <div class="gate-fill ${pass ? "gate-fill-pass" : "gate-fill-fail"}" style="width:${pct}%"></div>
          <div class="gate-threshold" style="left:${threshPct}%"></div>
        </div>
        <span class="gate-value" style="color:${pass ? "var(--green)" : "var(--red)"}">${val.toFixed(2)}</span>
      </div>
    `;
  }
  dom.gateBars.innerHTML = html;
}

// --- Protocol Health: Sigma Seeds ---

function renderSigmaSeeds(seeds) {
  let html = "";
  for (let i = 0; i < 10; i++) {
    const status = seeds[i] || "pending";
    const cls = status === "pass" ? "seed-pass" : status === "fail" ? "seed-fail" : "seed-pending";
    html += `<div class="seed ${cls}" title="Seed ${i}: ${status}"></div>`;
  }
  dom.sigmaSeeds.innerHTML = html;
}

// --- Protocol Health: Stats ---

function renderHealthStats() {
  dom.healthStats.innerHTML = `
    <div class="stat-row"><span>Dead ends</span><span class="stat-value">${state.deadEndCount}</span></div>
    <div class="stat-row"><span>False positives</span><span class="stat-value">${state.fpCount}</span></div>
    <div class="stat-row"><span>Consecutive passes</span><span class="stat-value">${state.consecutivePasses}</span></div>
    <div class="stat-row"><span>Mode</span><span class="stat-value">${state.mode}</span></div>
    <div class="stat-row"><span>Best score</span><span class="stat-value">${state.bestScore.toFixed(1)}</span></div>
  `;
}


// ============================================================================
// Mode badge
// ============================================================================

function updateModeBadge() {
  const badge = dom.modeBadge;
  badge.textContent = state.mode;
  badge.className = "badge";
  if (state.mode === "EXPLORATION") {
    badge.classList.add("badge-exploration");
  } else {
    badge.classList.add("badge-validation");
  }
}


// ============================================================================
// Controls
// ============================================================================

function updateButtons(running) {
  state.running = running;
  dom.btnDemo.disabled = running;
  dom.btnLive.disabled = running;
  dom.btnStop.disabled = !running;
}

dom.btnDemo.addEventListener("click", () => {
  fetch("/api/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ mode: "demo" }),
  });
  updateButtons(true);
  updateIndicator("running");
});

dom.btnLive.addEventListener("click", () => {
  fetch("/api/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ mode: "live" }),
  });
  updateButtons(true);
  updateIndicator("running");
});

dom.btnStop.addEventListener("click", () => {
  fetch("/api/stop", { method: "POST" });
  updateButtons(false);
  updateIndicator("connected");
});

dom.btnReset.addEventListener("click", () => {
  fetch("/api/reset", { method: "POST" });
});

dom.speedSelect.addEventListener("change", () => {
  const speed = Number(dom.speedSelect.value);
  fetch("/api/speed", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ speed }),
  });
});


// ============================================================================
// Reset
// ============================================================================

function resetState() {
  state.turn = 0;
  state.mode = "VALIDATION";
  state.running = false;
  state.baseline = null;
  state.bestScore = 0;
  state.scores = [];
  state.deadEndTurns = [];
  state.fpTurns = [];
  state.previousCode = "";
  state.currentWeights = null;
  state.gateScores = { frozen: 0, architecture: 0, scientific: 0, drift: 0 };
  state.sigmaSeeds = [];
  state.sigmaCV = 0;
  state.deadEndCount = 0;
  state.fpCount = 0;
  state.consecutivePasses = 0;
  state.totalTokens = 0;
  previousWeights = {};
  logEntryCount = 0;
}

function resetUI() {
  dom.turnCurrent.textContent = "0";
  dom.turnMax.textContent = "20";
  updateModeBadge();
  updateIndicator("connected");
  updateButtons(false);
  dom.statLines.textContent = "0";
  dom.statPieces.textContent = "0";
  dom.statScore.textContent = "0";
  dom.gameGen.textContent = "";
  dom.weightsBody.innerHTML = "";
  dom.scoreChart.innerHTML = "";
  dom.decisionLog.innerHTML = "";
  dom.logCount.textContent = "";
  dom.codeContent.textContent = "// Waiting for first turn...";
  dom.codeStatus.textContent = "";
  dom.gateBars.innerHTML = "";
  dom.sigmaSeeds.innerHTML = "";
  dom.sigmaCV.textContent = "";
  dom.healthStats.innerHTML = "";
  dom.improvement.textContent = "\u2014";
  dom.improvement.style.color = "";
  clearCanvas();

  // Initialize with placeholder gate bars and seeds
  renderGateBars();
  renderSigmaSeeds([]);
  renderHealthStats();
}


// ============================================================================
// Utility
// ============================================================================

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function calcStd(arr) {
  if (arr.length < 2) return 0;
  const mean = arr.reduce((a, b) => a + b, 0) / arr.length;
  const variance = arr.reduce((sum, v) => sum + (v - mean) ** 2, 0) / (arr.length - 1);
  return Math.sqrt(variance);
}

function niceScale(lo, hi, targetTicks) {
  const range = hi - lo;
  if (range <= 0) return [lo];
  const rough = range / targetTicks;
  const mag = Math.pow(10, Math.floor(Math.log10(rough)));
  const nice = rough / mag >= 5 ? 5 * mag : rough / mag >= 2 ? 2 * mag : mag;
  const start = Math.ceil(lo / nice) * nice;
  const ticks = [];
  for (let v = start; v <= hi; v += nice) {
    ticks.push(Math.round(v * 1000) / 1000);
  }
  return ticks.length > 0 ? ticks : [lo, hi];
}

function generateCodeDisplay(weights) {
  const nonZero = Object.entries(weights).filter(([, w]) => w !== 0);
  if (nonZero.length === 0) return 'def evaluate(board):\n    """Weighted evaluation."""\n    return 0.0\n';

  let lines = ['def evaluate(board):', '    """Weighted evaluation."""', '    return ('];
  const [firstName, firstW] = nonZero[0];
  lines.push(`        ${firstW >= 0 ? "+" : ""}${firstW.toFixed(3)} * ${firstName}(board)`);
  for (let i = 1; i < nonZero.length; i++) {
    const [name, w] = nonZero[i];
    lines.push(`      + ${w >= 0 ? "+" : ""}${w.toFixed(3)} * ${name}(board)`);
  }
  lines.push("    )");
  return lines.join("\n") + "\n";
}


// ============================================================================
// Initialize
// ============================================================================

clearCanvas();
renderGateBars();
renderSigmaSeeds([]);
renderHealthStats();
connect();
