  /* ---------- Lagebild ----------
     Anmutung wie RescueTrack. Die Luftfahrzeuge laufen einen echten Einsatzzyklus
     durch; Statusziffer und Farbe kommen aus FMS_STATUS_COLORS des Monorepos
     (apps/dispatch/app/_helpers/fmsStatusColors.ts). */
  var cv = document.getElementById('lage'), ctx = cv.getContext('2d');
  var W = 0, H = 0, dpr = Math.min(devicePixelRatio || 1, 2);
  var LAND = '#1E2A22', ROAD2 = '#333B38', AUTOB = '#6B7470',
      TEAL = '#2FA3A0', TRACK = '#D08A2C';

  /* aus dem Monorepo uebernommen */
  var FMS = {
    '0': 'rgb(140,10,10)', '1': 'rgb(10,134,25)', '2': 'rgb(10,134,25)',
    '3': 'rgb(140,10,10)', '4': 'rgb(140,10,10)', '5': 'rgb(231,77,22)',
    '6': 'rgb(85,85,85)',  '7': 'rgb(140,10,10)', '8': 'rgb(186,105,0)',
    '9': 'rgb(10,134,25)'
  };

  /* Ablauf eines Einsatzes: Status, Dauer in ms, wohin geflogen wird */
  var ABLAUF = [
    { st: '2', dauer: [5000, 14000], ziel: null      },  /* auf Wache          */
    { st: '3', dauer: [9000, 13000], ziel: 'einsatz' },  /* Einsatz uebernommen */
    { st: '4', dauer: [5000,  8000], ziel: null      },  /* am Einsatzort       */
    { st: '7', dauer: [8000, 12000], ziel: 'klinik'  },  /* Patient an Bord     */
    { st: '8', dauer: [4000,  7000], ziel: null      },  /* am Transportziel    */
    { st: '1', dauer: [8000, 12000], ziel: 'station' }   /* frei, Rueckflug     */
  ];

  var FLOTTE = [
    'Christoph 51', 'Rega 10', 'Christophorus 3', 'Christoph 22', 'Lifeliner 1'
  ];

  var STATIONEN = [], KLINIKEN = [], ROADS = [], LFZ = [];

  function rnd(a, b) { return a + Math.random() * (b - a); }
  function pick(a) { return a[(Math.random() * a.length) | 0]; }

  function seed() {
    STATIONEN = []; KLINIKEN = []; ROADS = []; LFZ = [];
    var i, j;
    for (i = 0; i < 16; i++) {
      var x = rnd(0, W), y = rnd(0, H), ang = rnd(0, 6.283), p = [[x, y]];
      for (j = 0; j < 5; j++) {
        ang += rnd(-0.55, 0.55);
        x += Math.cos(ang) * Math.min(W, H) * 0.14;
        y += Math.sin(ang) * Math.min(W, H) * 0.14;
        p.push([x, y]);
      }
      ROADS.push({ p: p, big: i < 4 });
    }
    var n = Math.max(4, Math.round(W / 300));
    for (i = 0; i < n; i++) STATIONEN.push({ x: rnd(0.34, 0.98) * W, y: rnd(0.10, 0.92) * H });
    for (i = 0; i < 3; i++) KLINIKEN.push({ x: rnd(0.36, 0.96) * W, y: rnd(0.12, 0.90) * H });

    var namen = FLOTTE.slice();
    for (i = 0; i < Math.min(4, STATIONEN.length); i++) {
      var heim = STATIONEN[i % STATIONEN.length];
      LFZ.push({
        nm: namen.splice((Math.random() * namen.length) | 0, 1)[0],
        heim: heim, x: heim.x, y: heim.y, von: null, nach: null,
        phase: (Math.random() * ABLAUF.length) | 0, t: 0, dauer: rnd(2000, 9000),
        spur: [], einsatz: null, klinik: null, blitz: 0, ang: 0
      });
    }
    LFZ.forEach(starte);
  }

  function starte(a) {
    var p = ABLAUF[a.phase];
    a.dauer = rnd(p.dauer[0], p.dauer[1]);
    a.t = 0;
    a.blitz = 1;
    if (p.ziel === 'einsatz') {
      a.einsatz = { x: rnd(0.34, 0.98) * W, y: rnd(0.10, 0.92) * H };
      a.von = { x: a.x, y: a.y }; a.nach = a.einsatz; a.spur = [];
    } else if (p.ziel === 'klinik') {
      a.klinik = pick(KLINIKEN);
      a.von = { x: a.x, y: a.y }; a.nach = a.klinik; a.spur = [];
    } else if (p.ziel === 'station') {
      a.von = { x: a.x, y: a.y }; a.nach = a.heim; a.spur = [];
    } else {
      a.von = null; a.nach = null;
    }
  }

  function schritt(a, dt) {
    a.t += dt;
    if (a.nach) {
      var k = Math.min(1, a.t / a.dauer);
      var e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;   /* weich an/ab */
      a.x = a.von.x + (a.nach.x - a.von.x) * e;
      a.y = a.von.y + (a.nach.y - a.von.y) * e;
      a.ang = Math.atan2(a.nach.y - a.von.y, a.nach.x - a.von.x);
      a.spur.push([a.x, a.y]);
      if (a.spur.length > 260) a.spur.shift();
    }
    if (a.blitz > 0) a.blitz = Math.max(0, a.blitz - dt / 900);
    if (a.t >= a.dauer) {
      a.phase = (a.phase + 1) % ABLAUF.length;
      if (a.phase === 0) { a.einsatz = null; a.klinik = null; a.spur = []; }
      starte(a);
    }
  }

  function fahne(a) {
    var st = ABLAUF[a.phase].st, col = FMS[st];
    var fs = 11, numw = 17, pad = 7, hgt = 17;
    ctx.font = '500 ' + fs + 'px ui-monospace, Consolas, monospace';
    var txw = ctx.measureText(a.nm).width + pad * 2;
    var ox = a.x + 9, oy = a.y - hgt / 2;
    if (ox + numw + txw > W - 8) ox = a.x - 9 - (numw + txw);
    if (a.blitz > 0) {                       /* kurzer Puls beim Statuswechsel */
      ctx.globalAlpha = a.blitz * 0.55;
      ctx.fillStyle = col;
      ctx.fillRect(ox - 4, oy - 4, numw + txw + 8, hgt + 8);
      ctx.globalAlpha = 1;
    }
    ctx.fillStyle = col; ctx.fillRect(ox, oy, numw + txw, hgt);
    ctx.fillStyle = 'rgba(0,0,0,.26)'; ctx.fillRect(ox, oy, numw, hgt);
    ctx.fillStyle = '#fff';
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(st, ox + numw / 2, oy + hgt / 2 + 0.5);
    ctx.textAlign = 'left';
    ctx.fillText(a.nm, ox + numw + pad, oy + hgt / 2 + 0.5);
    ctx.beginPath(); ctx.arc(a.x, a.y, 2.6, 0, 6.2832); ctx.fill();
  }

  function klinik(k) {
    ctx.strokeStyle = 'rgba(255,255,252,.5)'; ctx.lineWidth = 1.4;
    ctx.strokeRect(k.x - 8, k.y - 8, 16, 16);
    ctx.fillStyle = 'rgba(255,255,252,.72)';
    ctx.font = 'bold 11px ui-monospace, Consolas, monospace';
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText('H', k.x, k.y + 0.5);
  }

  function size() {
    var r = cv.getBoundingClientRect();
    W = r.width; H = r.height;
    cv.width = W * dpr; cv.height = H * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    seed();
  }

  var vorher = 0;
  function draw(now) {
    var dt = Math.min(64, now - vorher || 16); vorher = now;
    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = LAND; ctx.fillRect(0, 0, W, H);

    ROADS.forEach(function (r) {
      ctx.beginPath();
      r.p.forEach(function (p, i) { i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); });
      ctx.strokeStyle = r.big ? 'rgba(107,116,112,.38)' : 'rgba(51,59,56,.55)';
      ctx.lineWidth = r.big ? 1.7 : 1; ctx.stroke();
    });

    STATIONEN.forEach(function (s) {
      ctx.strokeStyle = TEAL; ctx.lineWidth = 1.6;
      ctx.beginPath();
      ctx.moveTo(s.x - 5, s.y); ctx.lineTo(s.x + 5, s.y);
      ctx.moveTo(s.x, s.y - 5); ctx.lineTo(s.x, s.y + 5);
      ctx.stroke();
    });
    KLINIKEN.forEach(klinik);

    LFZ.forEach(function (a) {
      if (!reduce) schritt(a, dt);
      if (a.einsatz) {
        var p = (Math.sin(now / 500) + 1) / 2;
        ctx.strokeStyle = 'rgba(217,59,52,' + (0.75 - 0.4 * p) + ')'; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(a.einsatz.x, a.einsatz.y, 9 + 7 * p, 0, 6.2832); ctx.stroke();
        ctx.fillStyle = '#D93B34';
        ctx.beginPath(); ctx.arc(a.einsatz.x, a.einsatz.y, 3, 0, 6.2832); ctx.fill();
      }
      if (a.spur.length > 1) {
        ctx.beginPath();
        a.spur.forEach(function (p, i) { i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); });
        ctx.strokeStyle = TRACK; ctx.lineWidth = 1.6; ctx.stroke();
      }
      ctx.save(); ctx.translate(a.x, a.y); ctx.rotate(a.ang);
      ctx.fillStyle = '#fff';
      ctx.beginPath(); ctx.moveTo(7, 0); ctx.lineTo(-5, 3.6); ctx.lineTo(-5, -3.6);
      ctx.closePath(); ctx.fill(); ctx.restore();
      fahne(a);
    });

    requestAnimationFrame(draw);
  }

