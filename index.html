<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WebLinac</title>
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
    .dnum-tp {
      background: var(--surf2); border: 1px solid var(--border); color: var(--text);
      border-radius: 4px; padding: 4px 8px; font-size: 16px; font-weight: 600;
      text-align: center; outline: none; width: 72px;
    }
    .dnum-tp:focus { border-color: var(--accent); }

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
    .profiles-wrap { position: relative; height: 360px; }

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

    /* ── TABS ── */
    .tab-bar { background: var(--surf); border-bottom: 1px solid var(--border); padding: 0 20px; display: flex; gap: 2px; }
    .tab-btn {
      background: none; border: none; border-bottom: 2px solid transparent;
      color: var(--muted); padding: 10px 18px; font-size: 13px; font-weight: 600;
      cursor: pointer; margin-bottom: -1px; transition: color .15s;
    }
    .tab-btn.active { color: var(--accent); border-bottom-color: var(--accent); }
    .tab-btn:hover:not(.active) { color: var(--text); }
    .tab-panel { display: none; }
    .tab-panel.active { display: block; }

    /* ── DOSIMÉTRIE ── */
    .main-dosi {
      padding: 14px 20px;
      display: grid;
      grid-template-columns: 216px 1fr 340px;
      gap: 14px;
    }
    .electro-wrap {
      background: #020c02;
      border: 2px solid #0c2b0c;
      border-radius: 8px;
      padding: 16px 14px;
      text-align: center;
    }
    .electro-screen {
      font-family: 'Courier New', monospace;
      font-size: 46px; font-weight: 700;
      color: #00e536;
      text-shadow: 0 0 16px rgba(0,229,54,.55);
      letter-spacing: 4px;
      display: block;
      padding: 8px 14px;
      background: #010901;
      border-radius: 4px;
    }
    .electro-unit { font-size: 11px; color: #00a025; margin-top: 4px; letter-spacing: .12em; text-transform: uppercase; }
    .mu-screen { font-family: 'Courier New', monospace; font-size: 17px; color: #fbbf24; text-shadow: 0 0 8px rgba(251,191,36,.4); margin-top: 10px; }
    .kq-table { border-collapse: collapse; font-size: 11px; width: 100%; }
    .kq-table th { background: var(--surf2); color: var(--muted); font-weight: 700; letter-spacing: .04em; padding: 4px 7px; border: 1px solid var(--border); text-align: center; font-size: 10px; white-space: nowrap; }
    .kq-table td { padding: 3px 7px; border: 1px solid var(--border); text-align: center; color: var(--muted); font-size: 11px; }
    .kq-table td.det-name { text-align: left; color: var(--text); font-weight: 600; white-space: nowrap; min-width: 90px; }
    .kq-table tr.det-active td { color: var(--text); }
    .kq-table td.kq-active { background: rgba(88,166,255,.20); color: #fff; font-weight: 800; border-color: rgba(88,166,255,.5); }
    .kq-table tr.det-active td.kq-active { background: rgba(88,166,255,.38); color: #e2f0ff; font-weight: 800; }
    .beam-btn {
      width: 100%; padding: 13px;
      background: #15803d; border: none; border-radius: 8px;
      color: #fff; font-size: 16px; font-weight: 800;
      letter-spacing: .07em; cursor: pointer; margin-top: 10px;
    }
    .beam-btn.on { background: #b91c1c; }
    .beam-btn:hover { filter: brightness(1.1); }
    .zero-btn {
      width: 100%; padding: 6px;
      background: var(--surf2); border: 1px solid var(--border);
      border-radius: 6px; color: var(--muted); font-size: 12px;
      cursor: pointer; margin-top: 8px;
    }
    .zero-btn:hover { background: var(--border); color: var(--text); }
    .calc-step { display: flex; justify-content: space-between; align-items: baseline; padding: 5px 0; border-bottom: 1px solid rgba(48,54,61,.5); font-size: 12px; }
    .calc-step:last-child { border-bottom: none; }
    .calc-step .cl { color: var(--muted); }
    .calc-step .cv { color: var(--accent); font-weight: 700; font-family: 'Courier New', monospace; font-size: 11px; }
    .calc-result { margin-top: 10px; padding: 10px; background: rgba(88,166,255,.06); border: 1px solid rgba(88,166,255,.2); border-radius: 6px; text-align: center; }
    .calc-result .big { font-size: 20px; font-weight: 700; color: var(--accent); font-family: 'Courier New', monospace; }
    .det-info { font-size: 11px; color: var(--muted); line-height: 1.8; margin-top: 8px; }
    .det-info b { color: var(--text); }
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

<div class="tab-bar">
  <button class="tab-btn active" data-tab="photons">Photons</button>
  <button class="tab-btn"        data-tab="electrons">Électrons</button>
  <button class="tab-btn"        data-tab="dosimetry">Dosimétrie</button>
</div>

<div id="panel-photons" class="tab-panel active">
<div class="ctrls">
  <div class="ctrl">
    <label>Énergie nominale</label>
    <select id="energy">
      <option value="4">4 MV</option>
      <option value="6" selected>6 MV</option>
      <option value="6fff">6 MV FFF</option>
      <option value="10">10 MV</option>
      <option value="10fff">10 MV FFF</option>
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
</div><!-- /panel-photons -->

<div id="panel-electrons" class="tab-panel">
<div class="ctrls">
  <div class="ctrl">
    <label>Énergie nominale</label>
    <select id="e-energy">
      <option value="4">4 MeV</option>
      <option value="6" selected>6 MeV</option>
      <option value="8">8 MeV</option>
      <option value="10">10 MeV</option>
      <option value="12">12 MeV</option>
      <option value="15">15 MeV</option>
      <option value="18">18 MeV</option>
      <option value="20">20 MeV</option>
    </select>
  </div>
  <div class="ctrl">
    <label>Applicateur</label>
    <select id="e-appSize">
      <option value="6">6 × 6 cm</option>
      <option value="10" selected>10 × 10 cm</option>
      <option value="14">14 × 14 cm</option>
      <option value="20">20 × 20 cm</option>
      <option value="25">25 × 25 cm</option>
    </select>
  </div>
  <div class="ctrl">
    <label>Profondeurs des profils</label>
    <div class="depth-tbl" id="e-depth-tbl"></div>
  </div>
</div>
</div><!-- /panel-electrons -->

<div id="panel-dosimetry" class="tab-panel">
  <div style="display:flex;gap:14px;padding:14px 20px 0">

    <!-- ── Paramètres machine ── -->
    <div class="card" style="flex:1;min-width:0">
      <div class="card-hdr">Paramètres machine</div>
      <div class="card-body" style="display:flex;flex-wrap:wrap;gap:18px 28px;align-items:flex-start">
        <div class="ctrl">
          <label>Type de faisceau</label>
          <select id="d-btype">
            <option value="photons">Photons</option>
            <option value="electrons">Électrons</option>
          </select>
        </div>
        <div class="ctrl">
          <label>Énergie</label>
          <select id="d-energy"></select>
        </div>
        <div class="ctrl" id="d-fs-ctrl">
          <label>Taille de champ</label>
          <div class="slider-row">
            <input type="range" id="d-fs" min="2" max="30" step="1" value="10">
            <span class="sval" id="d-fs-disp">10 × 10 cm</span>
          </div>
        </div>
        <div class="ctrl" id="d-app-ctrl" style="display:none">
          <label>Applicateur</label>
          <select id="d-app">
            <option value="6">6 × 6 cm</option>
            <option value="10" selected>10 × 10 cm</option>
            <option value="14">14 × 14 cm</option>
            <option value="20">20 × 20 cm</option>
            <option value="25">25 × 25 cm</option>
          </select>
        </div>
        <div class="ctrl">
          <label>Nombre d'UM</label>
          <div class="slider-row">
            <input type="number" id="d-mu" min="1" max="999" step="1" value="100" class="dnum" style="width:60px">
            <span class="dlabel">UM</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Paramètres de mesure ── -->
    <div class="card" style="flex:1;min-width:0">
      <div class="card-hdr">Paramètres de mesure</div>
      <div class="card-body" style="display:flex;flex-wrap:wrap;gap:18px 28px;align-items:flex-start">
        <div class="ctrl">
          <label>Profondeur</label>
          <div class="slider-row">
            <input type="number" id="d-depth" min="0" max="30" step="0.5" value="10" class="dnum" style="width:60px">
            <span class="dlabel">cm</span>
          </div>
        </div>
        <div class="ctrl" id="d-ssd-ctrl">
          <label>Distance Source-Surface (DSP)</label>
          <div class="slider-row">
            <input type="range" id="d-ssd" min="80" max="120" step="5" value="100">
            <span class="sval" id="d-ssd-disp">100 cm</span>
          </div>
        </div>
        <div class="ctrl">
          <label>Température</label>
          <div class="slider-row">
            <input type="number" id="d-temp" min="10" max="35" step="0.1" value="20" class="dnum-tp">
            <span class="dlabel" style="font-size:13px">°C</span>
          </div>
        </div>
        <div class="ctrl">
          <label>Pression</label>
          <div class="slider-row">
            <input type="number" id="d-pres" min="960" max="1060" step="0.1" value="1013" class="dnum-tp" style="width:82px">
            <span class="dlabel" style="font-size:13px">hPa</span>
          </div>
        </div>
      </div>
    </div>

  </div>

  <div class="main-dosi">

    <!-- Détecteur -->
    <div class="card">
      <div class="card-hdr">Détecteur</div>
      <div class="card-body">
        <select id="d-detector" style="width:100%;background:var(--surf2);border:1px solid var(--border);color:var(--text);border-radius:6px;padding:5px 8px;font-size:12px;outline:none;margin-bottom:8px"></select>
        <div style="display:flex;justify-content:center;margin:6px 0">
          <canvas id="det-cv" width="196" height="148"></canvas>
        </div>
        <div class="det-info" id="det-info"></div>
      </div>
    </div>

    <!-- Électromètre -->
    <div class="card">
      <div class="card-hdr">Électromètre</div>
      <div class="card-body" style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0">
        <div class="electro-wrap" style="width:100%;max-width:360px">
          <div style="font-size:9px;color:#3a6a3a;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px">Charge collectée</div>
          <span class="electro-screen" id="electro-display">0.000</span>
          <div class="electro-unit">nC</div>
        </div>
        <div style="width:100%;max-width:360px">
          <button class="zero-btn" onclick="zeroDosimetry()">⊘ Remise à zéro</button>
        </div>
      </div>
    </div>

    <!-- Schéma du dispositif -->
    <div class="card">
      <div class="card-hdr">Schéma du dispositif</div>
      <div class="card-body" style="padding:8px 10px;display:flex;flex-direction:column;align-items:center;gap:10px">
        <canvas id="dosi-schema-cv" width="308" height="326" style="display:block;border-radius:4px"></canvas>
        <div class="mu-screen" style="width:100%;max-width:308px;text-align:center">UM : <span id="mu-counter">0</span> / <span id="mu-total">100</span></div>
        <button class="beam-btn" id="beam-btn" onclick="toggleBeam()" style="width:100%;max-width:308px">▶  BEAM ON</button>
      </div>
    </div>

  </div>

  <!-- Tableau kQ,Q0 -->
  <div style="padding:0 20px 16px">
    <div class="card">
      <div class="card-hdr">Facteurs de qualité k<sub>Q,Q0</sub> — référence Co-60 &nbsp;<span style="font-size:10px;font-weight:400;color:var(--muted)">(TRS 398 — la cellule active est surlignée)</span></div>
      <div class="card-body" style="display:flex;gap:24px;flex-wrap:wrap;align-items:flex-start">
        <div style="flex:1;min-width:280px">
          <div style="font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px">Photons</div>
          <table class="kq-table" id="kq-photons-table"></table>
        </div>
        <div style="flex:1;min-width:300px">
          <div style="font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px">Électrons</div>
          <table class="kq-table" id="kq-electrons-table"></table>
        </div>
      </div>
    </div>
  </div>

</div><!-- /panel-dosimetry -->

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
          <thead id="metrics-head">
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
//  DOSIMÉTRIE PONCTUELLE
// ═══════════════════════════════════════════════════════

// kQ,Q0 : facteurs de qualité TRS 398 (référence Co-60), photons TPR20/10-interpolés, électrons R50-interpolés
const DETECTORS = [
  { name: 'Farmer — 0.6 cc',     model: 'PTW 30013',  volume: 0.600, shape: 'cyl',
    r_eff: 0.305,  // rayon effectif transverse de la cavité (cm) — pour le moyennage volumique
    ndw: 4.94,     // N_D,w,Q0 en cGy/nC (Co-60)
    kQ: {
      photons:   { '4':0.988, '6':0.982, '6fff':0.983, '10':0.975, '10fff':0.976, '15':0.971, '18':0.968 },
      electrons: { '4':0.904, '6':0.921, '8':0.935, '10':0.946, '12':0.954, '15':0.963, '18':0.970, '20':0.973 }
    }
  },
  { name: 'CC13 — 0.13 cc',      model: 'IBA CC13',   volume: 0.130, shape: 'cyl',
    r_eff: 0.225,
    ndw: 22.4,
    kQ: {
      photons:   { '4':0.989, '6':0.983, '6fff':0.984, '10':0.976, '10fff':0.977, '15':0.972, '18':0.969 },
      electrons: { '4':0.907, '6':0.923, '8':0.937, '10':0.948, '12':0.956, '15':0.965, '18':0.971, '20':0.974 }
    }
  },
  { name: 'Markus — 0.055 cc',   model: 'PTW 34045',  volume: 0.055, shape: 'pp',
    r_eff: 0.265,  // rayon de l'électrode collectrice (Ø 5,3 mm / 2)
    ndw: 53.1,
    kQ: {
      photons:   { '4':0.993, '6':0.989, '6fff':0.989, '10':0.984, '10fff':0.984, '15':0.981, '18':0.979 },
      electrons: { '4':1.052, '6':1.038, '8':1.028, '10':1.020, '12':1.014, '15':1.008, '18':1.004, '20':1.002 }
    }
  },
  { name: 'PinPoint — 0.016 cc', model: 'PTW 31016',  volume: 0.016, shape: 'cyl',
    r_eff: 0.145,
    ndw: 182,
    kQ: {
      photons:   { '4':0.987, '6':0.981, '6fff':0.980, '10':0.973, '10fff':0.972, '15':0.969, '18':0.966 },
      electrons: { '4':0.900, '6':0.917, '8':0.931, '10':0.943, '12':0.951, '15':0.961, '18':0.967, '20':0.970 }
    }
  },
];

// ── Moyennage volumique (volume averaging) ──────────────────────────────────
// Largeur σ de la pénombre gaussienne (cm) selon l'énergie
function sigmaPenumbra(btype, E) {
  if (btype === 'electrons') return 0.50;
  return { '4':0.40, '6':0.35, '6fff':0.27, '10':0.42, '10fff':0.31, '15':0.48, '18':0.52 }[String(E)] ?? 0.40;
}

// k_vol : rapport dose moyennée sur la cavité / dose au centre (intégrale 1D, Riemann médian)
// Modèle : profil = 0.5·[erf((a+x)/√2σ) + erf((a-x)/√2σ)], a = FS/2
function computeKvol(r_eff, FS, sigma_p) {
  if (r_eff <= 0 || FS <= 0 || sigma_p <= 0) return 1;
  const a = FS / 2;
  const sq2s = Math.SQRT2 * sigma_p;
  const D0 = erf(a / sq2s);           // dose normalisée au centre
  if (D0 < 1e-4) return 1;
  const N = 80;
  let sum = 0;
  for (let i = 0; i < N; i++) {
    const x = r_eff * (-1 + (2 * i + 1) / N);   // points milieux sur [-r_eff, r_eff]
    sum += 0.5 * (erf((a + x) / sq2s) + erf((a - x) / sq2s));
  }
  return Math.min(1, (sum / N) / D0);
}
// ────────────────────────────────────────────────────────────────────────────

function photonOutputFactor(E, fs) {
  const k = { '4': 0.0045, '6': 0.006, '6fff': 0.0065, '10': 0.007, '10fff': 0.0075, '15': 0.008, '18': 0.0085 }[E] ?? 0.006;
  return Math.max(0.65, 1 + k * (fs - 10));
}

// Calcule R50 numériquement depuis la courbe calcElectronPDD (bisection)
function computeElectronR50(fs, Emev) {
  let lo = 0.05, hi = 22;
  for (let i = 0; i < 60; i++) {
    const mid = (lo + hi) / 2;
    if (calcElectronPDD(mid, fs, Emev) > 50) lo = mid; else hi = mid;
  }
  return (lo + hi) / 2;
}

function getDosimetryResult() {
  const btype  = document.getElementById('d-btype').value;
  const E      = document.getElementById('d-energy').value;
  const ssd    = parseInt(document.getElementById('d-ssd').value) || 100;
  const fs     = btype === 'electrons'
    ? parseInt(document.getElementById('d-app').value)
    : parseFloat(document.getElementById('d-fs').value);
  const depth  = parseFloat(document.getElementById('d-depth').value) || 0;
  const MU     = Math.max(1, parseInt(document.getElementById('d-mu').value) || 100);
  const temp   = parseFloat(document.getElementById('d-temp').value) || 20;
  const pres   = parseFloat(document.getElementById('d-pres').value) || 1013;
  const detIdx = parseInt(document.getElementById('d-detector').value);
  const det    = DETECTORS[detIdx];

  // TRS 398 — kTP : T_réf = 20°C = 293.15 K, P_réf = 1013.25 hPa
  const kTP = ((273.15 + temp) / 293.15) * (1013.25 / pres);

  let dose_cGy, OF, z_ref;
  if (btype === 'electrons') {
    // TRS 398 §10 : z_ref = 0.6·R50 − 0.1 cm, R50 issu de la PDD simulée (applicateur sélectionné)
    const r50_eff = computeElectronR50(fs, E);
    z_ref    = Math.max(0.1, +(0.6 * r50_eff - 0.1).toFixed(2));
    OF       = 1.0;
    dose_cGy = MU * (calcElectronPDD(depth, fs, E) / calcElectronPDD(z_ref, fs, E));
  } else {
    // TRS 398 §9 : z_ref = 10 cm, FS = 10×10 cm, SSD_réf = 90 cm (DSD = 100 cm)
    z_ref    = 10;
    OF       = photonOutputFactor(E, fs);
    dose_cGy = MU * OF * (calcPDD(depth, fs, E, ssd) / calcPDD(z_ref, 10, E, 90));
  }

  // TRS 398 : M_raw = D / (N_D,w × kQ,Q0 × kTP)  — ce que l'électromètre affiche (non corrigé kTP)
  const kQ_map = btype === 'electrons' ? det.kQ.electrons : det.kQ.photons;
  const kQ     = kQ_map[String(E)] ?? (btype === 'electrons' ? 0.95 : 0.98);

  // Moyennage volumique : la chambre mesure la dose moyennée sur sa cavité, pas la dose au centre
  const sigma_p = sigmaPenumbra(btype, E);
  const k_vol   = computeKvol(det.r_eff, fs, sigma_p);
  const charge  = Math.max(0, dose_cGy * k_vol / (det.ndw * kQ * kTP));
  return { btype, E, fs, ssd, depth, MU, temp, pres, det, kTP, z_ref, OF, dose_cGy, kQ, k_vol, charge };
}

// Détecteur dans le schéma du dispositif — formes simples à l'échelle du fantôme
// Échelle : 1 cm ≈ 6.87 px (fantôme 30 cm / 206 px) × facteur ×2 pour lisibilité
function drawDetInSchema(ctx, cx, measY, det, depth) {
  ctx.save();
  ctx.fillStyle = 'rgba(74,222,128,.28)';
  ctx.strokeStyle = '#4ade80'; ctx.lineWidth = 1; ctx.setLineDash([]);

  if (det.shape === 'cyl') {
    const R = Math.max(4, Math.round(det.r_eff * 2.2 * 14)); // rayon outer en px
    ctx.beginPath(); ctx.arc(cx, measY, R, 0, Math.PI * 2);
    ctx.fill(); ctx.stroke();
    ctx.fillStyle = '#4ade80'; ctx.font = 'bold 7px sans-serif'; ctx.textAlign = 'left';
    ctx.fillText(`d = ${depth} cm`, cx + R + 4, measY + 3);
  } else {
    const w = 12, h = 3; // Markus : fine plaque rectangulaire
    ctx.fillRect(cx - w / 2, measY - h / 2, w, h);
    ctx.strokeRect(cx - w / 2, measY - h / 2, w, h);
    ctx.fillStyle = '#4ade80'; ctx.font = 'bold 7px sans-serif'; ctx.textAlign = 'left';
    ctx.fillText(`d = ${depth} cm`, cx + w / 2 + 4, measY + 3);
  }
  ctx.restore();
}

function drawDosimetrySchema(btype, E, fs, ssd, depth) {
  const cv = document.getElementById('dosi-schema-cv');
  if (!cv) return;
  const ctx = cv.getContext('2d');
  const W = cv.width, H = cv.height;
  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = '#0d1117'; ctx.fillRect(0, 0, W, H);

  const cx = W / 2;
  const srcY = 16, jawY = 58, surfY = 106, botY = H - 14;
  const phantomPx = botY - surfY;
  const scaleY    = phantomPx / DEPTH_MAX;
  const scaleX    = (W - 14) / (2 * X_HALF);
  const ssdEff    = btype === 'electrons' ? 100 : ssd;

  const lSurf = cx - (fs/2) * ssdEff / SAD * scaleX;
  const rSurf = cx + (fs/2) * ssdEff / SAD * scaleX;
  const lBot  = cx - (fs/2) * (ssdEff + DEPTH_MAX) / SAD * scaleX;
  const rBot  = cx + (fs/2) * (ssdEff + DEPTH_MAX) / SAD * scaleX;
  const JAW_DIST  = 40;
  const jawHalfPx = Math.min(cx - 6, (fs/2) * JAW_DIST / SAD * scaleX);
  const lJaw = cx - jawHalfPx, rJaw = cx + jawHalfPx;

  // Axe central
  ctx.save(); ctx.strokeStyle = 'rgba(255,255,255,.10)'; ctx.setLineDash([3,4]); ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(cx, srcY); ctx.lineTo(cx, botY); ctx.stroke(); ctx.restore();

  // Zone absorbée mâchoires
  ctx.save(); ctx.fillStyle = 'rgba(80,80,100,.18)';
  ctx.beginPath(); ctx.moveTo(cx,srcY); ctx.lineTo(5,jawY); ctx.lineTo(lJaw,jawY); ctx.closePath(); ctx.fill();
  ctx.beginPath(); ctx.moveTo(cx,srcY); ctx.lineTo(W-5,jawY); ctx.lineTo(rJaw,jawY); ctx.closePath(); ctx.fill();
  ctx.restore();

  const beamC = btype === 'electrons' ? 'rgba(100,220,255,' : 'rgba(251,191,36,';

  // Cône utile
  ctx.save();
  ctx.fillStyle = beamC + '.07)';
  ctx.beginPath(); ctx.moveTo(lJaw,jawY); ctx.lineTo(lSurf,surfY); ctx.lineTo(rSurf,surfY); ctx.lineTo(rJaw,jawY); ctx.closePath(); ctx.fill();
  ctx.strokeStyle = beamC + '.40)'; ctx.setLineDash([3,3]); ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(lJaw,jawY); ctx.lineTo(lSurf,surfY); ctx.moveTo(rJaw,jawY); ctx.lineTo(rSurf,surfY); ctx.stroke(); ctx.restore();

  if (btype === 'electrons') {
    const foilTopY = srcY + 8, foilW = Math.min(cx - 8, jawHalfPx + 6);
    ctx.save();
    [foilTopY, foilTopY + (jawY - 14 - foilTopY) / 2].forEach(fy => {
      const g = ctx.createLinearGradient(cx-foilW,0,cx+foilW,0);
      g.addColorStop(0,'rgba(80,120,80,.10)'); g.addColorStop(.5,'rgba(200,255,200,.75)'); g.addColorStop(1,'rgba(80,120,80,.10)');
      ctx.fillStyle = g; ctx.strokeStyle = 'rgba(160,230,160,.70)'; ctx.lineWidth = 1; ctx.setLineDash([]);
      ctx.beginPath(); ctx.rect(cx-foilW, fy, foilW*2, 3); ctx.fill(); ctx.stroke();
    });
    const appW = Math.min(cx - 6, (fs/2) * scaleX);
    ctx.strokeStyle = 'rgba(251,146,60,.80)'; ctx.lineWidth = 1.5; ctx.setLineDash([]);
    ctx.beginPath(); ctx.moveTo(cx-appW, surfY-22); ctx.lineTo(cx-appW, surfY);
    ctx.moveTo(cx+appW, surfY-22); ctx.lineTo(cx+appW, surfY); ctx.stroke(); ctx.restore();
  } else {
    const { fff = false } = BEAM[E] ?? BEAM['6'];
    const fTopY = srcY + 8, fBotY = jawY - 12;
    const fHalf = Math.min(cx - 12, (30/2) * JAW_DIST / SAD * scaleX);
    ctx.save();
    ctx.beginPath(); ctx.moveTo(cx-2,fTopY); ctx.lineTo(cx-fHalf,fBotY); ctx.lineTo(cx+fHalf,fBotY); ctx.lineTo(cx+2,fTopY); ctx.closePath();
    if (!fff) {
      const fg = ctx.createLinearGradient(cx-fHalf,0,cx+fHalf,0);
      fg.addColorStop(0,'rgba(60,70,95,.10)'); fg.addColorStop(.5,'rgba(205,220,245,.88)'); fg.addColorStop(1,'rgba(60,70,95,.10)');
      ctx.fillStyle = fg; ctx.fill();
    }
    ctx.strokeStyle = fff ? 'rgba(251,146,60,.50)' : 'rgba(200,215,240,.80)';
    ctx.lineWidth = 1; ctx.setLineDash(fff ? [3,3] : []); ctx.stroke(); ctx.restore();
  }

  // Mâchoires
  ctx.setLineDash([]); ctx.fillStyle = '#1e3a5f'; ctx.strokeStyle = '#2d5492'; ctx.lineWidth = 1;
  ctx.fillRect(5,jawY-8,lJaw-5,10); ctx.strokeRect(5,jawY-8,lJaw-5,10);
  ctx.fillRect(rJaw,jawY-8,W-5-rJaw,10); ctx.strokeRect(rJaw,jawY-8,W-5-rJaw,10);

  // Fantôme d'eau
  ctx.fillStyle = 'rgba(14,55,120,.20)'; ctx.fillRect(5,surfY,W-10,phantomPx);
  ctx.strokeStyle = '#1e40af'; ctx.lineWidth = 1.5; ctx.strokeRect(5,surfY,W-10,phantomPx);

  // Faisceau dans le fantôme
  ctx.save(); ctx.beginPath(); ctx.rect(5,surfY,W-10,phantomPx); ctx.clip();
  ctx.strokeStyle = beamC+'.45)'; ctx.setLineDash([]); ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(lSurf,surfY); ctx.lineTo(lBot,botY);
  ctx.moveTo(rSurf,surfY); ctx.lineTo(rBot,botY); ctx.stroke(); ctx.restore();

  // z_ref TRS 398 (jaune tirets) — pour les électrons dérivé de la R50 de la PDD simulée
  const z_ref = btype === 'electrons'
    ? Math.max(0.1, 0.6 * computeElectronR50(fs, E) - 0.1)
    : 10;
  if (z_ref <= DEPTH_MAX) {
    const zrefY = surfY + z_ref * scaleY;
    ctx.save(); ctx.strokeStyle = '#fbbf24'; ctx.setLineDash([4,3]); ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(5,zrefY); ctx.lineTo(W-5,zrefY); ctx.stroke();
    ctx.fillStyle = '#fbbf24'; ctx.font = '7px sans-serif'; ctx.textAlign = 'left'; ctx.setLineDash([]);
    ctx.fillText(`z_réf = ${z_ref.toFixed(1)} cm`, 7, zrefY - 2); ctx.restore();
  }

  // Profondeur de mesure + représentation réaliste du détecteur
  if (depth >= 0 && depth <= DEPTH_MAX) {
    const measY = surfY + depth * scaleY;
    const det   = DETECTORS[parseInt(document.getElementById('d-detector').value)];
    // Ligne de profondeur
    ctx.save();
    ctx.strokeStyle = '#4ade80'; ctx.setLineDash([3, 3]); ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(5, measY); ctx.lineTo(W - 5, measY); ctx.stroke();
    ctx.restore();
    drawDetInSchema(ctx, cx, measY, det, depth);
  }

  // Source
  ctx.setLineDash([]);
  const grd = ctx.createRadialGradient(cx,srcY,0,cx,srcY,6);
  grd.addColorStop(0,'#fffde7'); grd.addColorStop(1,'#f59e0b');
  ctx.beginPath(); ctx.arc(cx,srcY,6,0,Math.PI*2); ctx.fillStyle = grd; ctx.fill();

  // Flèche DSP
  const ax = W - 8, arrowTop = jawY + 4, arrowBot = surfY - 2;
  ctx.strokeStyle = '#8b949e'; ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(ax,arrowTop); ctx.lineTo(ax,arrowBot); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(ax-3,arrowTop+5); ctx.lineTo(ax,arrowTop); ctx.lineTo(ax+3,arrowTop+5); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(ax-3,arrowBot-5); ctx.lineTo(ax,arrowBot); ctx.lineTo(ax+3,arrowBot-5); ctx.stroke();
  const ssdMid = (arrowTop + arrowBot) / 2;
  ctx.fillStyle = '#8b949e'; ctx.font = '7px sans-serif'; ctx.textAlign = 'right';
  ctx.fillText('DSP', ax-4, ssdMid-2);
  ctx.fillStyle = '#58a6ff'; ctx.font = 'bold 7px sans-serif';
  ctx.fillText(`${ssdEff} cm`, ax-4, ssdMid+8);
  // Pour les photons : rappel DSD = DSP + z_réf = 100 cm
  if (btype !== 'electrons') {
    const dsdVal = ssdEff + 10;
    ctx.fillStyle = 'rgba(251,191,36,.55)'; ctx.font = '6px sans-serif';
    ctx.fillText(`DSD réf = ${dsdVal} cm`, ax-4, ssdMid+18);
  }

  // Labels divers
  ctx.fillStyle = '#8b949e'; ctx.font = '8px sans-serif'; ctx.textAlign = 'right';
  ctx.fillText('Source', cx-8, srcY+4);
  ctx.fillStyle = 'rgba(59,130,246,.55)'; ctx.font = '7px sans-serif'; ctx.textAlign = 'left';
  ctx.fillText("Fantôme d'eau", 7, surfY+36);
  ctx.fillStyle = 'rgba(255,255,255,.40)'; ctx.font = '7px sans-serif'; ctx.textAlign = 'center';
  ctx.fillText(`${((fs/2)*ssdEff/SAD*2).toFixed(1)} cm`, cx, surfY+14);
  ctx.fillStyle = 'rgba(139,148,158,.48)'; ctx.font = '7px sans-serif'; ctx.textAlign = 'left';
  for (let d = 5; d <= DEPTH_MAX; d += 5) {
    const y = surfY + d * scaleY;
    if (y < botY - 3) ctx.fillText(`${d}`, 7, y+3);
  }
}

function drawDetectorSchema(det) {
  const cv = document.getElementById('det-cv');
  if (!cv) return;
  const ctx = cv.getContext('2d');
  const W = cv.width, H = cv.height;
  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = '#0d1117'; ctx.fillRect(0, 0, W, H);
  const cx = W / 2, cy = H / 2 - 6;

  if (det.shape === 'cyl') {
    // Vue axiale (coupe ⊥ à l'axe) — cercles concentriques
    // Rout proportionnel au volume : Farmer 0.6cc→46, CC13 0.13→28, PinPoint 0.016→17
    const Rout = Math.max(16, Math.min(46, det.volume * 50 + 18));
    // Paroi fine : ~8 % du rayon (réaliste PMMA ~0.5 mm)
    const wallPx = Math.max(2, Rout * 0.08);
    const Rin  = Rout - wallPx;          // bord intérieur de la paroi
    const Rcol = Rin  * 0.90;            // cavité collectrice (occupe 90 % du rayon interne)
    const rEl  = Math.max(1.5, Rin * 0.08); // électrode centrale fine

    // Faisceau entrant
    ctx.save();
    ctx.strokeStyle = 'rgba(251,191,36,.45)'; ctx.fillStyle = 'rgba(251,191,36,.35)';
    ctx.lineWidth = 1; ctx.setLineDash([3,3]);
    const fTop = 6, fBot = cy - Rout - 5;
    ctx.beginPath();
    ctx.moveTo(cx - Rout*0.55, fTop); ctx.lineTo(cx - Rout*0.55, fBot);
    ctx.moveTo(cx + Rout*0.55, fTop); ctx.lineTo(cx + Rout*0.55, fBot);
    ctx.stroke();
    ctx.setLineDash([]); ctx.lineWidth = 1.4;
    ctx.beginPath(); ctx.moveTo(cx, fTop); ctx.lineTo(cx, fBot); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(cx-6, fBot+1); ctx.lineTo(cx, fBot+6); ctx.lineTo(cx+6, fBot+1); ctx.fill();
    ctx.restore();

    // Paroi extérieure (anneau métallique / PMMA)
    const gOut = ctx.createRadialGradient(cx - Rout*0.28, cy - Rout*0.28, 1, cx, cy, Rout);
    gOut.addColorStop(0, 'rgba(190,205,225,.90)');
    gOut.addColorStop(0.55, 'rgba(110,130,165,.70)');
    gOut.addColorStop(1, 'rgba(50,65,95,.45)');
    ctx.fillStyle = gOut; ctx.strokeStyle = 'rgba(160,180,210,.85)'; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.arc(cx, cy, Rout, 0, Math.PI*2); ctx.fill(); ctx.stroke();

    // Cavité intérieure (fond sombre)
    ctx.fillStyle = '#0a1020';
    ctx.beginPath(); ctx.arc(cx, cy, Rin, 0, Math.PI*2); ctx.fill();
    ctx.strokeStyle = 'rgba(100,120,155,.40)'; ctx.lineWidth = 0.8;
    ctx.beginPath(); ctx.arc(cx, cy, Rin, 0, Math.PI*2); ctx.stroke();

    // Volume collecteur (gaz / air)
    ctx.fillStyle = 'rgba(56,189,248,.18)'; ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 1.2;
    ctx.beginPath(); ctx.arc(cx, cy, Rcol, 0, Math.PI*2); ctx.fill(); ctx.stroke();

    // Électrode centrale fine
    const gEl = ctx.createRadialGradient(cx, cy, 0, cx, cy, rEl);
    gEl.addColorStop(0, '#fde68a'); gEl.addColorStop(1, '#b45309');
    ctx.fillStyle = gEl;
    ctx.beginPath(); ctx.arc(cx, cy, rEl, 0, Math.PI*2); ctx.fill();

    // Labels
    ctx.fillStyle = '#38bdf8'; ctx.font = 'bold 10px sans-serif'; ctx.textAlign = 'center';
    ctx.fillText('Cavité active', cx, cy + Rout + 16);
    ctx.fillStyle = 'rgba(253,230,138,.85)'; ctx.font = '9px sans-serif';
    ctx.fillText('Électrode', cx, cy + rEl + 11);
    ctx.fillStyle = 'rgba(200,210,230,.50)'; ctx.font = '9px sans-serif'; ctx.textAlign = 'right';
    ctx.fillText('Vue axiale ⊥ faisceau', W - 4, H - 4);

  } else {
    // Plan-parallèle : coupe sagittale dans le sens du faisceau
    const w = 148, gap = 14, thin = 5, guard = 14;
    const topY = cy - gap/2 - thin;

    // Faisceau entrant
    ctx.save();
    ctx.strokeStyle = 'rgba(251,191,36,.40)'; ctx.fillStyle = 'rgba(251,191,36,.30)';
    ctx.lineWidth = 1; ctx.setLineDash([3,3]);
    const fTop = 6, fBot = topY - 5;
    ctx.beginPath();
    ctx.moveTo(cx - w*0.38, fTop); ctx.lineTo(cx - w*0.38, fBot);
    ctx.moveTo(cx + w*0.38, fTop); ctx.lineTo(cx + w*0.38, fBot);
    ctx.stroke();
    ctx.setLineDash([]); ctx.lineWidth = 1.4;
    ctx.beginPath(); ctx.moveTo(cx, fTop); ctx.lineTo(cx, fBot); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(cx-6, fBot+1); ctx.lineTo(cx, fBot+6); ctx.lineTo(cx+6, fBot+1); ctx.fill();
    ctx.restore();

    // Électrode haute (collectrice)
    ctx.fillStyle = 'rgba(130,150,185,.50)'; ctx.strokeStyle = 'rgba(160,180,210,.80)'; ctx.lineWidth = 1.5; ctx.setLineDash([]);
    ctx.fillRect(cx - w/2, topY, w, thin);
    ctx.strokeRect(cx - w/2, topY, w, thin);

    // Séparateur de garde (tirets)
    ctx.save(); ctx.strokeStyle = 'rgba(160,180,210,.45)'; ctx.lineWidth = 1; ctx.setLineDash([2,3]);
    ctx.beginPath();
    ctx.moveTo(cx - w/2 + guard, topY); ctx.lineTo(cx - w/2 + guard, topY + thin);
    ctx.moveTo(cx + w/2 - guard, topY); ctx.lineTo(cx + w/2 - guard, topY + thin);
    ctx.stroke(); ctx.restore();

    // Volume actif (gaz entre électrodes)
    ctx.fillStyle = 'rgba(251,146,60,.22)'; ctx.strokeStyle = '#fb923c'; ctx.lineWidth = 1.2; ctx.setLineDash([]);
    ctx.fillRect(cx - w/2 + guard, cy - gap/2, w - 2*guard, gap);
    ctx.strokeRect(cx - w/2 + guard, cy - gap/2, w - 2*guard, gap);

    // Électrode basse (haute tension)
    ctx.fillStyle = 'rgba(130,150,185,.45)'; ctx.strokeStyle = 'rgba(160,180,210,.80)'; ctx.lineWidth = 1.5;
    ctx.fillRect(cx - w/2, cy + gap/2, w, thin);
    ctx.strokeRect(cx - w/2, cy + gap/2, w, thin);

    // Labels
    ctx.fillStyle = '#fb923c'; ctx.font = 'bold 10px sans-serif'; ctx.textAlign = 'center'; ctx.setLineDash([]);
    ctx.fillText('Cavité active', cx, cy + gap/2 + thin + 16);
    ctx.fillStyle = 'rgba(200,210,230,.50)'; ctx.font = '9px sans-serif'; ctx.textAlign = 'right';
    ctx.fillText('Vue sagittale ‖ faisceau', W - 4, H - 4);
  }
}

function updateDetectorInfo() {
  const det = DETECTORS[parseInt(document.getElementById('d-detector').value)];
  // Conversion cGy/nC → Gy/C : ×10⁷  (1 cGy/nC = 0.01 Gy / 1e-9 C = 1e7 Gy/C)
  const ndwGpC = det.ndw * 1e7;
  const exp    = Math.floor(Math.log10(ndwGpC));
  const mant   = (ndwGpC / Math.pow(10, exp)).toFixed(2);
  const ndwStr = `${mant} × 10<sup>${exp}</sup> Gy/C`;
  document.getElementById('det-info').innerHTML =
    `<b>Modèle :</b> ${det.model}<br>` +
    `<b>Volume actif :</b> ${det.volume} cm³<br>` +
    `<b>Forme :</b> ${det.shape === 'cyl' ? 'Cylindrique' : 'Plan-parallèle'}<br>` +
    `<b>N<sub>D,w,Q0</sub> (Co-60) :</b> ${ndwStr}<br>` +
    `<i style="color:var(--muted)">Étalonnée dans l'eau, Co-60 — T<sub>0</sub> = 20,0 °C, P<sub>0</sub> = 1013,25 hPa</i>`;
  drawDetectorSchema(det);
}

function updateDosimetryEnergyOptions() {
  const btype = document.getElementById('d-btype').value;
  const sel   = document.getElementById('d-energy');
  sel.innerHTML = '';
  const opts = btype === 'photons'
    ? [['4','4 MV'],['6','6 MV'],['6fff','6 MV FFF'],['10','10 MV'],['10fff','10 MV FFF'],['15','15 MV'],['18','18 MV']]
    : [['4','4 MeV'],['6','6 MeV'],['8','8 MeV'],['10','10 MeV'],['12','12 MeV'],['15','15 MeV'],['18','18 MeV'],['20','20 MeV']];
  opts.forEach(([v, t]) => {
    const o = document.createElement('option'); o.value = v; o.textContent = t;
    if (v === '6') o.selected = true;
    sel.append(o);
  });
  document.getElementById('d-fs-ctrl').style.display  = btype === 'photons'   ? '' : 'none';
  document.getElementById('d-app-ctrl').style.display = btype === 'electrons' ? '' : 'none';
  refreshDosimetry();
}

let beamRunning = false, beamRAF = null;

function toggleBeam() { beamRunning ? stopBeam() : startBeam(); }

function startBeam() {
  beamRunning = true;
  const btn = document.getElementById('beam-btn');
  btn.textContent = '■  BEAM OFF'; btn.classList.add('on');
  const r = getDosimetryResult();
  document.getElementById('mu-total').textContent = r.MU;
  const dur = Math.max(600, Math.min(5000, r.MU * 20));
  const t0  = performance.now();
  function step(now) {
    const prog  = Math.min(1, (now - t0) / dur);
    const noise = (Math.random() - .5) * 8e-4 * r.charge * Math.sqrt(prog);
    document.getElementById('electro-display').textContent = Math.max(0, r.charge * prog + noise).toFixed(3);
    document.getElementById('mu-counter').textContent = Math.round(r.MU * prog);
    if (prog < 1) { beamRAF = requestAnimationFrame(step); }
    else {
      document.getElementById('electro-display').textContent = r.charge.toFixed(3);
      document.getElementById('mu-counter').textContent = r.MU;
      stopBeam();
    }
  }
  beamRAF = requestAnimationFrame(step);
}

function stopBeam() {
  beamRunning = false;
  if (beamRAF) cancelAnimationFrame(beamRAF);
  const btn = document.getElementById('beam-btn');
  btn.textContent = '▶  BEAM ON'; btn.classList.remove('on');
}

function zeroDosimetry() {
  stopBeam();
  document.getElementById('electro-display').textContent = '0.000';
  document.getElementById('mu-counter').textContent = '0';
}

function renderKQTable() {
  const detIdx = parseInt(document.getElementById('d-detector').value);
  const btype  = document.getElementById('d-btype').value;
  const E      = document.getElementById('d-energy').value;

  const PHOTON_E = [
    { key:'4', label:'4 MV' }, { key:'6', label:'6 MV' }, { key:'6fff', label:'6 FFF' },
    { key:'10', label:'10 MV' }, { key:'10fff', label:'10 FFF' },
    { key:'15', label:'15 MV' }, { key:'18', label:'18 MV' }
  ];
  const ELEC_E = [
    { key:'4', label:'4 MeV' }, { key:'6', label:'6 MeV' }, { key:'8', label:'8 MeV' },
    { key:'10', label:'10 MeV' }, { key:'12', label:'12 MeV' },
    { key:'15', label:'15 MeV' }, { key:'18', label:'18 MeV' }, { key:'20', label:'20 MeV' }
  ];

  function buildTable(tableId, energies, qMode) {
    const tbl = document.getElementById(tableId);
    if (!tbl) return;
    let html = '<thead><tr><th>Chambre / N<sub>D,w</sub></th>';
    energies.forEach(e => { html += `<th>${e.label}</th>`; });
    html += '</tr></thead><tbody>';
    DETECTORS.forEach((det, di) => {
      const rowActive = di === detIdx;
      html += `<tr class="${rowActive ? 'det-active' : ''}">`;
      html += `<td class="det-name">${det.model}<br><span style="color:var(--muted);font-size:10px;font-weight:400">${det.ndw} cGy/nC</span></td>`;
      energies.forEach(e => {
        const val = det.kQ[qMode][e.key];
        const cellActive = rowActive && qMode === (btype === 'electrons' ? 'electrons' : 'photons') && e.key === E;
        html += `<td class="${cellActive ? 'kq-active' : ''}">${val !== undefined ? val.toFixed(3) : '—'}</td>`;
      });
      html += '</tr>';
    });
    html += '</tbody>';
    tbl.innerHTML = html;
  }

  buildTable('kq-photons-table',   PHOTON_E, 'photons');
  buildTable('kq-electrons-table', ELEC_E,   'electrons');
}

function refreshDosimetry() {
  const fsVal  = document.getElementById('d-fs').value;
  document.getElementById('d-fs-disp').textContent  = `${fsVal} × ${fsVal} cm`;
  const ssdVal = document.getElementById('d-ssd').value;
  document.getElementById('d-ssd-disp').textContent = `${ssdVal} cm`;
  document.getElementById('mu-total').textContent = document.getElementById('d-mu').value || 100;
  updateDetectorInfo();
  const r = getDosimetryResult();
  drawDosimetrySchema(r.btype, r.E, r.fs, r.ssd, r.depth);
  renderKQTable();
}

function initDosimetry() {
  // Valeurs aléatoires réalistes de T et P à chaque chargement
  const randT = +(18.0 + Math.random() * 7.0).toFixed(1);   // 18–25 °C
  const randP = +(995  + Math.random() * 30 ).toFixed(1);   // 995–1025 hPa
  document.getElementById('d-temp').value = randT;
  document.getElementById('d-pres').value = randP;

  const detSel = document.getElementById('d-detector');
  DETECTORS.forEach((d, i) => {
    const o = document.createElement('option'); o.value = i;
    o.textContent = `${d.name}  (${d.model})`; detSel.append(o);
  });
  updateDosimetryEnergyOptions();
  ['d-energy','d-fs','d-ssd','d-app','d-depth','d-mu','d-temp','d-pres'].forEach(id => {
    const el = document.getElementById(id);
    el.addEventListener(el.tagName === 'SELECT' ? 'change' : 'input', refreshDosimetry);
  });
  document.getElementById('d-btype').addEventListener('change', updateDosimetryEnergyOptions);
  document.getElementById('d-detector').addEventListener('change', refreshDosimetry);
}

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
  //  dmax  : profondeur de dose max FS=10×10, SSD=100 (cm)
  //  mu    : coeff. atténuation effectif recalibré sur PDD(10) réel TrueBeam (cm⁻¹)
  //  Ds    : dose de surface FS=10×10 (fraction de Dmax) — source Fogliata Fig.6 / données standards
  //  dFS   : variation de dmax par cm de FS (cm/cm) — FF uniquement
  //  sFS   : variation de Ds par cm de FS
  //  sig0  : sigma pénombre à d=0, FS=10 (cm)
  //  horn  : coefficient de cornes FF (>0 → cornes, 0 pour FFF)
  //  sigma_fff : largeur demi-max Lorentzienne ramenée au plan source (cm)
  //              recalibré sur les facteurs de renormalisation Table I Fogliata 2012
    '4': { dmax: 1.0, mu: 0.0420, Ds: 0.40, dFS: 0.006, sFS: 0.004, sig0: 0.28, horn:  0.03 },
    '6': { dmax: 1.5, mu: 0.0330, Ds: 0.32, dFS: 0.009, sFS: 0.006, sig0: 0.35, horn:  0.05 },
  '6fff': { dmax: 1.4, mu: 0.0360, Ds: 0.65, dFS: 0.007, sFS: 0.005, sig0: 0.36, horn: 0, sigma_fff: 13, fff: true },
   '10': { dmax: 2.5, mu: 0.0260, Ds: 0.20, dFS: 0.011, sFS: 0.006, sig0: 0.42, horn:  0.08 },
'10fff': { dmax: 2.4, mu: 0.0280, Ds: 0.42, dFS: 0.011, sFS: 0.005, sig0: 0.43, horn: 0, sigma_fff: 10, fff: true },
   '15': { dmax: 3.0, mu: 0.0190, Ds: 0.15, dFS: 0.012, sFS: 0.005, sig0: 0.48, horn:  0.11 },
   '18': { dmax: 3.5, mu: 0.0160, Ds: 0.12, dFS: 0.013, sFS: 0.004, sig0: 0.53, horn:  0.13 },
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

/** dmax effectif : diminue légèrement avec FS (plus de diffusé latéral)
 *  Pour les faisceaux FFF, dmax est indépendant de la taille de champ. */
function getEffDmax(E, fs) {
  const { dmax, dFS, fff = false } = BEAM[E] ?? BEAM['6'];
  if (fff) return dmax;
  return Math.max(0.5, dmax - dFS * (fs - 10));
}

/**
 * PDD — axe central
 * fs = taille de champ À L'ISOCENTRE (DSA = 100 cm)
 */
function calcPDD(d, fs, E, ssd) {
  const { mu, Ds: Ds0, sFS } = BEAM[E] ?? BEAM['6'];
  const dmax = getEffDmax(E, fs);
  // Dose de surface augmente avec FS (plus de diffusé = plus de contamination)
  const Ds = Math.max(0.08, Math.min(0.80, Ds0 + sFS * (fs - 10)));

  if (d <= 0) return Ds * 100;
  if (d < dmax) {
    const t = d / dmax;
    return 100 * (Ds + (1 - Ds) * (3*t*t - 2*t*t*t));
  }
  // Phantom scatter : augmente avec la taille de champ et la profondeur.
  // Coefficient 1.5e-3 calibré pour reproduire la dépendance FS des PDD mesurées.
  const scatter = 1 + 1.5e-3 * (fs - 10) * (d - dmax);
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
  const { sig0, horn, fff = false, sigma_fff = 10 } = BEAM[E] ?? BEAM['6'];
  const sig = sig0 + 0.012 * d + 0.004 * (fs - 10);
  const M = Math.SQRT2 * sig;
  const pen = 0.5 * (erf((a - x) / M) + erf((a + x) / M));

  let horns;
  if (fff) {
    // FFF : distribution Lorentzienne basée sur la distance hors-axe ramenée au plan source.
    // x_src diminue avec la profondeur → inhomogénéité naturellement réduite en profondeur.
    // Grande taille de champ → x_src grand → inhomogénéité plus prononcée, sans paramètre ad hoc.
    const x_src = Math.abs(x) * SAD / (ssd + d);
    horns = 1 / (1 + (x_src / sigma_fff) ** 2);
  } else {
    // FF : cornes quadratiques (r relatif), limitées à l'intérieur du champ
    const r = a > 0 ? Math.abs(x) / a : 0;
    const hornEff = horn * Math.max(0.4, 1 + 0.025 * (fs - 10));
    horns = r < 1 ? (1 + hornEff * r * r) : 1.0;
  }
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

/**
 * Facteur de renormalisation Fogliata 2012 pour les faisceaux FFF.
 * R(FS, d) = (a + b·FS + c·d) / (1 + dd·FS + e·d)   [résultat en fraction]
 * Représente la valeur du profil FFF (normalisé sur l'axe) au point de référence
 * correspondant à la région "plate" du faisceau FF équivalent.
 * Les seuils 20/50/80 % sont appliqués à ce niveau de référence plutôt qu'à 1.0.
 * Paramètres : Fogliata et al., Med. Phys. 39(10), 2012 – Table II.
 */
function fogliataRenorm(E, fs, d) {
  // a et dd recalibrés (b inchangé) pour D50% = géométrique à FS=10 et FS=20 cm.
  // c=e=0 : calcProfile au bord géométrique est indépendant de d → pas de terme en d.
  const P = {
    '6fff':  { a: 85.39, b: 0.6595, c: 0, dd: -0.01816, e: 0 },
    '10fff': { a: 76.05, b: 2.4826, c: 0, dd: -0.01745, e: 0 },
  };
  const p = P[E];
  if (!p) return null;
  return (p.a + p.b * fs + p.c * d) / (1 + p.dd * fs + p.e * d) / 100;
}

/**
 * Recherche dichotomique : position x > 0 où le profil = frac × ref.
 * Pour FF : ref = valeur sur l'axe (≈ 1).
 * Pour FFF : ref = facteur de renormalisation Fogliata (< 1).
 */
function findXatFrac(frac, d, fs, E, ssd, ref = null) {
  const p0 = ref !== null ? ref : calcProfile(0, d, fs, E, ssd);
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
  const { fff = false } = BEAM[E] ?? BEAM['6'];
  // FFF : profil renormalisé = calcProfile(x) × fogliataRenorm
  // → chercher où ce produit = frac ↔ calcProfile(x) = frac / fogliataRenorm
  // → ref = 1/fogliataRenorm   (FF : ref = null → p0 = valeur sur l'axe)
  const renorm = fff ? fogliataRenorm(E, fs, d) : null;
  const ref = renorm !== null ? 1 / renorm : null;
  const x50 = findXatFrac(0.50, d, fs, E, ssd, ref);
  const x80 = findXatFrac(0.80, d, fs, E, ssd, ref);
  const x20 = findXatFrac(0.20, d, fs, E, ssd, ref);
  // Taille géométrique = taille à l'isocentre projetée à la profondeur d
  const geom = fs * (ssd + d) / SAD;
  return {
    fieldWidth: (2 * x50).toFixed(1),
    penumbra:   (x20 - x80).toFixed(1),
    geom:       geom.toFixed(1),
  };
}

// ═══════════════════════════════════════════════════════
//  ÉLECTRONS — PARAMÈTRES ET PHYSIQUE
// ═══════════════════════════════════════════════════════

const EBEAM = {
  //  dmax  : profondeur de dose max (cm), applicateur 10×10, SSD=100
  //  r50   : profondeur de mi-valeur (cm) — indicateur d'énergie (R50 ≈ 0.3·E)
  //  rp    : portée pratique (cm) — extrapolation de la chute du PDD
  //  Ds    : dose de surface (fraction de Dmax) — augmente avec l'énergie
  //  sigE0 : sigma de pénombre à la surface (cm)
  //  kSig  : croissance de sigma par cm de profondeur (diffusion coulombienne multiple)
  //  brem : fraction de dose de bremsstrahlung au-delà de Rp — augmente avec l'énergie
  //         (ref. IAEA Ch.8 : ~0.25×E% pour un faisceau clinique dans l'eau)
  '4':  { dmax: 0.9,  r50: 1.5,  rp: 2.2,  Ds: 0.77, sigE0: 0.30, kSig: 0.068, brem: 0.010 },
  '6':  { dmax: 1.3,  r50: 2.3,  rp: 3.1,  Ds: 0.80, sigE0: 0.27, kSig: 0.063, brem: 0.015 },
  '8':  { dmax: 1.7,  r50: 3.1,  rp: 4.1,  Ds: 0.83, sigE0: 0.25, kSig: 0.058, brem: 0.020 },
  '10': { dmax: 2.2,  r50: 3.9,  rp: 5.2,  Ds: 0.85, sigE0: 0.23, kSig: 0.053, brem: 0.025 },
  '12': { dmax: 2.7,  r50: 4.8,  rp: 6.3,  Ds: 0.87, sigE0: 0.21, kSig: 0.050, brem: 0.030 },
  '15': { dmax: 3.0,  r50: 6.0,  rp: 7.8,  Ds: 0.88, sigE0: 0.19, kSig: 0.047, brem: 0.038 },
  '18': { dmax: 3.5,  r50: 7.3,  rp: 9.4,  Ds: 0.89, sigE0: 0.18, kSig: 0.044, brem: 0.045 },
  '20': { dmax: 3.8,  r50: 8.2, rp: 10.5,  Ds: 0.90, sigE0: 0.17, kSig: 0.041, brem: 0.050 },
};

/**
 * PDD électrons : buildup cubique jusqu'à dmax, puis décroissance Fermi centrée sur R50.
 * Queue de bremsstrahlung résiduelle (~1.5%) au-delà de Rp.
 */
function calcElectronPDD(d, fs, Emev) {
  const p = EBEAM[Emev] ?? EBEAM['6'];
  const { dmax, r50, rp, Ds: Ds0, brem } = p;
  // Surface dose increases with applicator size (~0.5% per cm above 10×10 reference)
  const Ds = Math.min(0.97, Ds0 + 0.005 * (fs - 10));
  const sigmaF = Math.max(0.15, (rp - r50) / 3);
  if (d <= 0) return Ds * 100;
  const build   = d < dmax ? Ds + (1 - Ds) * (3*(d/dmax)**2 - 2*(d/dmax)**3) : 1.0;
  const falloff = 1 / (1 + Math.exp((d - r50) / sigmaF));
  return 100 * (build * falloff + brem * (1 - falloff));
}

/**
 * Profil latéral électrons : plateau erf avec pénombre croissante en profondeur.
 * La diffusion coulombienne multiple élargit sigma linéairement avec d.
 * Pas de cornes — le diffuseur homogénéise le faisceau dans l'applicateur.
 */
function calcElectronProfile(x, d, fs, Emev) {
  const p = EBEAM[Emev] ?? EBEAM['6'];
  const sig = p.sigE0 + p.kSig * d;
  const M   = Math.SQRT2 * sig;
  const a   = (fs / 2) * (100 + d) / SAD; // légère divergence depuis la source
  const pen = 0.5 * (erf((a - x) / M) + erf((a + x) / M));
  return pen + 0.004 * (1 - pen); // fuite quasi-nulle
}

function calcElectronDose(x, d, fs, Emev) {
  return calcElectronPDD(d, fs, Emev) * calcElectronProfile(x, d, fs, Emev);
}

/** Platéité IEC 60976 : (Dmax-Dmin)/(Dmax+Dmin) dans les 80% centraux du champ. */
function calcElectronFlatness(d, fs, Emev) {
  const vals = [];
  for (let i = 0; i <= 40; i++) {
    const x = -0.4*fs + (0.8*fs/40)*i;
    vals.push(calcElectronProfile(x, d, fs, Emev));
  }
  const Dmax = Math.max(...vals), Dmin = Math.min(...vals);
  if (Dmax + Dmin <= 0) return '—';
  return ((Dmax - Dmin) / (Dmax + Dmin) * 100).toFixed(1);
}

function calcElectronMetrics(d, fs, Emev) {
  const prof = x => calcElectronProfile(x, d, fs, Emev);
  const p0   = prof(0);
  const bisect = (frac) => {
    let lo = 0, hi = fs / 2 + 6;
    for (let i = 0; i < 52; i++) {
      const mid = (lo + hi) / 2;
      if (prof(mid) > frac * p0) lo = mid; else hi = mid;
    }
    return (lo + hi) / 2;
  };
  return {
    fieldWidth: (2 * bisect(0.50)).toFixed(1),
    penumbra:   (bisect(0.20) - bisect(0.80)).toFixed(1),
    flatness:   calcElectronFlatness(d, fs, Emev),
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

function renderElectronPhantom(fs, Emev) {
  const cv  = document.getElementById('phantom-cv');
  const ctx = cv.getContext('2d');
  const W = cv.width, H = cv.height;
  const img = ctx.createImageData(W, H);
  const px  = img.data;
  for (let py = 0; py < H; py++) {
    const d = (py / H) * DEPTH_MAX;
    for (let xi = 0; xi < W; xi++) {
      const x    = (xi / W - 0.5) * 2 * X_HALF;
      const dose = calcElectronDose(x, d, fs, Emev);
      const [r, g, b] = toRGB(dose / 100);
      const i = (py * W + xi) * 4;
      px[i]=r; px[i+1]=g; px[i+2]=b; px[i+3]=255;
    }
  }
  ctx.putImageData(img, 0, 0);
  // Bords de champ (légère divergence)
  drawBeamEdges(ctx, W, H, fs, 100);
  drawDepthLines(ctx, W, H);
  drawDepthScale(ctx, W, H);
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
  const jawY  = 54;   // sortie mâchoires
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

  // ── Filtre égalisateur — géométrie ──
  const { horn, fff = false } = BEAM[E] ?? BEAM['6'];
  const filterTopY   = srcY + 9;      // juste sous la source
  const filterBotY   = jawY - 15;     // juste au-dessus des mâchoires
  // Taille fixe = filtre dimensionné pour le champ maximum (30 cm), indépendant de fs
  const filterBaseHalf = Math.min(cx - 14, (30 / 2) * JAW_DIST / SAD * scaleX);

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

  // ── Filtre égalisateur (absent en mode FFF) ──
  ctx.save();
  if (!fff) {
    // Forme : trapèze (apex vers la source, base vers les mâchoires)
    // La brillance centrale reflète l'atténuation maximale sur l'axe
    const fGrad = ctx.createLinearGradient(cx - filterBaseHalf, 0, cx + filterBaseHalf, 0);
    fGrad.addColorStop(0,    'rgba(60,70,95,.10)');
    fGrad.addColorStop(0.30, 'rgba(130,145,175,.55)');
    fGrad.addColorStop(0.50, 'rgba(205,220,245,.92)');
    fGrad.addColorStop(0.70, 'rgba(130,145,175,.55)');
    fGrad.addColorStop(1,    'rgba(60,70,95,.10)');
    ctx.fillStyle = fGrad;
    ctx.strokeStyle = 'rgba(200,215,240,.85)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(cx - 2, filterTopY);
    ctx.lineTo(cx - filterBaseHalf, filterBotY);
    ctx.lineTo(cx + filterBaseHalf, filterBotY);
    ctx.lineTo(cx + 2, filterTopY);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
  } else {
    // FFF : emplacement vide du filtre, contour en tirets
    ctx.strokeStyle = 'rgba(251,146,60,.50)';
    ctx.setLineDash([3, 3]); ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(cx - 2, filterTopY);
    ctx.lineTo(cx - filterBaseHalf, filterBotY);
    ctx.lineTo(cx + filterBaseHalf, filterBotY);
    ctx.lineTo(cx + 2, filterTopY);
    ctx.closePath();
    ctx.stroke();
  }
  ctx.restore();

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

  // Filtre égalisateur — label
  ctx.save();
  const filterMidY = (filterTopY + filterBotY) / 2;
  ctx.font = '8px sans-serif'; ctx.textAlign = 'right';
  if (!fff) {
    ctx.fillStyle = 'rgba(190,208,240,.80)';
    ctx.fillText('Filtre éq.', cx - filterBaseHalf - 3, filterMidY + 3);
    ctx.strokeStyle = 'rgba(190,208,240,.45)';
  } else {
    ctx.fillStyle = 'rgba(251,146,60,.85)';
    ctx.fillText('FFF', cx - filterBaseHalf - 3, filterMidY + 3);
    ctx.strokeStyle = 'rgba(251,146,60,.45)';
  }
  ctx.lineWidth = 0.5; ctx.setLineDash([]);
  ctx.beginPath();
  ctx.moveTo(cx - filterBaseHalf - 2, filterMidY);
  ctx.lineTo(cx - filterBaseHalf, filterMidY);
  ctx.stroke();
  ctx.restore();

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

function drawElectronSchema(fs, Emev) {
  const cv = document.getElementById('schema-cv');
  if (!cv) return;
  const ctx = cv.getContext('2d');
  const W = cv.width, H = cv.height;
  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = '#0d1117';
  ctx.fillRect(0, 0, W, H);

  const cx = W / 2;
  const srcY  = 16;
  const jawY  = 54;
  const surfY = 100;
  const botY  = H - 10;
  const phantomPx = botY - surfY;
  const scaleY = phantomPx / DEPTH_MAX;
  const scaleX = (W - 10) / (2 * X_HALF);
  const p = EBEAM[Emev] ?? EBEAM['6'];

  // Axe central
  ctx.save();
  ctx.strokeStyle = 'rgba(255,255,255,.10)'; ctx.setLineDash([4, 5]); ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(cx, srcY); ctx.lineTo(cx, botY); ctx.stroke(); ctx.restore();

  // Bords faisceau divergents
  const lSurf = cx - (fs/2) * 100 / SAD * scaleX;
  const rSurf = cx + (fs/2) * 100 / SAD * scaleX;
  const lBot  = cx - (fs/2) * (100 + DEPTH_MAX) / SAD * scaleX;
  const rBot  = cx + (fs/2) * (100 + DEPTH_MAX) / SAD * scaleX;

  // Mâchoires (définissent le champ applicateur, dist source-jaw ≈ 40 cm)
  const JAW_DIST = 40;
  const jawHalfPx = Math.min(cx - 6, (fs / 2) * JAW_DIST / SAD * scaleX);
  const lJaw = cx - jawHalfPx, rJaw = cx + jawHalfPx;

  // Zone absorbée par mâchoires
  ctx.save();
  ctx.fillStyle = 'rgba(80,80,100,.18)';
  ctx.beginPath(); ctx.moveTo(cx, srcY); ctx.lineTo(5, jawY); ctx.lineTo(lJaw, jawY); ctx.closePath(); ctx.fill();
  ctx.beginPath(); ctx.moveTo(cx, srcY); ctx.lineTo(W-5, jawY); ctx.lineTo(rJaw, jawY); ctx.closePath(); ctx.fill();
  ctx.restore();

  // Cône utile mâchoires → surface
  ctx.save();
  ctx.fillStyle = 'rgba(100,220,255,.06)';
  ctx.beginPath();
  ctx.moveTo(lJaw, jawY); ctx.lineTo(lSurf, surfY); ctx.lineTo(rSurf, surfY); ctx.lineTo(rJaw, jawY);
  ctx.closePath(); ctx.fill();
  ctx.strokeStyle = 'rgba(100,220,255,.35)'; ctx.setLineDash([3, 3]); ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(lJaw, jawY); ctx.lineTo(lSurf, surfY);
  ctx.moveTo(rJaw, jawY); ctx.lineTo(rSurf, surfY); ctx.stroke(); ctx.restore();

  // Feuilles de diffusion (2 feuilles = diffuseur primaire + secondaire)
  const foilTopY = srcY + 9, foilBotY = jawY - 15;
  const foilW    = Math.min(cx - 8, (fs/2) * JAW_DIST / SAD * scaleX + 8);
  ctx.save();
  [foilTopY, (foilTopY + foilBotY) / 2].forEach(fy => {
    const g = ctx.createLinearGradient(cx - foilW, 0, cx + foilW, 0);
    g.addColorStop(0,    'rgba(80,120,80,.10)');
    g.addColorStop(0.35, 'rgba(140,200,140,.55)');
    g.addColorStop(0.50, 'rgba(200,255,200,.80)');
    g.addColorStop(0.65, 'rgba(140,200,140,.55)');
    g.addColorStop(1,    'rgba(80,120,80,.10)');
    ctx.fillStyle = g;
    ctx.strokeStyle = 'rgba(160,230,160,.70)'; ctx.lineWidth = 1; ctx.setLineDash([]);
    ctx.beginPath(); ctx.rect(cx - foilW, fy, foilW * 2, 3); ctx.fill(); ctx.stroke();
  });
  ctx.restore();

  // Fantôme d'eau
  ctx.fillStyle = 'rgba(14,55,120,.20)';
  ctx.fillRect(5, surfY, W - 10, phantomPx);
  ctx.strokeStyle = '#1e40af'; ctx.setLineDash([]); ctx.lineWidth = 1.5;
  ctx.strokeRect(5, surfY, W - 10, phantomPx);

  // Applicateur (tube de la surface vers -5 cm au-dessus)
  const appW  = Math.min(cx - 6, (fs/2) * scaleX);
  const appTopY = surfY - 28, appBotY = surfY;
  ctx.save();
  ctx.strokeStyle = 'rgba(251,146,60,.80)'; ctx.lineWidth = 1.5; ctx.setLineDash([]);
  ctx.beginPath();
  ctx.moveTo(cx - appW, appTopY); ctx.lineTo(cx - appW, appBotY); // paroi gauche
  ctx.moveTo(cx + appW, appTopY); ctx.lineTo(cx + appW, appBotY); // paroi droite
  ctx.stroke();
  ctx.strokeStyle = 'rgba(251,146,60,.40)'; ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(cx - appW, appTopY); ctx.lineTo(cx + appW, appTopY); // bord haut
  ctx.stroke();
  ctx.fillStyle = 'rgba(251,146,60,.80)'; ctx.font = '8px sans-serif'; ctx.textAlign = 'right';
  ctx.fillText('Applicateur', cx - appW - 3, surfY - 12);
  ctx.restore();

  // Faisceau dans le fantôme (électrons, clippé)
  ctx.save();
  ctx.beginPath(); ctx.rect(5, surfY, W-10, phantomPx); ctx.clip();
  ctx.strokeStyle = 'rgba(100,220,255,.45)'; ctx.setLineDash([]); ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(lSurf, surfY); ctx.lineTo(lBot, botY);
  ctx.moveTo(rSurf, surfY); ctx.lineTo(rBot, botY);
  ctx.stroke(); ctx.restore();

  // Lignes de profondeur
  ctx.save(); ctx.setLineDash([4, 3]); ctx.lineWidth = 1.2;
  getDepths().forEach((d, i) => {
    if (d < 0 || d > DEPTH_MAX) return;
    const y  = surfY + d * scaleY;
    const lx = cx - (fs/2) * (100 + d) / SAD * scaleX - 4;
    const rx = cx + (fs/2) * (100 + d) / SAD * scaleX + 4;
    ctx.strokeStyle = PCOLS[i];
    ctx.beginPath(); ctx.moveTo(Math.max(6, lx), y); ctx.lineTo(Math.min(W-6, rx), y); ctx.stroke();
  });
  ctx.restore();

  // Marqueurs R50 et Rp sur le côté
  ctx.save();
  ctx.font = '8px sans-serif'; ctx.textAlign = 'right';
  [[p.r50, '#38bdf8', 'R₅₀'], [p.rp, '#fb923c', 'Rₚ']].forEach(([dv, col, lbl]) => {
    if (dv > DEPTH_MAX) return;
    const y = surfY + dv * scaleY;
    ctx.strokeStyle = col; ctx.setLineDash([2, 3]); ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(5, y); ctx.lineTo(W-5, y); ctx.stroke();
    ctx.fillStyle = col; ctx.setLineDash([]);
    ctx.fillText(lbl, W - 3, y - 1);
  });
  ctx.restore();

  // Source
  ctx.setLineDash([]);
  const grd = ctx.createRadialGradient(cx, srcY, 0, cx, srcY, 7);
  grd.addColorStop(0, '#fffde7'); grd.addColorStop(1, '#f59e0b');
  ctx.beginPath(); ctx.arc(cx, srcY, 7, 0, Math.PI * 2);
  ctx.fillStyle = grd; ctx.fill();

  // Mâchoires
  ctx.fillStyle = '#1e3a5f'; ctx.strokeStyle = '#2d5492'; ctx.lineWidth = 1;
  ctx.fillRect(5, jawY-10, lJaw-5, 12); ctx.strokeRect(5, jawY-10, lJaw-5, 12);
  ctx.fillRect(rJaw, jawY-10, W-5-rJaw, 12); ctx.strokeRect(rJaw, jawY-10, W-5-rJaw, 12);

  // Labels
  ctx.fillStyle = '#8b949e'; ctx.font = '9px sans-serif';
  ctx.textAlign = 'right'; ctx.fillText('Source', cx - 10, srcY + 4);
  // Diffuseurs
  ctx.fillStyle = 'rgba(160,230,160,.80)'; ctx.font = '8px sans-serif'; ctx.textAlign = 'right';
  ctx.fillText('Diffuseurs', cx - foilW - 3, foilTopY + 8);
  // Énergie
  ctx.fillStyle = '#58a6ff'; ctx.font = 'bold 8px sans-serif'; ctx.textAlign = 'center';
  ctx.fillText(`${Emev} MeV  ·  App. ${fs}×${fs} cm`, cx, surfY + 32);
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
    if (activeTab === 'electrons') {
      const { Emev } = getElectronParams();
      const p = EBEAM[Emev] ?? EBEAM['6'];
      const xScale = chart.scales.x;
      if (!xScale) return;
      const { top, bottom } = chart.chartArea;
      const ctx = chart.ctx;
      const markers = [
        [p.dmax, '#fbbf24', `d_max=${p.dmax} cm`, 12],
        [p.r50,  '#38bdf8', `R₅₀=${p.r50} cm`,   24],
        [p.rp,   '#fb923c', `Rₚ=${p.rp} cm`,      36],
      ];
      markers.forEach(([dv, col, lbl, yOff]) => {
        if (dv > 30) return;
        const px = xScale.getPixelForValue(dv);
        ctx.save();
        ctx.strokeStyle = col; ctx.setLineDash([5, 4]); ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.moveTo(px, top); ctx.lineTo(px, bottom); ctx.stroke();
        ctx.fillStyle = col; ctx.font = 'bold 9px sans-serif';
        ctx.textAlign = 'left'; ctx.setLineDash([]);
        ctx.fillText(lbl, px + 4, top + yOff);
        ctx.restore();
      });
      return;
    }
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
  chartPDD.data.datasets[0].borderColor = '#38bdf8';
  chartPDD.update('none');
}

function updateElectronPDDChart(fs, Emev) {
  const pts = [];
  for (let d = 0; d <= 30; d += 0.1) pts.push({ x: d, y: calcElectronPDD(d, fs, Emev) });
  chartPDD.data.datasets[0].data = pts;
  chartPDD.data.datasets[0].borderColor = '#4ade80';
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

function updateElectronProfilesChart(fs, Emev) {
  const deps = getDepths();
  const xs = [];
  for (let x = -20; x <= 20; x += 0.2) xs.push(x);
  chartProf.data.datasets = deps.map((d, i) => ({
    label: `d = ${d} cm`,
    data: xs.map(x => ({ x, y: calcElectronDose(x, d, fs, Emev) })),
    borderColor: PCOLS[i], backgroundColor: 'transparent',
    borderWidth: 2, pointRadius: 0, tension: 0.2,
  }));
  chartProf.update('none');
}

// ═══════════════════════════════════════════════════════
//  TABLE MÉTRIQUES
// ═══════════════════════════════════════════════════════

function updateMetrics(fs, E, ssd) {
  document.getElementById('metrics-head').innerHTML = `<tr>
    <th>Profondeur</th><th>Taille de champ D<sub>50%</sub></th>
    <th>Pénombre 20–80 %</th><th>Taille géom. à l'iso (FS × (DSP+d)/100)</th></tr>`;
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

function updateElectronMetrics(fs, Emev) {
  const p = EBEAM[Emev] ?? EBEAM['6'];
  document.getElementById('metrics-head').innerHTML = `<tr>
    <th>Profondeur</th><th>Taille de champ D<sub>50%</sub></th>
    <th>Pénombre 20–80 %</th><th>Platéité IEC (central 80%)</th></tr>`;
  document.getElementById('metrics-body').innerHTML =
    getDepths().map((d, i) => {
      const m = calcElectronMetrics(d, fs, Emev);
      return `<tr>
        <td><span class="dot" style="background:${PCOLS[i]}"></span>${d} cm</td>
        <td><b>${m.fieldWidth}</b> cm</td>
        <td><b>${m.penumbra}</b> cm</td>
        <td><b>${m.flatness}</b> %</td>
      </tr>`;
    }).join('');
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
    tip.style.display = 'block';
    tip.style.left = (e.offsetX + 14) + 'px';
    tip.style.top  = (e.offsetY + 14) + 'px';
    let dose;
    if (activeTab === 'electrons') {
      const { fs: efs, Emev } = getElectronParams();
      dose = calcElectronDose(x, d, efs, Emev);
    } else {
      const { fs, E, ssd } = getParams();
      dose = calcDose(x, d, fs, E, ssd);
    }
    tip.innerHTML = `x = ${x.toFixed(1)} cm<br>d = ${d.toFixed(1)} cm<br><b style="color:#38bdf8">Dose = ${dose.toFixed(1)} %</b>`;
  });
  cv.addEventListener('mouseleave', () => { tip.style.display = 'none'; });
}

// ═══════════════════════════════════════════════════════
//  ÉTAT & RAFRAÎCHISSEMENT
// ═══════════════════════════════════════════════════════

let activeTab = 'photons';

function getParams() {
  return {
    E:   document.getElementById('energy').value,
    fs:  parseInt(document.getElementById('fieldSize').value),
    ssd: parseInt(document.getElementById('ssd').value),
  };
}

function getElectronParams() {
  return {
    Emev: document.getElementById('e-energy').value,
    fs:   parseInt(document.getElementById('e-appSize').value),
    ssd:  100,
  };
}

function getDepths() {
  const cls = activeTab === 'electrons' ? '.e-dnum' : '.dnum';
  return Array.from(document.querySelectorAll(cls))
    .map(el => parseFloat(el.value))
    .filter(d => isFinite(d) && d >= 0 && d <= 30);
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

function updateElectronDisplays() {
  const { Emev, fs } = getElectronParams();
  const p = EBEAM[Emev] ?? EBEAM['6'];
  document.getElementById('dmax-info').textContent = `d_max = ${p.dmax} cm`;
  document.getElementById('chips').innerHTML =
    `<span class="chip">d<sub>max</sub> = <b>${p.dmax} cm</b></span>` +
    `<span class="chip">R<sub>50</sub> = <b>${p.r50} cm</b></span>` +
    `<span class="chip">R<sub>p</sub> = <b>${p.rp} cm</b></span>` +
    `<span class="chip">Dose surface = <b>${(p.Ds*100).toFixed(0)} %</b></span>`;
}

/** Pré-règle les profondeurs électrons sur dmax, R50, 0.8×Rp */
function setElectronDefaultDepths(Emev) {
  const p = EBEAM[Emev] ?? EBEAM['6'];
  const defaults = [p.dmax, p.r50, p.rp];
  document.querySelectorAll('.e-dnum').forEach((inp, i) => {
    if (defaults[i] !== undefined) inp.value = defaults[i];
  });
}

function refresh() {
  if (activeTab === 'electrons') {
    const { Emev, fs } = getElectronParams();
    updateElectronDisplays();
    updateElectronPDDChart(fs, Emev);
    updateElectronProfilesChart(fs, Emev);
    updateElectronMetrics(fs, Emev);
    renderElectronPhantom(fs, Emev);
    drawElectronSchema(fs, Emev);
  } else {
    const { E, fs, ssd } = getParams();
    updateDisplays();
    updatePDDChart(fs, E, ssd);
    updateProfilesChart(fs, E, ssd);
    updateMetrics(fs, E, ssd);
    renderPhantom(fs, E, ssd);
    drawSchema(fs, E, ssd);
  }
}

function initDepthControls() {
  // Photons
  const tbl = document.getElementById('depth-tbl');
  [1.5, 5, 10, 20].forEach((d, i) => {
    const sw  = Object.assign(document.createElement('div'), { className: 'dswatch' });
    sw.style.background = PCOLS[i];
    const lbl = Object.assign(document.createElement('span'), { className: 'dlabel', textContent: `d${i+1}` });
    const inp = Object.assign(document.createElement('input'), { type: 'number', className: 'dnum', value: d, min: 0, max: 30, step: 0.5 });
    inp.addEventListener('input', refresh);
    const unit = Object.assign(document.createElement('span'), { className: 'dlabel', textContent: 'cm' });
    tbl.append(sw, lbl, inp, unit);
  });
  // Électrons (3 profondeurs — pré-réglées dynamiquement)
  const etbl = document.getElementById('e-depth-tbl');
  [0, 1, 2].forEach((_, i) => {
    const sw  = Object.assign(document.createElement('div'), { className: 'dswatch' });
    sw.style.background = PCOLS[i];
    const lbl = Object.assign(document.createElement('span'), { className: 'dlabel', textContent: `d${i+1}` });
    const inp = Object.assign(document.createElement('input'), { type: 'number', className: 'e-dnum', value: 0, min: 0, max: 30, step: 0.1 });
    inp.addEventListener('input', refresh);
    const unit = Object.assign(document.createElement('span'), { className: 'dlabel', textContent: 'cm' });
    etbl.append(sw, lbl, inp, unit);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initDepthControls();
  renderColorbar();
  initCharts();
  initPhantomHover();

  // Onglet photons
  document.getElementById('energy').addEventListener('change', refresh);
  document.getElementById('fieldSize').addEventListener('input', refresh);
  document.getElementById('ssd').addEventListener('input', refresh);

  // Onglet électrons
  document.getElementById('e-energy').addEventListener('change', () => {
    setElectronDefaultDepths(document.getElementById('e-energy').value);
    refresh();
  });
  document.getElementById('e-appSize').addEventListener('change', refresh);

  // Bascule des onglets
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      activeTab = btn.dataset.tab;
      document.getElementById(`panel-${activeTab}`).classList.add('active');
      // Masquer la zone fantôme/PDD/profils pour l'onglet dosimétrie
      document.querySelector('.main').style.display = activeTab === 'dosimetry' ? 'none' : '';
      if (activeTab === 'electrons') {
        setElectronDefaultDepths(document.getElementById('e-energy').value);
      }
      if (activeTab === 'dosimetry') refreshDosimetry();
      else refresh();
    });
  });

  initDosimetry();
  refresh();
});
</script>
</body>
</html>
