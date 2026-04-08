<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WebLinac — Physique des photons thérapeutiques</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg:     #0d1117;
      --surf:   #161b22;
      --surf2:  #21262d;
      --border: #30363d;
      --accent: #58a6ff;
      --text:   #c9d1d9;
      --muted:  #8b949e;
    }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      font-size: 13px;
      min-height: 100vh;
    }

    /* ── HEADER ── */
    .hdr {
      background: var(--surf);
      border-bottom: 1px solid var(--border);
      padding: 12px 20px;
      display: flex; align-items: center; justify-content: space-between;
    }
    .hdr h1 { font-size: 17px; font-weight: 700; color: var(--accent); }
    .hdr p  { font-size: 11px; color: var(--muted); margin-top: 2px; }
    .badge {
      background: rgba(88,166,255,.12); color: var(--accent);
      border: 1px solid rgba(88,166,255,.3);
      border-radius: 20px; padding: 3px 10px;
      font-size: 11px; font-weight: 600; white-space: nowrap;
    }

    /* ── CONTROLS ── */
    .ctrls {
      background: var(--surf); border-bottom: 1px solid var(--border);
      padding: 12px 20px; display: flex; gap: 26px; flex-wrap: wrap; align-items: flex-start;
    }
    .ctrl { display: flex; flex-direction: column; gap: 5px; }
    .ctrl label { font-size: 10px; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); font-weight: 700; }
    .ctrl select {
      background: var(--surf2); border: 1px solid var(--border); color: var(--text);
      border-radius: 6px; padding: 5px 9px; font-size: 13px; outline: none;
    }
    .ctrl select:focus { border-color: var(--accent); }
    .slider-row { display: flex; align-items: center; gap: 10px; }
    .ctrl input[type="range"] { width: 150px; accent-color: var(--accent); cursor: pointer; }
    .sval { font-weight: 700; color: var(--accent); min-width: 72px; font-size: 13px; }

    /* depth rows */
    .depth-tbl { display: grid; grid-template-columns: 14px 22px 58px 20px; gap: 5px 8px; align-items: center; }
    .dswatch { height: 4px; border-radius: 2px; }
    .dlabel  { font-size: 11px; color: var(--muted); }
    .dnum {
      width: 58px; background: var(--surf2); border: 1px solid var(--border); color: var(--text);
      border-radius: 4px; padding: 3px 6px; font-size: 12px; text-align: center; outline: none;
    }
    .dnum:focus { border-color: var(--accent); }

    /* ── MAIN GRID ── */
    .main {
      padding: 14px 20px;
      display: grid;
      grid-template-columns: 380px 1fr 164px;
      grid-template-rows: auto auto;
      grid-template-areas: "phantom pdd schema" "profiles profiles profiles";
      gap: 14px;
    }
    @media (max-width: 980px) {
      .main { grid-template-columns: 1fr; grid-template-areas: "phantom" "pdd" "schema" "profiles"; }
    }

    /* ── CARDS ── */
    .card { background: var(--surf); border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }
    .card-hdr {
      padding: 9px 14px; border-bottom: 1px solid var(--border);
      font-size: 10px; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); font-weight: 700;
      display: flex; justify-content: space-between; align-items: center;
    }
    .card-hdr span { color: var(--accent); font-size: 11px; text-transform: none; letter-spacing: 0; }
    .card-body { padding: 12px 14px; }

    /* ── PHANTOM ── */
    .phantom-area { grid-area: phantom; }
    .phantom-inner { display: flex; gap: 6px; align-items: flex-start; }

    /* Depth-axis label (HTML rotated element) */
    .ph-depth-lbl {
      writing-mode: vertical-rl;
      transform: rotate(180deg);
      font-size: 10px; color: var(--muted); white-space: nowrap;
      display: flex; align-items: center;
      padding-right: 2px; flex-shrink: 0;
    }

    #phantom-cv { cursor: crosshair; display: block; border-radius: 4px; }
    .cb-wrap { display: flex; flex-direction: column; align-items: center; gap: 2px; flex-shrink: 0; }
    .cb-wrap em { font-size: 9px; color: var(--muted); font-style: normal; }
    #cb-cv { border-radius: 3px; }
    .htip {
      position: absolute; background: rgba(13,17,23,.93); border: 1px solid var(--border);
      border-radius: 6px; padding: 6px 10px; font-size: 11px; line-height: 1.6;
      pointer-events: none; display: none; z-index: 20; white-space: nowrap;
    }
    .phantom-wrap { position: relative; display: inline-block; }

    /* ── PDD ── */
    .pdd-area { grid-area: pdd; }
    .chart-wrap { position: relative; height: 280px; }

    /* ── SCHEMA ── */
    .schema-area { grid-area: schema; }
    #schema-cv { display: block; border-radius: 4px; }

    /* ── PROFILES ── */
    .profiles-area { grid-area: profiles; }
    .profiles-wrap { position: relative; height: 230px; }

    /* metrics table */
    .metrics-wrap { margin-top: 10px; overflow-x: auto; }
    .metrics-tbl { width: 100%; border-collapse: collapse; font-size: 11px; }
    .metrics-tbl th {
      padding: 4px 10px; text-align: left; color: var(--muted);
      font-weight: 600; font-size: 10px; text-transform: uppercase; letter-spacing: .04em;
      border-bottom: 1px solid var(--border); white-space: nowrap;
    }
    .metrics-tbl td { padding: 4px 10px; border-bottom: 1px solid rgba(48,54,61,.5); white-space: nowrap; }
    .metrics-tbl td b { color: var(--accent); }
    .dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 5px; vertical-align: middle; }

    /* chips */
    .chips { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }
    .chip { background: var(--surf2); border: 1px solid var(--border); border-radius: 20px; padding: 3px 10px; font-size: 11px; }
    .chip b { color: var(--accent); }

    footer { text-align: center; padding: 10px; font-size: 10px; color: var(--muted); border-top: 1px solid var(--border); }
  </style>
</head>
<body>

<div class="hdr">
  <div>
    <h1>WebLinac</h1>
    <p>Simulation pédagogique simplifié d'un accélérateur linéaire médical</p>
  </div>
  <span class="badge">Centre Oscar Lambret</span>
</div>

<div class="ctrls">
  <div class="ctrl">
    <label>Énergie nominale</label>
    <select id="energy">
      <option value="4">4 MV</option>
      <option value="6" selected>6 MV</option>
      <option value="10">10 MV</option>
      <option value="15">15 MV</option>
      <option value="18">18 MV</option>
    </select>
  </div>
  <div class="ctrl">
    <label>Taille de champ </label>
    <div class="slider-row">
      <input type="range" id="fieldSize" min="2" max="30" step="1" value="10">
      <span class="sval" id="fs-disp">10 × 10 cm</span>
    </div>
  </div>
  <div class="ctrl">
    <label>Distance Source-Surface (DSP)</label>
    <div class="slider-row">
      <input type="range" id="ssd" min="80" max="130" step="5" value="100">
      <span class="sval" id="ssd-disp">100 cm</span>
    </div>
  </div>
  <div class="ctrl">
    <label>Profondeurs des profils</label>
    <div class="depth-tbl" id="depth-tbl"></div>
  </div>
</div>

<div class="main">

  <!-- 2D DOSE MAP -->
  <div class="card phantom-area">
    <div class="card-hdr">Distribution de dose 2D<span id="dmax-info"></span></div>
    <div class="card-body">
      <div class="phantom-inner">
        <span class="ph-depth-lbl">Profondeur (cm)</span>
        <div class="phantom-wrap">
          <canvas id="phantom-cv" width="296" height="340"></canvas>
          <div class="htip" id="htip"></div>
        </div>
        <div class="cb-wrap">
          <em>100%</em>
          <canvas id="cb-cv" width="18" height="256"></canvas>
          <em>0%</em>
        </div>
      </div>
      <div class="chips" id="chips"></div>
    </div>
  </div>

  <!-- PDD -->
  <div class="card pdd-area">
    <div class="card-hdr">Rendement en profondeur (PDD) — axe central</div>
    <div class="card-body">
      <div class="chart-wrap"><canvas id="pdd-cv"></canvas></div>
      <p style="margin-top:8px;font-size:11px;color:var(--muted)">
        Dose normalisée à d<sub>max</sub> = 100 % · trait pointillé jaune = d<sub>max</sub>
      </p>
    </div>
  </div>

  <!-- SCHÉMA -->
  <div class="card schema-area">
    <div class="card-hdr">Schéma du dispositif</div>
    <div class="card-body" style="padding:10px 8px;">
      <canvas id="schema-cv" width="140" height="326"></canvas>
    </div>
  </div>

  <!-- PROFILES -->
  <div class="card profiles-area">
    <div class="card-hdr">Profils de dose transversaux</div>
    <div class="card-body">
      <div class="profiles-wrap"><canvas id="prof-cv"></canvas></div>
      <div class="metrics-wrap">
        <table class="metrics-tbl">
          <thead>
            <tr>
              <th>Profondeur</th>
              <th>Taille de champ D<sub>50%</sub></th>
              <th>Pénombre 20–80 %</th>
              <th>Taille géom. à l'iso (FS × (DSP+d)/100)</th>
            </tr>
          </thead>
          <tbody id="metrics-body"></tbody>
        </table>
      </div>
    </div>
  </div>

</div>

<footer>WebLinac — outil pédagogique de physique médicale · modèle analytique simplifié — Simon MARTIN </footer>

<script>
'use strict';

// ═══════════════════════════════════════════════════════
//  CONSTANTES PHYSIQUES
// ═══════════════════════════════════════════════════════

const SAD = 100; // Distance Source-Axe (isocentre), cm

/**
 * Paramètres faisceau par énergie nominale (MV)
 *  dmax : profondeur de dose max pour FS=10×10 à l'isocentre (cm)
 *  mu   : coefficient d'atténuation effectif (cm⁻¹)
 *  Ds   : dose de surface pour FS=10×10 (fraction de la dose max)
 *  dFS  : décroissance de dmax par cm d'augmentation de FS
 *  sFS  : augmentation de Ds par cm d'augmentation de FS
 */
const BEAM = {
   4: { dmax: 1.0, mu: 0.0560, Ds: 0.40, dFS: 0.006, sFS: 0.004, sig0: 0.28, horn: 0.03 },
   6: { dmax: 1.5, mu: 0.0510, Ds: 0.32, dFS: 0.009, sFS: 0.006, sig0: 0.35, horn: 0.05 },
  10: { dmax: 2.5, mu: 0.0450, Ds: 0.20, dFS: 0.011, sFS: 0.006, sig0: 0.42, horn: 0.08 },
  15: { dmax: 3.0, mu: 0.0400, Ds: 0.15, dFS: 0.012, sFS: 0.005, sig0: 0.48, horn: 0.11 },
  18: { dmax: 3.5, mu: 0.0380, Ds: 0.12, dFS: 0.013, sFS: 0.004, sig0: 0.53, horn: 0.13 },
};

const PCOLS     = ['#38bdf8', '#4ade80', '#fb923c', '#e879f9'];
const X_HALF    = 18;   // demi-largeur affichée ±18 cm
const DEPTH_MAX = 30;   // profondeur maximale 30 cm

// ═══════════════════════════════════════════════════════
//  FONCTIONS PHYSIQUES
// ═══════════════════════════════════════════════════════

function erf(x) {
  const s = x < 0 ? -1 : 1, a = Math.abs(x);
  const t = 1 / (1 + 0.3275911 * a);
  const p = t * (0.254829592 + t * (-0.284496736 + t * (1.421413741 + t * (-1.453152027 + t * 1.061405429))));
  return s * (1 - p * Math.exp(-a * a));
}

/** dmax effectif : diminue légèrement avec FS (plus de diffusé latéral) */
function getEffDmax(E, fs) {
  const { dmax, dFS } = BEAM[E] ?? BEAM[6];
  return Math.max(0.5, dmax - dFS * (fs - 10));
}

/**
 * PDD — axe central
 * fs = taille de champ À L'ISOCENTRE (DSA = 100 cm)
 */
function calcPDD(d, fs, E, ssd) {
  const { mu, Ds: Ds0, sFS } = BEAM[E] ?? BEAM[6];
  const dmax = getEffDmax(E, fs);
  // Dose de surface augmente avec FS (plus de diffusé = plus de contamination)
  const Ds = Math.max(0.08, Math.min(0.80, Ds0 + sFS * (fs - 10)));

  if (d <= 0) return Ds * 100;
  if (d < dmax) {
    const t = d / dmax;
    return 100 * (Ds + (1 - Ds) * (3*t*t - 2*t*t*t));
  }
  const scatter = 1 + 4e-4 * (fs - 10) * (d - dmax);
  const isl = ((ssd + dmax) / (ssd + d)) ** 2;
  return 100 * isl * Math.exp(-mu * (d - dmax)) * scatter;
}

/**
 * Profil latéral normalisé à 1 sur l'axe central
 * La demi-largeur de champ à la profondeur d est calculée par divergence
 * depuis l'isocentre (SAD = 100 cm) : a = (fs/2) × (ssd+d) / SAD
 */
function calcProfile(x, d, fs, E, ssd) {
  // Demi-largeur à la profondeur d (divergence depuis la source, FS défini à SAD=100)
  const a = (fs / 2) * (ssd + d) / SAD;
  // Sigma de pénombre : dépend de l'énergie, de la profondeur et de la taille de champ
  // (grand champ → plus de diffusé latéral → pénombre plus large)
  const { sig0, horn } = BEAM[E] ?? BEAM[6];
  const sig = sig0 + 0.012 * d + 0.004 * (fs - 10);
  const M = Math.SQRT2 * sig;
  const pen = 0.5 * (erf((a - x) / M) + erf((a + x) / M));
  // Cornes (filtre égalisateur) : plus prononcées à haute énergie et à grand champ
  const r = a > 0 ? Math.abs(x) / a : 0;
  const hornEff = horn * Math.max(0.4, 1 + 0.025 * (fs - 10));
  const horns = r < 1 ? (1 + hornEff * r * r) : 1.0;
  // Fuite hors champ
  return pen * horns + 0.018 * (1 - pen);
}

function calcDose(x, d, fs, E, ssd) {
  const axial = calcPDD(d, fs, E, ssd);
  const p  = calcProfile(x, d, fs, E, ssd);
  const p0 = calcProfile(0, d, fs, E, ssd);
  return p0 > 0 ? axial * p / p0 : 0;
}

// ═══════════════════════════════════════════════════════
//  MÉTRIQUES DES PROFILS
// ═══════════════════════════════════════════════════════

/** Recherche dichotomique : position x > 0 où le profil normalisé = frac */
function findXatFrac(frac, d, fs, E, ssd) {
  const p0 = calcProfile(0, d, fs, E, ssd);
  const target = frac * p0;
  // Borne haute : au-delà du bord géométrique du champ
  let lo = 0, hi = (fs / 2) * (ssd + d) / SAD + 10;
  if (calcProfile(hi, d, fs, E, ssd) > target) return hi;
  for (let i = 0; i < 54; i++) {
    const mid = (lo + hi) / 2;
    if (calcProfile(mid, d, fs, E, ssd) > target) lo = mid; else hi = mid;
  }
  return (lo + hi) / 2;
}

function calcMetrics(d, fs, E, ssd) {
  const x50 = findXatFrac(0.50, d, fs, E, ssd);
  const x80 = findXatFrac(0.80, d, fs, E, ssd);
  const x20 = findXatFrac(0.20, d, fs, E, ssd);
  // Taille géométrique = taille à l'isocentre projetée à la profondeur d
  const geom = fs * (ssd + d) / SAD;
  return {
    fieldWidth: (2 * x50).toFixed(1),
    penumbra:   (x20 - x80).toFixed(1),
    geom:       geom.toFixed(1),
  };
}

// ═══════════════════════════════════════════════════════
//  ÉCHELLE DE COULEURS
// ═══════════════════════════════════════════════════════

const CS = [
  [0.00, [  0,   0,   0]],
  [0.05, [  0,   0, 120]],
  [0.20, [  0,  30, 220]],
  [0.40, [  0, 180, 220]],
  [0.60, [ 20, 200,  20]],
  [0.75, [240, 220,   0]],
  [0.90, [255,  90,   0]],
  [1.00, [255,   0,   0]],
];
function toRGB(v) {
  v = Math.max(0, Math.min(1, v));
  let lo = CS[0], hi = CS[CS.length - 1];
  for (let i = 0; i < CS.length - 1; i++) {
    if (v <= CS[i+1][0]) { lo = CS[i]; hi = CS[i+1]; break; }
  }
  const t = (hi[0] - lo[0]) > 0 ? (v - lo[0]) / (hi[0] - lo[0]) : 0;
  return lo[1].map((c, j) => Math.round(c + t * (hi[1][j] - c)));
}

// ═══════════════════════════════════════════════════════
//  RENDU DU FANTÔME 2D
//  (pas de représentation de la tête — fantôme seul)
// ═══════════════════════════════════════════════════════

function renderPhantom(fs, E, ssd) {
  const cv  = document.getElementById('phantom-cv');
  const ctx = cv.getContext('2d');
  const W = cv.width, H = cv.height;

  const img = ctx.createImageData(W, H);
  const px  = img.data;

  // Carte de dose pixel par pixel (plein canvas = fantôme 0→30 cm)
  for (let py = 0; py < H; py++) {
    const d  = (py / H) * DEPTH_MAX;
    const d0 = calcPDD(d, fs, E, ssd);
    const p0 = calcProfile(0, d, fs, E, ssd);
    for (let xi = 0; xi < W; xi++) {
      const x    = (xi / W - 0.5) * 2 * X_HALF;
      const p    = calcProfile(x, d, fs, E, ssd);
      const dose = p0 > 0 ? d0 * p / p0 : 0;
      const [r, g, b] = toRGB(dose / 100);
      const i = (py * W + xi) * 4;
      px[i]=r; px[i+1]=g; px[i+2]=b; px[i+3]=255;
    }
  }
  ctx.putImageData(img, 0, 0);

  // Bords divergents du faisceau (SAD = 100)
  drawBeamEdges(ctx, W, H, fs, ssd);
  // Lignes de profondeur sélectionnées
  drawDepthLines(ctx, W, H);
  // Échelle de profondeur (chiffres, ticks)
  drawDepthScale(ctx, W, H);
}

function drawBeamEdges(ctx, W, H, fs, ssd) {
  // Bords calculés avec divergence depuis la source, FS défini à SAD=100
  const toX = physX => (physX / (2 * X_HALF) + 0.5) * W;
  const toY = d     => (d / DEPTH_MAX) * H;

  ctx.save();
  ctx.setLineDash([5, 5]);
  ctx.strokeStyle = 'rgba(255,255,255,.35)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  // Bord gauche : à la surface, puis au fond
  ctx.moveTo(toX(-(fs/2) * ssd / SAD),                    toY(0));
  ctx.lineTo(toX(-(fs/2) * (ssd + DEPTH_MAX) / SAD),      toY(DEPTH_MAX));
  // Bord droit
  ctx.moveTo(toX( (fs/2) * ssd / SAD),                    toY(0));
  ctx.lineTo(toX( (fs/2) * (ssd + DEPTH_MAX) / SAD),      toY(DEPTH_MAX));
  ctx.stroke();
  ctx.restore();
}

function drawDepthLines(ctx, W, H) {
  ctx.save();
  ctx.setLineDash([7, 4]);
  ctx.lineWidth = 1.5;
  getDepths().forEach((d, i) => {
    if (d < 0 || d > DEPTH_MAX) return;
    const y = (d / DEPTH_MAX) * H;
    ctx.strokeStyle = PCOLS[i];
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = PCOLS[i];
    ctx.font = 'bold 9px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(`d=${d} cm`, 4, y - 2);
    ctx.setLineDash([7, 4]);
  });
  ctx.restore();
}

function drawDepthScale(ctx, W, H) {
  ctx.save();
  ctx.fillStyle = 'rgba(139,148,158,.72)';
  ctx.font = '9px sans-serif';
  ctx.textAlign = 'right';
  for (let d = 0; d <= DEPTH_MAX; d += 5) {
    const y = (d / DEPTH_MAX) * H;
    ctx.fillText(`${d}`, W - 2, y + 3);
    ctx.fillStyle = 'rgba(139,148,158,.25)';
    ctx.fillRect(W - 12, y, 8, 1);
    ctx.fillStyle = 'rgba(139,148,158,.72)';
  }
  ctx.restore();
}

// ═══════════════════════════════════════════════════════
//  BARRE DE COULEURS
// ═══════════════════════════════════════════════════════

function renderColorbar() {
  const cv  = document.getElementById('cb-cv');
  const ctx = cv.getContext('2d');
  const H = cv.height, W = cv.width;
  const img = ctx.createImageData(W, H);
  const d = img.data;
  for (let y = 0; y < H; y++) {
    const [r, g, b] = toRGB(1 - y / H);
    for (let x = 0; x < W; x++) {
      const i = (y * W + x) * 4;
      d[i]=r; d[i+1]=g; d[i+2]=b; d[i+3]=255;
    }
  }
  ctx.putImageData(img, 0, 0);
}

// ═══════════════════════════════════════════════════════
//  SCHÉMA DU DISPOSITIF
// ═══════════════════════════════════════════════════════

function drawSchema(fs, E, ssd) {
  const cv = document.getElementById('schema-cv');
  if (!cv) return;
  const ctx = cv.getContext('2d');
  const W = cv.width, H = cv.height;

  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = '#0d1117';
  ctx.fillRect(0, 0, W, H);

  const cx = W / 2;

  // Positions verticales (représentation compressée)
  const srcY  = 16;   // point source
  const jawY  = 40;   // sortie mâchoires
  const surfY = 100;  // surface du fantôme (d = 0)
  const botY  = H - 10;
  const phantomPx = botY - surfY;
  const scaleY    = phantomPx / DEPTH_MAX;   // px/cm vertical
  const scaleX    = (W - 10) / (2 * X_HALF); // px/cm horizontal

  // ── Position de l'isocentre dans le schéma ──
  const dIso = SAD - ssd; // profondeur de l'isocentre (peut être négatif si SSD > SAD)

  // ── Axe central ──
  ctx.save();
  ctx.strokeStyle = 'rgba(255,255,255,.10)';
  ctx.setLineDash([4, 5]); ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(cx, srcY); ctx.lineTo(cx, botY);
  ctx.stroke(); ctx.restore();

  // ── Bords du faisceau — avec SAD=100 ──
  // Demi-largeur à la surface = (fs/2) × ssd / SAD
  // Demi-largeur au fond      = (fs/2) × (ssd + DEPTH_MAX) / SAD
  const lSurf = cx - (fs/2) * ssd / SAD * scaleX;
  const rSurf = cx + (fs/2) * ssd / SAD * scaleX;
  const lBot  = cx - (fs/2) * (ssd + DEPTH_MAX) / SAD * scaleX;
  const rBot  = cx + (fs/2) * (ssd + DEPTH_MAX) / SAD * scaleX;

  // ── Géométrie des mâchoires (distance source-mâchoires ≈ 40 cm) ──
  const JAW_DIST = 40; // cm depuis la source
  const jawHalfPx = Math.min(cx - 6, (fs / 2) * JAW_DIST / SAD * scaleX);
  const lJaw = cx - jawHalfPx;
  const rJaw = cx + jawHalfPx;

  // Rayonnement absorbé par les mâchoires (triangles source → bords canvas → bord interne mâchoire)
  ctx.save();
  ctx.fillStyle = 'rgba(80,80,100,.18)';
  ctx.beginPath(); ctx.moveTo(cx, srcY); ctx.lineTo(5, jawY); ctx.lineTo(lJaw, jawY); ctx.closePath(); ctx.fill();
  ctx.beginPath(); ctx.moveTo(cx, srcY); ctx.lineTo(W - 5, jawY); ctx.lineTo(rJaw, jawY); ctx.closePath(); ctx.fill();
  ctx.restore();

  // Rayons primaires (source → bord interne mâchoire, très atténués)
  ctx.save();
  ctx.strokeStyle = 'rgba(251,191,36,.15)';
  ctx.setLineDash([2, 4]); ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(cx, srcY); ctx.lineTo(lJaw, jawY);
  ctx.moveTo(cx, srcY); ctx.lineTo(rJaw, jawY);
  ctx.stroke(); ctx.restore();

  // Cône de faisceau utile : mâchoires → surface (rempli + bords tiretés)
  ctx.save();
  ctx.fillStyle = 'rgba(251,191,36,.08)';
  ctx.beginPath();
  ctx.moveTo(lJaw, jawY); ctx.lineTo(lSurf, surfY); ctx.lineTo(rSurf, surfY); ctx.lineTo(rJaw, jawY);
  ctx.closePath(); ctx.fill();
  ctx.strokeStyle = 'rgba(251,191,36,.45)';
  ctx.setLineDash([3, 3]); ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(lJaw, jawY); ctx.lineTo(lSurf, surfY);
  ctx.moveTo(rJaw, jawY); ctx.lineTo(rSurf, surfY);
  ctx.stroke(); ctx.restore();

  // ── Fantôme d'eau ──
  ctx.fillStyle = 'rgba(14, 55, 120, 0.20)';
  ctx.fillRect(5, surfY, W - 10, phantomPx);
  ctx.strokeStyle = '#1e40af'; ctx.setLineDash([]); ctx.lineWidth = 1.5;
  ctx.strokeRect(5, surfY, W - 10, phantomPx);

  // Faisceau dans le fantôme (continu, clippé)
  ctx.save();
  ctx.beginPath(); ctx.rect(5, surfY, W - 10, phantomPx); ctx.clip();
  ctx.strokeStyle = 'rgba(251,191,36,.55)';
  ctx.setLineDash([]); ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(lSurf, surfY); ctx.lineTo(lBot, botY);
  ctx.moveTo(rSurf, surfY); ctx.lineTo(rBot, botY);
  ctx.stroke(); ctx.restore();

  // ── Lignes de profondeur ──
  ctx.save(); ctx.setLineDash([4, 3]); ctx.lineWidth = 1.2;
  getDepths().forEach((d, i) => {
    if (d < 0 || d > DEPTH_MAX) return;
    const y  = surfY + d * scaleY;
    const lx = cx - (fs/2) * (ssd + d) / SAD * scaleX - 4;
    const rx = cx + (fs/2) * (ssd + d) / SAD * scaleX + 4;
    ctx.strokeStyle = PCOLS[i];
    ctx.beginPath();
    ctx.moveTo(Math.max(6, lx), y);
    ctx.lineTo(Math.min(W - 6, rx), y);
    ctx.stroke();
  });
  ctx.restore();

  // ── Isocentre (si dans le fantôme) ──
  if (dIso >= 0 && dIso <= DEPTH_MAX) {
    const isoY = surfY + dIso * scaleY;
    ctx.save();
    ctx.strokeStyle = 'rgba(88,166,255,.75)';
    ctx.setLineDash([2, 2]); ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(5, isoY); ctx.lineTo(W - 5, isoY); ctx.stroke();
    // Croix isocentre sur l'axe
    ctx.strokeStyle = '#58a6ff'; ctx.setLineDash([]); ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(cx - 5, isoY - 5); ctx.lineTo(cx + 5, isoY + 5);
    ctx.moveTo(cx + 5, isoY - 5); ctx.lineTo(cx - 5, isoY + 5);
    ctx.stroke();
    ctx.fillStyle = '#58a6ff'; ctx.font = '8px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('iso', cx + 8, isoY + 3);
    ctx.restore();
  }

  // ── Source ──
  ctx.setLineDash([]);
  const grd = ctx.createRadialGradient(cx, srcY, 0, cx, srcY, 7);
  grd.addColorStop(0, '#fffde7'); grd.addColorStop(1, '#f59e0b');
  ctx.beginPath(); ctx.arc(cx, srcY, 7, 0, Math.PI * 2);
  ctx.fillStyle = grd; ctx.fill();

  // ── Mâchoires (ouverture calée sur la géométrie source-mâchoires) ──
  ctx.fillStyle = '#1e3a5f'; ctx.strokeStyle = '#2d5492'; ctx.lineWidth = 1;
  ctx.fillRect(5, jawY - 10, lJaw - 5, 12);
  ctx.strokeRect(5, jawY - 10, lJaw - 5, 12);
  ctx.fillRect(rJaw, jawY - 10, W - 5 - rJaw, 12);
  ctx.strokeRect(rJaw, jawY - 10, W - 5 - rJaw, 12);

  // ── Flèche DSP ──
  const ax = W - 8;
  const arrowTop = jawY + 4, arrowBot = surfY - 2;
  ctx.strokeStyle = '#8b949e'; ctx.setLineDash([]); ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(ax, arrowTop); ctx.lineTo(ax, arrowBot); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(ax-3, arrowTop+6); ctx.lineTo(ax, arrowTop); ctx.lineTo(ax+3, arrowTop+6); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(ax-3, arrowBot-6); ctx.lineTo(ax, arrowBot); ctx.lineTo(ax+3, arrowBot-6); ctx.stroke();

  // ── Flèche FS à la surface ──
  const fsSurfHalf = (fs/2) * ssd / SAD; // demi-largeur réelle à la surface
  if (rSurf - lSurf > 12) {
    const fy = surfY + 9;
    ctx.strokeStyle = 'rgba(255,255,255,.40)'; ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(Math.max(6, lSurf), fy); ctx.lineTo(Math.min(W-6, rSurf), fy);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(Math.max(6,lSurf)+5,fy-3); ctx.lineTo(Math.max(6,lSurf),fy); ctx.lineTo(Math.max(6,lSurf)+5,fy+3);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(Math.min(W-6,rSurf)-5,fy-3); ctx.lineTo(Math.min(W-6,rSurf),fy); ctx.lineTo(Math.min(W-6,rSurf)-5,fy+3);
    ctx.stroke();
  }

  // ── Labels ──
  ctx.fillStyle = '#8b949e'; ctx.font = '9px sans-serif';
  ctx.textAlign = 'right'; ctx.fillText('Source', cx - 10, srcY + 4);

  // DSP
  const ssdMid = (arrowTop + arrowBot) / 2;
  ctx.textAlign = 'right';
  ctx.fillStyle = '#8b949e'; ctx.fillText('DSP =', ax - 5, ssdMid - 3);
  ctx.fillStyle = '#58a6ff'; ctx.font = 'bold 9px sans-serif';
  ctx.fillText(`${ssd} cm`, ax - 5, ssdMid + 8);

  // FS à la surface
  ctx.fillStyle = 'rgba(255,255,255,.55)'; ctx.font = '8px sans-serif'; ctx.textAlign = 'center';
  ctx.fillText(`${(fsSurfHalf*2).toFixed(1)} cm`, cx, surfY + 21);

  // "FS = X cm @iso" sous le schéma
  ctx.fillStyle = '#58a6ff'; ctx.font = 'bold 8px sans-serif'; ctx.textAlign = 'center';
  ctx.fillText(`FS = ${fs} cm @ iso`, cx, surfY + 32);

  // "Fantôme d'eau"
  ctx.fillStyle = 'rgba(59,130,246,.60)'; ctx.font = '8px sans-serif'; ctx.textAlign = 'left';
  ctx.fillText("Fantôme d'eau", 8, surfY + 48);

  // Échelle profondeur
  ctx.fillStyle = 'rgba(139,148,158,.55)'; ctx.font = '8px sans-serif'; ctx.textAlign = 'right';
  for (let d = 5; d <= DEPTH_MAX; d += 5) {
    const y = surfY + d * scaleY;
    if (y < botY - 4) ctx.fillText(`${d}`, W - 3, y + 3);
  }
  ctx.fillText('cm', W - 3, surfY + 11);
}

// ═══════════════════════════════════════════════════════
//  GRAPHIQUES
// ═══════════════════════════════════════════════════════

let chartPDD = null, chartProf = null;
const GRID_C = 'rgba(48,54,61,.8)', TICK_C = '#8b949e';

const dmaxPlugin = {
  id: 'dmaxLine',
  afterDraw(chart) {
    const { E, fs } = getParams();
    const dmax = getEffDmax(E, fs);
    const xScale = chart.scales.x;
    if (!xScale) return;
    const x = xScale.getPixelForValue(dmax);
    const { top, bottom } = chart.chartArea;
    const ctx = chart.ctx;
    ctx.save();
    ctx.strokeStyle = 'rgba(251,191,36,.7)'; ctx.setLineDash([5, 4]); ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(x, top); ctx.lineTo(x, bottom); ctx.stroke();
    ctx.fillStyle = '#fbbf24'; ctx.font = 'bold 9px sans-serif';
    ctx.textAlign = 'left'; ctx.setLineDash([]);
    ctx.fillText(`d_max=${dmax.toFixed(1)} cm`, x + 4, top + 12);
    ctx.restore();
  }
};

function initCharts() {
  chartPDD = new Chart(document.getElementById('pdd-cv'), {
    type: 'line',
    plugins: [dmaxPlugin],
    data: { datasets: [{ data: [], borderColor: '#38bdf8', backgroundColor: 'rgba(56,189,248,.07)', borderWidth: 2, pointRadius: 0, fill: true, tension: 0.3 }] },
    options: {
      animation: false, responsive: true, maintainAspectRatio: false,
      scales: {
        x: { type: 'linear', min: 0, max: 30, title: { display: true, text: 'Profondeur (cm)', color: TICK_C, font: { size: 11 } }, grid: { color: GRID_C }, ticks: { color: TICK_C } },
        y: { type: 'linear', min: 0, max: 110, title: { display: true, text: 'Dose (%)', color: TICK_C, font: { size: 11 } }, grid: { color: GRID_C }, ticks: { color: TICK_C } }
      },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: {
          title: c => `Profondeur : ${(+c[0].parsed.x).toFixed(1)} cm`,
          label:  c => `PDD = ${(+c.parsed.y).toFixed(1)} %`,
        }}
      }
    }
  });

  chartProf = new Chart(document.getElementById('prof-cv'), {
    type: 'line',
    data: { datasets: [] },
    options: {
      animation: false, responsive: true, maintainAspectRatio: false,
      scales: {
        x: { type: 'linear', title: { display: true, text: 'Position latérale (cm)', color: TICK_C, font: { size: 11 } }, grid: { color: GRID_C }, ticks: { color: TICK_C } },
        y: { type: 'linear', min: 0, max: 115, title: { display: true, text: 'Dose (%)', color: TICK_C, font: { size: 11 } }, grid: { color: GRID_C }, ticks: { color: TICK_C } }
      },
      plugins: {
        legend: { display: true, labels: { color: '#c9d1d9', boxWidth: 20, font: { size: 11 } } },
        tooltip: { mode: 'index', intersect: false, callbacks: {
          title: c => `Position : ${(+c[0].parsed.x).toFixed(1)} cm`,
          label:  c => `${c.dataset.label} : ${(+c.parsed.y).toFixed(1)} %`,
        }}
      }
    }
  });
}

function updatePDDChart(fs, E, ssd) {
  const pts = [];
  for (let d = 0; d <= 30; d += 0.25) pts.push({ x: d, y: calcPDD(d, fs, E, ssd) });
  chartPDD.data.datasets[0].data = pts;
  chartPDD.update('none');
}

function updateProfilesChart(fs, E, ssd) {
  const deps = getDepths();
  const xs = [];
  for (let x = -20; x <= 20; x += 0.25) xs.push(x);
  chartProf.data.datasets = deps.map((d, i) => ({
    label: `d = ${d} cm`,
    data: xs.map(x => ({ x, y: calcDose(x, d, fs, E, ssd) })),
    borderColor: PCOLS[i], backgroundColor: 'transparent',
    borderWidth: 2, pointRadius: 0, tension: 0.3,
  }));
  chartProf.update('none');
}

// ═══════════════════════════════════════════════════════
//  TABLE MÉTRIQUES
// ═══════════════════════════════════════════════════════

function updateMetrics(fs, E, ssd) {
  document.getElementById('metrics-body').innerHTML =
    getDepths().map((d, i) => {
      const m = calcMetrics(d, fs, E, ssd);
      return `<tr>
        <td><span class="dot" style="background:${PCOLS[i]}"></span>${d} cm</td>
        <td><b>${m.fieldWidth}</b> cm</td>
        <td><b>${m.penumbra}</b> cm</td>
        <td>${m.geom} cm</td>
      </tr>`;
    }).join('');
}

// ═══════════════════════════════════════════════════════
//  CONTRÔLES PROFONDEURS
// ═══════════════════════════════════════════════════════

function initDepthControls() {
  const tbl = document.getElementById('depth-tbl');
  [1.5, 5, 10, 20].forEach((d, i) => {
    const sw = Object.assign(document.createElement('div'), { className: 'dswatch' });
    sw.style.background = PCOLS[i];
    const lbl = Object.assign(document.createElement('span'), { className: 'dlabel', textContent: `d${i+1}` });
    const inp = Object.assign(document.createElement('input'), { type: 'number', className: 'dnum', value: d, min: 0, max: 30, step: 0.5 });
    inp.addEventListener('input', refresh);
    const unit = Object.assign(document.createElement('span'), { className: 'dlabel', textContent: 'cm' });
    tbl.append(sw, lbl, inp, unit);
  });
}

function getDepths() {
  return Array.from(document.querySelectorAll('.dnum'))
    .map(el => parseFloat(el.value))
    .filter(d => isFinite(d) && d >= 0 && d <= 30);
}

// ═══════════════════════════════════════════════════════
//  TOOLTIP FANTÔME
// ═══════════════════════════════════════════════════════

function initPhantomHover() {
  const cv = document.getElementById('phantom-cv');
  const tip = document.getElementById('htip');
  cv.addEventListener('mousemove', e => {
    const rect = cv.getBoundingClientRect();
    const px = (e.clientX - rect.left) * cv.width  / rect.width;
    const py = (e.clientY - rect.top)  * cv.height / rect.height;
    const x = (px / cv.width  - 0.5) * 2 * X_HALF;
    const d = (py / cv.height) * DEPTH_MAX;
    const { fs, E, ssd } = getParams();
    tip.style.display = 'block';
    tip.style.left = (e.offsetX + 14) + 'px';
    tip.style.top  = (e.offsetY + 14) + 'px';
    tip.innerHTML = `x = ${x.toFixed(1)} cm<br>d = ${d.toFixed(1)} cm<br><b style="color:#38bdf8">Dose = ${calcDose(x, d, fs, E, ssd).toFixed(1)} %</b>`;
  });
  cv.addEventListener('mouseleave', () => { tip.style.display = 'none'; });
}

// ═══════════════════════════════════════════════════════
//  ÉTAT & RAFRAÎCHISSEMENT
// ═══════════════════════════════════════════════════════

function getParams() {
  return {
    E:   parseInt(document.getElementById('energy').value),
    fs:  parseInt(document.getElementById('fieldSize').value),
    ssd: parseInt(document.getElementById('ssd').value),
  };
}

function updateDisplays() {
  const { fs, ssd, E } = getParams();
  document.getElementById('fs-disp').textContent  = `${fs} × ${fs} cm`;
  document.getElementById('ssd-disp').textContent = `${ssd} cm`;
  const dmax  = getEffDmax(E, fs);
  const pdd10 = calcPDD(10, fs, E, ssd).toFixed(1);
  const pdd20 = calcPDD(20, fs, E, ssd).toFixed(1);
  let d50 = '--';
  for (let d = dmax; d <= 30; d += 0.05)
    if (calcPDD(d, fs, E, ssd) <= 50) { d50 = d.toFixed(1); break; }
  document.getElementById('dmax-info').textContent = `d_max = ${dmax.toFixed(1)} cm`;
  document.getElementById('chips').innerHTML =
    `<span class="chip">d<sub>max</sub> = <b>${dmax.toFixed(1)} cm</b></span>` +
    `<span class="chip">PDD<sub>10</sub> = <b>${pdd10} %</b></span>` +
    `<span class="chip">PDD<sub>20</sub> = <b>${pdd20} %</b></span>` +
    `<span class="chip">D<sub>50</sub> ≈ <b>${d50} cm</b></span>`;
}

function refresh() {
  const { E, fs, ssd } = getParams();
  updateDisplays();
  updatePDDChart(fs, E, ssd);
  updateProfilesChart(fs, E, ssd);
  updateMetrics(fs, E, ssd);
  renderPhantom(fs, E, ssd);
  drawSchema(fs, E, ssd);
}

document.addEventListener('DOMContentLoaded', () => {
  initDepthControls();
  renderColorbar();
  initCharts();
  initPhantomHover();
  document.getElementById('energy').addEventListener('change', refresh);
  document.getElementById('fieldSize').addEventListener('input', refresh);
  document.getElementById('ssd').addEventListener('input', refresh);
  refresh();
});
</script>
</body>
</html>
