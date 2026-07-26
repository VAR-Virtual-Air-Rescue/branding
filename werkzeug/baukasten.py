# -*- coding: utf-8 -*-
"""Baut den Reel-Baukasten ins Brandbook.

Ein funktionierendes Werkzeug, kein Mockup: sechs Fenster nehmen Bilder oder
Videos entgegen, das Overlay wird live auf ein Canvas gezeichnet, und heraus
kommt entweder ein Story-PNG je Schritt oder ein aufgezeichnetes Reel als WebM.

Alles laeuft lokal im Browser -- die Dateien werden nie hochgeladen.
"""
import base64

BOOK = "book.tpl.html"
s = open(BOOK, encoding="utf-8").read()

# Marke und Wortmarke als data-URI, damit das Canvas sie zeichnen kann
def duri(pfad):
    b = base64.b64encode(open(pfad, "rb").read()).decode()
    return f"data:image/svg+xml;base64,{b}"

BADGE = duri("neu/n1_kante.svg")

CSS = """
/* ---------------- Reel-Baukasten ---------------- */
.bk{display:grid;grid-template-columns:1fr 340px;gap:0;border:1px solid var(--line);
  border-top:4px solid var(--gold);background:var(--card)}
@media(max-width:960px){.bk{grid-template-columns:1fr}}
.bk .arbeit{padding:28px 30px}
.bk .vorschau{background:var(--navy);padding:26px;display:flex;flex-direction:column;
  align-items:center;gap:16px;border-left:1px solid var(--line)}
@media(max-width:960px){.bk .vorschau{border-left:0;border-top:1px solid var(--line)}}
.bk canvas{width:100%;max-width:264px;height:auto;background:#0B1020;border-radius:2px;
  box-shadow:0 12px 30px -14px rgba(0,0,0,.8)}
.bk .felder{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:22px}
@media(max-width:560px){.bk .felder{grid-template-columns:1fr}}
.bk label{display:block;font-family:var(--fm);font-size:10.5px;letter-spacing:.12em;
  text-transform:uppercase;color:var(--muted);margin-bottom:5px}
.bk input[type=text]{width:100%;background:var(--sunk);border:1px solid var(--line);
  border-radius:2px;padding:9px 11px;color:var(--ink);font-family:inherit;font-size:14px}
.bk input[type=text]:focus{outline:2px solid var(--gold);outline-offset:1px}
.slots{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
@media(max-width:700px){.slots{grid-template-columns:repeat(2,1fr)}}
.slot{border:1px dashed var(--line);border-radius:2px;padding:12px;cursor:pointer;
  transition:border-color .15s,background .15s;position:relative;overflow:hidden}
.slot:hover{border-color:var(--gold);background:var(--sunk)}
.slot.voll{border-style:solid;border-color:var(--gold)}
.slot.aktiv{box-shadow:inset 0 0 0 2px var(--gold)}
.slot .nr{font-family:var(--fm);font-size:10px;letter-spacing:.1em;color:var(--gold)}
.slot .nm{font-size:13px;font-weight:700;margin:3px 0 2px}
.slot .st{font-family:var(--fm);font-size:10.5px;color:var(--muted)}
.slot .mini{position:absolute;inset:0;object-fit:cover;width:100%;height:100%;opacity:.26}
.slot input[type=file]{display:none}
.bk .knoepfe{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}
.bk button{background:var(--gold);color:#00113A;border:0;border-radius:2px;
  padding:11px 20px;font-family:inherit;font-weight:700;font-size:14px;cursor:pointer}
.bk button.leer{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 1px var(--line)}
.bk button:disabled{opacity:.45;cursor:default}
.bk .hinw{font-size:12.5px;color:var(--muted);margin-top:14px;line-height:1.5}
.bk .zeitleiste{display:flex;gap:5px;margin-top:16px}
.bk .zeitleiste i{height:3px;flex:1;background:var(--line);border-radius:2px}
.bk .zeitleiste i.an{background:var(--gold)}
"""

WERKZEUG = """
<!-- ===================================================== Reel-Baukasten -->
<section>
  <div class="wrap">
    <div class="kicker">Werkzeug</div>
    <h2>Der Reel-Baukasten</h2>
    <p>Sechs Fenster f&#252;r Bilder oder Videos, oben die Kopfdaten &#8212; heraus
      kommt entweder ein Story-Bild je Schritt oder ein fertiges Reel. Alles
      passiert im Browser: <strong>keine Datei verl&#228;sst diesen Rechner.</strong></p>

    <div class="bk" style="margin-top:28px">
      <div class="arbeit">
        <div class="felder">
          <div><label for="bk-ruf">Funkrufname</label>
            <input type="text" id="bk-ruf" value="Christoph 51"></div>
          <div><label for="bk-stw">Stichwort</label>
            <input type="text" id="bk-stw" value="VU klemmt &#183; B27"></div>
          <div><label for="bk-sta">Station</label>
            <input type="text" id="bk-sta" value="Stuttgart"></div>
          <div><label for="bk-zeit">Startzeit (UTC)</label>
            <input type="text" id="bk-zeit" value="18:42"></div>
        </div>

        <label>Die sechs Schritte &#8212; anklicken und Datei w&#228;hlen</label>
        <div class="slots" id="bk-slots"></div>
        <div class="zeitleiste" id="bk-zeit-leiste"></div>

        <div class="knoepfe">
          <button type="button" id="bk-png">Story-Bild sichern</button>
          <button type="button" id="bk-alle" class="leer">Alle sechs sichern</button>
          <button type="button" id="bk-reel" class="leer">Reel aufzeichnen</button>
        </div>
        <div class="hinw" id="bk-status">Noch kein Material geladen. Ohne Datei zeigt
          das Fenster den Platzhalter &#8212; das Overlay steht trotzdem.</div>
      </div>

      <div class="vorschau">
        <canvas id="bk-canvas" width="1080" height="1920"></canvas>
        <div style="font-family:var(--fm);font-size:10.5px;letter-spacing:.1em;
          color:rgba(255,255,252,.5);text-align:center">1080 &#215; 1920 &#183; 9:16</div>
      </div>
    </div>

    <div class="grid g3" style="margin-top:26px">
      <div class="card"><h4>Was herauskommt</h4><p class="small" style="margin:6px 0 0">
        Story-Bilder als PNG in voller Aufl&#246;sung, das Reel als WebM. Beides
        l&#228;dt direkt herunter, ohne Zwischenstation.</p></div>
      <div class="card"><h4>Videos</h4><p class="small" style="margin:6px 0 0">
        Ein Videofenster spielt beim Aufzeichnen ab. Standbilder bekommen eine
        langsame Fahrt, damit das Reel nicht steht.</p></div>
      <div class="card" style="border-color:var(--gold)"><h4>F&#252;r die Endfassung</h4>
        <p class="small" style="margin:6px 0 0">Hier zeichnet die Systemschrift, weil
        Uniform nicht mitgeliefert wird. In der eingebauten Fassung im Hub geh&#246;rt
        die echte Schrift eingebunden.</p></div>
    </div>
  </div>
</section>
"""

JS = """
<script>
(function(){
  var cv = document.getElementById('bk-canvas');
  if (!cv) return;
  var ctx = cv.getContext('2d');
  var W = 1080, H = 1920, FUSS = 470;
  var GOLD = '#D5A507', IVORY = '#FFFFFC', NAVY = '#00113A';
  var FMS = { '1':'rgb(10,134,25)', '2':'rgb(10,134,25)', '3':'rgb(140,10,10)',
              '4':'rgb(140,10,10)', '7':'rgb(140,10,10)', '8':'rgb(186,105,0)' };

  var SCHRITTE = [
    { st:'3', t:'ALARMIERUNG',   u:'stichwort', min:0  },
    { st:'3', t:'AUSR\\u00dcCKEN', u:'abflug',   min:2  },
    { st:'4', t:'ANKOMMEN',      u:'vorort',    min:11 },
    { st:'7', t:'ABFLUG KLINIK', u:'patient',   min:29 },
    { st:'8', t:'ANKUNFT KLINIK',u:'klinik',    min:44 },
    { st:'1', t:'EINSATZKLAR',   u:'frei',      min:56 }
  ];

  var badge = new Image();
  badge.src = 'BADGE_URI';

  var medien = SCHRITTE.map(function(){ return null; });
  var aktiv = 0, aufnahme = false;

  function feld(id){ return (document.getElementById(id) || {}).value || ''; }

  function untertext(i){
    var s = SCHRITTE[i];
    if (s.u === 'stichwort') return feld('bk-stw');
    if (s.u === 'abflug')    return 'ABFLUG STATION ' + feld('bk-sta').toUpperCase();
    if (s.u === 'vorort')    return 'LANDUNG AM EINSATZORT';
    if (s.u === 'patient')   return 'PATIENT AN BORD';
    if (s.u === 'klinik')    return 'AM TRANSPORTZIEL';
    return 'FREI \\u00dcBER FUNK';
  }

  function uhrzeit(i){
    var z = feld('bk-zeit').split(':');
    var m = (parseInt(z[0],10)||18) * 60 + (parseInt(z[1],10)||42) + SCHRITTE[i].min;
    var hh = Math.floor(m/60) % 24, mm = m % 60;
    return (hh<10?'0':'')+hh+':'+(mm<10?'0':'')+mm;
  }

  function deckend(el, zoom){
    zoom = zoom || 1;
    var iw = el.videoWidth || el.naturalWidth, ih = el.videoHeight || el.naturalHeight;
    if (!iw || !ih) return false;
    var r = Math.max(W/iw, H/ih) * zoom;
    var w = iw*r, h = ih*r;
    ctx.drawImage(el, (W-w)/2, (H-h)/2, w, h);
    return true;
  }

  function zeichne(i, zoom){
    var s = SCHRITTE[i], col = FMS[s.st];
    ctx.clearRect(0,0,W,H);
    var m = medien[i];
    var ok = m ? deckend(m.el, zoom) : false;
    if (!ok){
      ctx.fillStyle = '#141C31'; ctx.fillRect(0,0,W,H);
      ctx.fillStyle = '#1B2540';
      for (var x=0; x<W; x+=52) ctx.fillRect(x,0,26,H);
      ctx.fillStyle = 'rgba(255,255,252,.45)';
      ctx.font = '600 34px ui-monospace, Consolas, monospace';
      ctx.textAlign = 'center';
      ctx.fillText('FOTO ODER VIDEO', W/2, H*0.34);
    }
    // Abdunklung unten
    var g = ctx.createLinearGradient(0, H-FUSS-260, 0, H);
    g.addColorStop(0,'rgba(0,8,28,0)'); g.addColorStop(1,'rgba(0,8,28,.93)');
    ctx.fillStyle = g; ctx.fillRect(0, H-FUSS-260, W, FUSS+260);

    // Kopfzeile
    if (badge.complete && badge.naturalWidth) ctx.drawImage(badge, 56, 210, 104, 104);
    ctx.textAlign = 'left'; ctx.fillStyle = IVORY;
    ctx.font = '600 26px ui-monospace, Consolas, monospace';
    ctx.fillText('VIRTUAL AIR RESCUE', 176, 280);
    ctx.fillStyle = GOLD; ctx.font = '600 22px ui-monospace, Consolas, monospace';
    ctx.fillText('EINSATZ-TAGEBUCH \\u00b7 ' + feld('bk-ruf').toUpperCase(), 176, 314);

    // Fortschrittsleiste
    var y0 = H - FUSS - 46, seg = (W-112)/(SCHRITTE.length-1);
    ctx.fillStyle = 'rgba(255,255,252,.22)'; ctx.fillRect(56, y0-1, W-112, 2);
    for (var k=0;k<SCHRITTE.length;k++){
      var px = 56 + seg*k, an = k===i, fertig = k<i;
      ctx.beginPath(); ctx.arc(px, y0, an?9:5, 0, 6.2832);
      ctx.fillStyle = an ? col : (fertig ? GOLD : 'rgba(255,255,252,.28)');
      ctx.fill();
      if (an){ ctx.beginPath(); ctx.arc(px,y0,16,0,6.2832);
        ctx.strokeStyle = col; ctx.lineWidth = 2; ctx.stroke(); }
    }

    // Statuskachel
    var ky = H - FUSS + 34;
    ctx.fillStyle = col; ctx.fillRect(56, ky, 112, 112);
    ctx.fillStyle = IVORY; ctx.textAlign = 'center';
    ctx.font = '800 68px system-ui, sans-serif';
    ctx.fillText(s.st, 112, ky+82);
    ctx.font = '600 18px ui-monospace, Consolas, monospace';
    ctx.globalAlpha = .6; ctx.fillText('STATUS', 112, ky+136); ctx.globalAlpha = 1;

    // Titel
    ctx.textAlign = 'left'; ctx.fillStyle = GOLD;
    ctx.font = '600 24px ui-monospace, Consolas, monospace';
    ctx.fillText('SCHRITT ' + (i+1) + ' VON ' + SCHRITTE.length, 200, ky+34);
    ctx.fillStyle = IVORY; ctx.font = '800 76px system-ui, sans-serif';
    ctx.fillText(s.t, 200, ky+112);
    ctx.fillStyle = GOLD; ctx.fillRect(200, ky+142, 150, 5);
    ctx.fillStyle = IVORY; ctx.globalAlpha = .85;
    ctx.font = '600 28px system-ui, sans-serif';
    ctx.fillText(untertext(i).toUpperCase(), 200, ky+196);
    ctx.globalAlpha = 1;

    // Uhrzeit
    ctx.textAlign = 'right';
    ctx.font = '700 44px ui-monospace, Consolas, monospace';
    ctx.fillText(uhrzeit(i), W-56, ky+82);
    ctx.globalAlpha = .5; ctx.font = '600 18px ui-monospace, Consolas, monospace';
    ctx.fillText('UTC', W-56, ky+112); ctx.globalAlpha = 1;

    ctx.fillStyle = GOLD; ctx.fillRect(0, H-8, W, 8);
  }

  // ---------- Fenster aufbauen ----------
  var slots = document.getElementById('bk-slots');
  var leiste = document.getElementById('bk-zeit-leiste');
  SCHRITTE.forEach(function(s, i){
    var d = document.createElement('div');
    d.className = 'slot' + (i===0 ? ' aktiv' : '');
    d.innerHTML = '<span class="nr">SCHRITT ' + (i+1) + '</span>' +
      '<div class="nm">' + s.t + '</div>' +
      '<div class="st">Status ' + s.st + '</div>' +
      '<input type="file" accept="image/*,video/*">';
    var inp = d.querySelector('input');
    d.addEventListener('click', function(e){
      aktiv = i; markiere();
      if (e.target !== inp) inp.click();
    });
    inp.addEventListener('change', function(){
      var f = inp.files[0]; if (!f) return;
      var url = URL.createObjectURL(f);
      var video = f.type.indexOf('video') === 0;
      var el = document.createElement(video ? 'video' : 'img');
      if (video){ el.muted = true; el.loop = true; el.playsInline = true; }
      el.onloadeddata = el.onload = function(){
        medien[i] = { el: el, video: video };
        var alt = d.querySelector('.mini'); if (alt) alt.remove();
        if (!video){ var mini = el.cloneNode(); mini.className = 'mini'; d.appendChild(mini); }
        d.classList.add('voll');
        aktiv = i; markiere(); zeichne(aktiv, 1);
        melde(zaehle() + ' von 6 Fenstern gef\\u00fcllt.');
      };
      el.src = url;
      if (video) el.load();
    });
    slots.appendChild(d);
    var b = document.createElement('i'); leiste.appendChild(b);
  });

  function zaehle(){ return medien.filter(Boolean).length; }
  function melde(t){ document.getElementById('bk-status').textContent = t; }
  function markiere(){
    [].forEach.call(slots.children, function(el,k){ el.classList.toggle('aktiv', k===aktiv); });
    [].forEach.call(leiste.children, function(el,k){ el.classList.toggle('an', k===aktiv); });
  }

  ['bk-ruf','bk-stw','bk-sta','bk-zeit'].forEach(function(id){
    var el = document.getElementById(id);
    if (el) el.addEventListener('input', function(){ zeichne(aktiv, 1); });
  });

  function sichere(i){
    zeichne(i, 1);
    cv.toBlob(function(b){
      var a = document.createElement('a');
      a.href = URL.createObjectURL(b);
      a.download = 'VAR_tagebuch_' + (i+1) + '_' + SCHRITTE[i].t.toLowerCase() + '.png';
      a.click();
    }, 'image/png');
  }

  document.getElementById('bk-png').addEventListener('click', function(){
    sichere(aktiv); melde('Story-Bild f\\u00fcr Schritt ' + (aktiv+1) + ' gesichert.');
  });
  document.getElementById('bk-alle').addEventListener('click', function(){
    SCHRITTE.forEach(function(_, i){ setTimeout(function(){ sichere(i); }, i*420); });
    melde('Sechs Story-Bilder werden gesichert.');
  });

  // ---------- Reel aufzeichnen ----------
  document.getElementById('bk-reel').addEventListener('click', function(){
    if (aufnahme) return;
    if (!window.MediaRecorder || !cv.captureStream){
      melde('Dieser Browser kann kein Reel aufzeichnen. Story-Bilder gehen trotzdem.');
      return;
    }
    aufnahme = true;
    var strom = cv.captureStream(30), teile = [];
    var typ = MediaRecorder.isTypeSupported('video/webm;codecs=vp9')
      ? 'video/webm;codecs=vp9' : 'video/webm';
    var rec = new MediaRecorder(strom, { mimeType: typ, videoBitsPerSecond: 6000000 });
    rec.ondataavailable = function(e){ if (e.data.size) teile.push(e.data); };
    rec.onstop = function(){
      var b = new Blob(teile, { type: 'video/webm' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(b);
      a.download = 'VAR_einsatz-tagebuch.webm';
      a.click();
      aufnahme = false;
      melde('Reel fertig \\u2014 ' + Math.round(b.size/1024/1024*10)/10 + ' MB, 24 Sekunden.');
    };

    var pro = 4000, i = 0, t0 = performance.now();
    medien.forEach(function(m){ if (m && m.video){ m.el.currentTime = 0; m.el.play(); } });
    rec.start();
    melde('Zeichnet auf \\u2026');

    (function tick(){
      var t = performance.now() - t0;
      i = Math.min(SCHRITTE.length-1, Math.floor(t / pro));
      var lokal = (t % pro) / pro;
      zeichne(i, 1 + lokal * 0.06);          // langsame Fahrt ins Bild
      aktiv = i; markiere();
      if (t < pro * SCHRITTE.length) requestAnimationFrame(tick);
      else { rec.stop(); medien.forEach(function(m){ if (m && m.video) m.el.pause(); }); }
    })();
  });

  badge.onload = function(){ zeichne(0, 1); };
  zeichne(0, 1);
})();
</script>
"""

JS = JS.replace("BADGE_URI", BADGE)

s = s.replace("/* ---------------- Reel-Baukasten ---------------- */", "")
s = s.replace("/* Tagebuch */", CSS + "\n/* Tagebuch */")

MARK = '<!-- ===================================================== 11 Sichere Zonen -->'
if MARK not in s:
    MARK = '<div class="kicker">Spickzettel</div>'
s = s.replace(MARK, WERKZEUG + "\n" + MARK, 1)
s = s.replace("</footer>", "</footer>\n" + JS)

open(BOOK, "w", encoding="utf-8").write(s)
print("Baukasten eingebaut, Badge:", len(BADGE) // 1024, "KB data-URI")
