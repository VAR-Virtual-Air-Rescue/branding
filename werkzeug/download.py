# -*- coding: utf-8 -*-
"""Haengt an jede Grafik im Brandbook einen Herunterladen-Knopf und, wo ein
Bildplatz vorgesehen ist, ein Plus zum Einsetzen eigener Aufnahmen.

Alles laeuft lokal: die SVG wird im Browser serialisiert, ueber ein Canvas
gerastert und als Datei gesichert. Hochgeladene Bilder werden als <image> in die
Grafik gelegt, sodass der anschliessende Download sie bereits enthaelt.
"""
BOOK = "book.tpl.html"
s = open(BOOK, encoding="utf-8").read()

CSS = """
/* ---------------- Herunterladen und Einsetzen ---------------- */
.dl-huelle{position:relative}
.dl-leiste{position:absolute;right:7px;top:7px;display:flex;gap:5px;z-index:9;
  opacity:0;transition:opacity .16s;pointer-events:none}
.dl-huelle:hover .dl-leiste,.dl-huelle:focus-within .dl-leiste{opacity:1;pointer-events:auto}
@media(hover:none){.dl-leiste{opacity:.9;pointer-events:auto}}
.dl-knopf{width:26px;height:26px;border-radius:2px;border:1px solid rgba(255,255,252,.28);
  background:rgba(10,16,32,.86);color:#FFFFFC;font-family:var(--fm);font-size:10px;
  font-weight:700;line-height:1;display:flex;align-items:center;justify-content:center;
  cursor:pointer;padding:0;backdrop-filter:blur(3px)}
.dl-knopf:hover{border-color:var(--gold);color:var(--gold)}
.dl-knopf:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
.dl-knopf.breit{width:34px}
.dl-huelle input.dl-datei{display:none}
.dl-fertig{position:absolute;left:7px;top:7px;z-index:9;background:rgba(10,16,32,.9);
  color:var(--gold);font-family:var(--fm);font-size:10px;letter-spacing:.08em;
  padding:3px 7px;border-radius:2px;opacity:0;transition:opacity .2s;pointer-events:none}
.dl-fertig.an{opacity:1}
"""

JS = """
<script>
(function(){
  /* Jede Grafik bekommt einen Herunterladen-Knopf. Wo ein Bildplatz vorgesehen
     ist, zusaetzlich ein Plus zum Einsetzen eigener Aufnahmen. */
  var MIT_BILD = '.tpl .art, .tbcard .art';       /* Vorlagen mit Fotoflaeche */
  var ALLE = [
    '.tile .stage', '.pb .rund', '.tpl .art', '.tbcard .art',
    '.step .box', '.vari .box', '.dd .item .box',
    '.light-panel', '.dark-panel', '.clearance .box', '.type-spec'
  ].join(', ');

  function dateiname(el){
    var k = el.closest('figure, .tile, .pb, .step, .vari, .item, section');
    var t = k && k.querySelector('.cap b, .cap, b, span');
    var n = (t ? t.textContent : 'VAR_grafik').trim().slice(0, 42);
    return 'VAR_' + n.replace(/[^\\wäöüÄÖÜß -]/g, '').replace(/\\s+/g, '_') || 'VAR_grafik';
  }

  function masse(svg){
    var vb = (svg.getAttribute('viewBox') || '0 0 512 512').split(/[\\s,]+/);
    return { w: parseFloat(vb[2]) || 512, h: parseFloat(vb[3]) || 512 };
  }

  function alsText(svg){
    var k = svg.cloneNode(true);
    k.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    k.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink');
    var m = masse(svg);
    k.setAttribute('width', m.w); k.setAttribute('height', m.h);
    return new XMLSerializer().serializeToString(k);
  }

  function lade(blob, name){
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = name;
    a.click();
    setTimeout(function(){ URL.revokeObjectURL(a.href); }, 4000);
  }

  function melde(huelle, text){
    var m = huelle.querySelector('.dl-fertig');
    if (!m) return;
    m.textContent = text; m.classList.add('an');
    setTimeout(function(){ m.classList.remove('an'); }, 1800);
  }

  function alsPng(svg, name, huelle){
    var m = masse(svg), txt = alsText(svg);
    var url = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(txt);
    var img = new Image();
    img.onload = function(){
      var sk = Math.min(3, Math.max(1, 1024 / Math.max(m.w, m.h)));
      var c = document.createElement('canvas');
      c.width = Math.round(m.w * sk); c.height = Math.round(m.h * sk);
      var x = c.getContext('2d');
      x.drawImage(img, 0, 0, c.width, c.height);
      c.toBlob(function(b){ lade(b, name + '.png'); melde(huelle, 'PNG gesichert'); });
    };
    img.onerror = function(){ melde(huelle, 'PNG nicht moeglich'); };
    img.src = url;
  }

  function knopf(txt, titel, breit){
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'dl-knopf' + (breit ? ' breit' : '');
    b.textContent = txt;
    b.title = titel;
    b.setAttribute('aria-label', titel);
    return b;
  }

  document.querySelectorAll(ALLE).forEach(function(el){
    var svg = el.querySelector('svg');
    if (!svg || el.querySelector('.dl-leiste')) return;
    el.classList.add('dl-huelle');

    var leiste = document.createElement('div');
    leiste.className = 'dl-leiste';
    var fertig = document.createElement('span');
    fertig.className = 'dl-fertig';
    el.appendChild(fertig);

    var name = dateiname(el);
    var bewegt = !!svg.querySelector('animate, animateTransform, animateMotion');

    var bPng = knopf('\\u2193', 'Als PNG sichern' + (bewegt ? ' (Standbild)' : ''));
    bPng.addEventListener('click', function(e){
      e.stopPropagation(); alsPng(svg, name, el);
    });
    leiste.appendChild(bPng);

    var bSvg = knopf('SVG', bewegt ? 'Als SVG sichern (mit Animation)' : 'Als SVG sichern', true);
    bSvg.addEventListener('click', function(e){
      e.stopPropagation();
      lade(new Blob([alsText(svg)], { type: 'image/svg+xml' }), name + '.svg');
      melde(el, 'SVG gesichert');
    });
    leiste.appendChild(bSvg);

    if (el.matches(MIT_BILD)) {
      var inp = document.createElement('input');
      inp.type = 'file'; inp.accept = 'image/*,video/*'; inp.className = 'dl-datei';
      el.appendChild(inp);

      var bPlus = knopf('+', 'Eigene Aufnahme einsetzen');
      bPlus.addEventListener('click', function(e){ e.stopPropagation(); inp.click(); });
      leiste.appendChild(bPlus);

      inp.addEventListener('change', function(){
        var f = inp.files[0]; if (!f) return;
        if (f.type.indexOf('video') === 0) {
          /* Aus einem Video den ersten brauchbaren Einzelbild ziehen */
          var v = document.createElement('video');
          v.muted = true; v.playsInline = true;
          v.onloadeddata = function(){
            v.currentTime = Math.min(1.2, (v.duration || 2) / 3);
          };
          v.onseeked = function(){
            var c = document.createElement('canvas');
            c.width = v.videoWidth; c.height = v.videoHeight;
            c.getContext('2d').drawImage(v, 0, 0);
            setze(svg, c.toDataURL('image/jpeg', 0.86), el);
            melde(el, 'Einzelbild gesetzt');
          };
          v.src = URL.createObjectURL(f); v.load();
        } else {
          var r = new FileReader();
          r.onload = function(){ setze(svg, r.result, el); melde(el, 'Bild gesetzt'); };
          r.readAsDataURL(f);
        }
      });
    }

    el.appendChild(leiste);
  });

  function setze(svg, datenUrl, huelle){
    var m = masse(svg);
    var alt = svg.querySelector('image[data-eigen]');
    if (alt) alt.remove();
    var bild = document.createElementNS('http://www.w3.org/2000/svg', 'image');
    bild.setAttribute('href', datenUrl);
    bild.setAttributeNS('http://www.w3.org/1999/xlink', 'xlink:href', datenUrl);
    bild.setAttribute('x', 0); bild.setAttribute('y', 0);
    bild.setAttribute('width', m.w); bild.setAttribute('height', m.h);
    bild.setAttribute('preserveAspectRatio', 'xMidYMid slice');
    bild.setAttribute('data-eigen', '1');
    svg.insertBefore(bild, svg.firstChild);
  }
})();
</script>
"""

if "dl-leiste" not in s:
    s = s.replace("/* Tagebuch */", CSS + "\n/* Tagebuch */")
    s = s.replace("</footer>", "</footer>\n" + JS)

# Hinweis im Vorlagenkapitel
s = s.replace("<p>Jede Vorlage endet mit der Absenderleiste:",
              "<p class=\"small\" style=\"margin-bottom:18px\">Mit dem Zeiger &#252;ber "
              "einer Grafik erscheinen oben rechts drei Knöpfe: <strong>&#8595;</strong> "
              "sichert ein PNG, <strong>SVG</strong> die Vektorfassung (bei bewegten "
              "Fassungen mitsamt Animation), <strong>+</strong> setzt eine eigene "
              "Aufnahme ein &#8212; danach enth&#228;lt auch der Download das Bild.</p>"
              "<p>Jede Vorlage endet mit der Absenderleiste:")

open(BOOK, "w", encoding="utf-8").write(s)
print("Download- und Plus-Knoepfe eingebaut")
