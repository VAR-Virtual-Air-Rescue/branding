# -*- coding: utf-8 -*-
"""Ergaenzt den Onepager um die Wissensdatenbank und die Statusgruppen-Pruefung
vor der Registrierung."""

p = "site.tpl.html"
s = open(p, encoding="utf-8").read()

CSS = """
/* ---------------- Wissensdatenbank ---------------- */
.wissen{display:grid;grid-template-columns:1.1fr 1fr;gap:0;border:1px solid var(--line)}
@media(max-width:900px){.wissen{grid-template-columns:1fr}}
.wissen .links{background:var(--surf);padding:40px 38px;border-right:1px solid var(--line)}
.wissen .rechts{background:var(--surf2);padding:0}
.kapitel{border-bottom:1px solid var(--line)}
.kapitel:last-child{border-bottom:0}
.kapitel .kopf{padding:18px 30px;display:flex;align-items:baseline;gap:14px}
.kapitel .kopf b{font-size:15px;color:var(--tx)}
.kapitel .kopf .n{font-family:var(--fm);font-size:11px;color:var(--gold);
  letter-spacing:.12em;flex:0 0 26px}
.kapitel .kopf .z{margin-left:auto;font-family:var(--fm);font-size:11px;color:var(--dim)}
.kapitel .seiten{padding:0 30px 20px 70px;display:flex;flex-wrap:wrap;gap:8px}
.kapitel .seiten span{font-size:12.5px;color:var(--dim);background:rgba(43,110,255,.07);
  border:1px solid var(--line);border-radius:2px;padding:3px 9px}
.zahl{display:flex;gap:0;flex-wrap:wrap;margin:26px 0 0;border-top:1px solid var(--line)}
.zahl div{padding:18px 30px 4px 0;margin-right:30px;border-right:1px solid var(--line)}
.zahl div:last-child{border-right:0}
.zahl b{display:block;font-family:var(--fm);font-size:27px;color:var(--gold);
  font-variant-numeric:tabular-nums;line-height:1.15}
.zahl span{font-size:11.5px;color:var(--dim);font-family:var(--fm);letter-spacing:.1em;
  text-transform:uppercase}

/* ---------------- Statuspruefung ---------------- */
.gate{border:1px solid var(--line);background:var(--surf);border-top:var(--kante) solid var(--gold)}
.gate .kopf{padding:34px 38px 0}
.gate .kopf h3{margin-bottom:10px}
.gate .kopf p{color:var(--dim);font-size:15.5px;max-width:60ch}
.gate .frage{padding:26px 38px 34px}
.gate .zaehler{font-family:var(--fm);font-size:11.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--gold);margin-bottom:14px}
.gate .text{font-size:clamp(18px,2.2vw,23px);font-weight:700;letter-spacing:-.015em;
  margin-bottom:22px;max-width:52ch;line-height:1.3}
.gate .optionen{display:flex;gap:12px;flex-wrap:wrap}
.gate .opt{display:flex;align-items:center;gap:12px;background:var(--surf2);
  border:1px solid var(--line);border-radius:2px;padding:12px 18px 12px 12px;
  cursor:pointer;font-family:inherit;font-size:14.5px;color:var(--tx);
  transition:border-color .15s,background .15s}
.gate .opt:hover{border-color:var(--gold)}
.gate .opt .zi{width:34px;height:34px;border-radius:2px;background:#3B4560;
  display:flex;align-items:center;justify-content:center;font-family:var(--fm);
  font-size:16px;font-weight:700;color:#fff;flex:0 0 34px}
.gate .opt.richtig{border-color:rgb(10,134,25);background:rgba(10,134,25,.12)}
.gate .opt.falsch{border-color:rgb(140,10,10);background:rgba(140,10,10,.12)}
.gate .opt:disabled{cursor:default}
.gate .hinweis{margin-top:20px;padding:16px 20px;border-left:3px solid var(--gold);
  background:rgba(213,165,7,.07);font-size:14.5px;color:var(--dim);display:none}
.gate .hinweis.an{display:block}
.gate .hinweis b{color:var(--tx);display:block;margin-bottom:4px}
.gate .hinweis a{color:var(--gold-hi)}
.gate .fortschritt{display:flex;gap:6px;padding:0 38px 26px}
.gate .fortschritt i{height:3px;flex:1;background:var(--line);border-radius:2px}
.gate .fortschritt i.ok{background:rgb(10,134,25)}
.gate .fortschritt i.jetzt{background:var(--gold)}
.gate .fertig{display:none;padding:34px 38px 38px;border-top:1px solid var(--line)}
.gate .fertig.an{display:block}
.gate .fertig h3{margin-bottom:12px}
.gate .fertig p{color:var(--dim);max-width:58ch}
"""
s = s.replace("/* ---------------- Mitmachen ---------------- */",
              CSS + "\n/* ---------------- Mitmachen ---------------- */")

WISSEN = """<!-- ================= Wissensdatenbank ================= -->
<section id="wissen">
  <div class="wrap">
    <div class="sechead">
      <span class="eyebrow">Wissensdatenbank</span>
      <h2>Der Teil, den man nicht wegklicken kann.</h2>
      <p class="lede">47 Seiten Fachwissen, geschrieben von Leuten, die es im echten
        Leben machen. Das ist keine Beilage zum Fliegen &#8212; das ist die Grundlage,
        auf der bei uns disponiert und geflogen wird.</p>
    </div>
    <div class="wissen">
      <div class="links">
        <h3 style="margin-bottom:14px">Und daran hängt die Ausbildung</h3>
        <p style="color:var(--dim);font-size:15.5px">Zu jedem Bereich gibt es im Hub
          einen Kurs mit einem Test in Moodle. Wer besteht, bekommt automatisch das
          Abzeichen, die Berechtigung im System und die Rolle im Discord &#8212; ohne
          dass jemand etwas von Hand freischalten muss.</p>
        <p style="color:var(--dim);font-size:15.5px">Der Weg ist gestaffelt:
          <strong style="color:var(--tx)">P1</strong> bringt dich ins Cockpit,
          <strong style="color:var(--tx)">P2</strong> und
          <strong style="color:var(--tx)">P3</strong> zu Winde und Nachtflug,
          <strong style="color:var(--tx)">D1</strong> bis
          <strong style="color:var(--tx)">D3</strong> auf die Leitstellenplätze.</p>
        <div class="zahl">
          <div><b>47</b><span>Seiten</span></div>
          <div><b>6</b><span>Bereiche</span></div>
          <div><b>8</b><span>Abzeichen</span></div>
        </div>
        <div style="margin-top:26px">
          <a class="btn ghost" href="#">Zur Wissensdatenbank</a>
        </div>
      </div>
      <div class="rechts">
        <div class="kapitel"><div class="kopf"><span class="n">01</span>
          <b>BOS-Funk</b><span class="z">5 SEITEN</span></div>
          <div class="seiten"><span>Grundlagen</span><span>Funkverkehr</span>
            <span>Funkbeispiel</span><span>OPTA</span><span>Statusgruppen</span></div></div>
        <div class="kapitel"><div class="kopf"><span class="n">02</span>
          <b>Luftrettung</b><span class="z">6 SEITEN</span></div>
          <div class="seiten"><span>Außenlandung</span><span>Landeplatz</span>
            <span>Luftrettungszentren</span><span>HEMS TC</span><span>Notarzt</span>
            <span>Betrieb Schweiz</span></div></div>
        <div class="kapitel"><div class="kopf"><span class="n">03</span>
          <b>Disponentenbereich</b><span class="z">3 SEITEN</span></div>
          <div class="seiten"><span>Disposition</span><span>How-to Disponent</span>
            <span>Stichwortkatalog</span></div></div>
        <div class="kapitel"><div class="kopf"><span class="n">04</span>
          <b>VAR-Systeme</b><span class="z">Leitstelle &amp; Client</span></div>
          <div class="seiten"><span>Leitstelle v2</span><span>Pilotenansicht</span>
            <span>VAR Client</span></div></div>
        <div class="kapitel"><div class="kopf"><span class="n">05</span>
          <b>VATSIM</b><span class="z">2 SEITEN</span></div>
          <div class="seiten"><span>Registrierung</span><span>Flugplan</span></div></div>
        <div class="kapitel"><div class="kopf"><span class="n">06</span>
          <b>Militärische Luftrettung</b><span class="z">2 SEITEN</span></div>
          <div class="seiten"><span>Einführung</span><span>SOP</span></div></div>
      </div>
    </div>
  </div>
</section>

"""
s = s.replace("<!-- ================= Mitmachen ================= -->",
              WISSEN + "<!-- ================= Mitmachen ================= -->")

GATE = """
    <div class="gate" id="gate" style="margin-top:44px">
      <div class="kopf">
        <h3>Vor dem Anmelden: drei Fragen.</h3>
        <p>Bei uns alarmiert dich ein Mensch, und du antwortest über Funk. Dafür
          brauchst du die Statusgruppen &#8212; sie sind das erste, was in jeder
          Einweisung drankommt, und die ganze Leitstelle läuft darauf. Wenn du sie
          hier hinbekommst, kennst du das Wichtigste vom ersten Flug an.</p>
      </div>
      <div class="fortschritt" id="g-fort"></div>
      <div class="frage" id="g-frage">
        <div class="zaehler" id="g-zaehler">Frage 1 von 3</div>
        <div class="text" id="g-text"></div>
        <div class="optionen" id="g-opt"></div>
        <div class="hinweis" id="g-hinweis"></div>
      </div>
      <div class="fertig" id="g-fertig">
        <h3>Das war es schon.</h3>
        <p>Genau so meldest du dich künftig über Funk. Im Hub wartet der Pilotenkurs
          mit dem Rest &#8212; Funkverkehr, Außenlandung, der Ablauf einer Alarmierung
          &#8212; und am Ende ein Test in Moodle. Wer besteht, ist freigeschaltet.</p>
        <div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:26px">
          <a class="btn" href="#">Jetzt registrieren</a>
          <a class="btn ghost" href="#wissen">Erst weiterlesen</a>
        </div>
      </div>
    </div>
"""
alt = s[s.index('<div class="close">'):s.index('</main>')]
neu = ('<section id="pruefung" style="padding-top:0;border-top:0">\n'
       '  <div class="wrap">' + GATE + '  </div>\n</section>\n\n'
       + alt.replace('<a class="btn" href="#">Jetzt registrieren</a>',
                     '<a class="btn" href="#pruefung">Zur Anmeldung</a>'))
s = s.replace(alt, neu)
s = s.replace('<a href="#mitmachen">Mitmachen</a>',
              '<a href="#wissen">Wissen</a>\n      <a href="#mitmachen">Mitmachen</a>')
s = s.replace('<a class="btn" href="#mitmachen">Registrieren</a>',
              '<a class="btn" href="#pruefung">Registrieren</a>')

JS = """
  /* ---------- Statusgruppen-Pruefung vor der Registrierung ---------- */
  var FRAGEN = [
    { t: 'Die Leitstelle hat dich alarmiert, du hebst ab und fliegst die Einsatzstelle an. Welchen Status meldest du?',
      opt: ['1', '3', '4', '7'], ok: 1,
      hilf: 'Status\\u00a03 hei\\u00dft: Einsatz \\u00fcbernommen, auf Anfahrt. Damit wei\\u00df die Leitstelle, dass du unterwegs bist \\u2014 und ab dann l\\u00e4uft deine Spur \\u00fcber das Lagebild.' },
    { t: 'Du bist gelandet, die Crew ist beim Patienten. Welcher Status geht jetzt raus?',
      opt: ['4', '5', '8', '2'], ok: 0,
      hilf: 'Status\\u00a04 bedeutet: am Einsatzort eingetroffen. Erst ab hier z\\u00e4hlt die Zeit vor Ort, nicht mehr die Anfahrt.' },
    { t: 'Der Patient ist an Bord und ihr fliegt die Klinik an. Was meldest du?',
      opt: ['3', '6', '7', '1'], ok: 2,
      hilf: 'Status\\u00a07 hei\\u00dft: Patient aufgenommen, einsatzgebunden im Transport. Am Transportziel folgt dann die\\u00a08, nach der \\u00dcbergabe die\\u00a01.' }
  ];
  var gIdx = 0;
  var gEl = document.getElementById('gate');
  if (gEl) {
    var gFort = document.getElementById('g-fort'), gZ = document.getElementById('g-zaehler'),
        gT = document.getElementById('g-text'), gO = document.getElementById('g-opt'),
        gH = document.getElementById('g-hinweis'), gF = document.getElementById('g-frage'),
        gFertig = document.getElementById('g-fertig');
    FRAGEN.forEach(function () { gFort.appendChild(document.createElement('i')); });

    function malen() {
      var f = FRAGEN[gIdx];
      gZ.textContent = 'Frage ' + (gIdx + 1) + ' von ' + FRAGEN.length;
      gT.textContent = f.t;
      gH.className = 'hinweis';
      gO.innerHTML = '';
      [].forEach.call(gFort.children, function (i, k) {
        i.className = k < gIdx ? 'ok' : (k === gIdx ? 'jetzt' : '');
      });
      f.opt.forEach(function (nr, k) {
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'opt';
        b.innerHTML = '<span class="zi" style="background:' +
          (FMS[nr] || '#3B4560') + '">' + nr + '</span>Status ' + nr;
        b.addEventListener('click', function () { antwort(b, k, f); });
        gO.appendChild(b);
      });
    }

    function antwort(btn, k, f) {
      [].forEach.call(gO.children, function (b) { b.disabled = true; });
      btn.classList.add(k === f.ok ? 'richtig' : 'falsch');
      if (k !== f.ok) gO.children[f.ok].classList.add('richtig');
      gH.className = 'hinweis an';
      gH.innerHTML = '<b>' + (k === f.ok ? 'Richtig.' : 'Nicht ganz.') + '</b>' +
        f.hilf + ' <a href="#wissen">Nachlesen in der Wissensdatenbank &#8250;</a>';
      setTimeout(function () {
        gIdx++;
        if (gIdx < FRAGEN.length) { malen(); }
        else {
          [].forEach.call(gFort.children, function (i) { i.className = 'ok'; });
          gF.style.display = 'none';
          gFertig.className = 'fertig an';
        }
      }, k === f.ok ? 1900 : 3600);
    }
    malen();
  }
"""
s = s.replace("  /* ---------- Lagebild ----------", JS + "\n  /* ---------- Lagebild ----------")

open(p, "w", encoding="utf-8").write(s)
print("Wissensdatenbank und Pruefung ergaenzt")
