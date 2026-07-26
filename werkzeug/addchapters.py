# -*- coding: utf-8 -*-
"""Ergaenzt das Brandbook um die Kapitel Profilbilder und Einsatz-Tagebuch."""
import base64

p = "book.tpl.html"
s = open(p, encoding="utf-8").read()

CSS = """
/* Profilbilder */
.pbgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(148px,1fr));gap:20px}
.pb{text-align:center}
.pb .rund{aspect-ratio:1;border-radius:50%;overflow:hidden;background:var(--sunk)}
.pb .rund svg{width:100%;height:100%;display:block}
.pb b{display:block;font-size:13.5px;margin-top:10px;font-weight:700}
.pb span{display:block;font-family:var(--fm);font-size:10.5px;letter-spacing:.09em;
  text-transform:uppercase;color:var(--muted);margin-top:2px}
.pbsizes{display:flex;gap:24px;align-items:flex-end;flex-wrap:wrap;padding:28px;
  background:var(--navy);border-radius:3px}
.pbsizes .it{text-align:center}
.pbsizes .it .rund{border-radius:50%;overflow:hidden;margin:0 auto}
.pbsizes .it svg{width:100%;height:100%;display:block}
.pbsizes .it span{display:block;font-family:var(--fm);font-size:10px;letter-spacing:.08em;
  color:rgba(255,255,252,.55);margin-top:9px}
/* Tagebuch */
.tbgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:18px}
.tbcard{border:1px solid var(--line);border-radius:3px;overflow:hidden;background:var(--card)}
.tbcard .art svg{width:100%;height:auto;display:block}
.tbcard .cap{padding:12px 14px;border-top:1px solid var(--line)}
.tbcard .cap b{display:block;font-size:13.5px}
.tbcard .cap span{font-family:var(--fm);font-size:10.5px;letter-spacing:.08em;
  color:var(--muted);display:block;margin-top:3px}
.stchip{display:inline-block;width:20px;height:20px;border-radius:2px;color:#fff;
  font-family:var(--fm);font-size:11px;line-height:20px;text-align:center;font-weight:700;
  vertical-align:-4px;margin-right:7px}
"""
s = s.replace("/* Vorlagen */", CSS + "\n/* Vorlagen */")

KAP = """
<!-- ===================================================== Profilbilder -->
<section>
  <div class="wrap">
    <div class="kicker">Profilbilder</div>
    <h2>Ein Bild, sechs Plattformen, beliebig viele Anl&#228;sse</h2>
    <p>Jede Plattform beschneidet rund und zeigt klein. Deshalb gilt &#252;berall
      dieselbe Fassung: das App-Icon, nicht die Hauptfassung. Der Hubschrauber ist
      3,1&#8202;:&#8202;1 breit und im runden Beschnitt schon unter 100&#8239;px kaum
      noch zu erkennen.</p>

    <div class="pbsizes" style="margin-top:28px">
      <div class="it"><div class="rund" style="width:170px;height:170px">{{SVG:pb_standard}}</div>
        <span>DISCORD &#183; 512</span></div>
      <div class="it"><div class="rund" style="width:110px;height:110px">{{SVG:pb_standard}}</div>
        <span>YOUTUBE &#183; 800</span></div>
      <div class="it"><div class="rund" style="width:86px;height:86px">{{SVG:pb_standard}}</div>
        <span>INSTAGRAM &#183; 320</span></div>
      <div class="it"><div class="rund" style="width:64px;height:64px">{{SVG:pb_standard}}</div>
        <span>FACEBOOK &#183; 170</span></div>
      <div class="it"><div class="rund" style="width:48px;height:48px">{{SVG:pb_standard}}</div>
        <span>X &#183; 400</span></div>
      <div class="it"><div class="rund" style="width:34px;height:34px">{{SVG:pb_standard}}</div>
        <span>TIKTOK &#183; 200</span></div>
    </div>
    <p class="small" style="margin-top:14px">Immer quadratisch hochladen, nie
      vorbeschneiden &#8212; jede Plattform schneidet selbst, und zwar unterschiedlich
      stark. Als PNG mit deckendem Hintergrund, damit Discord keine graue Fl&#228;che
      darunterlegt.</p>

    <h3 style="margin:46px 0 12px">Sondereditionen</h3>
    <p>Der Grundsatz ist streng: <strong>das Zeichen bleibt unangetastet.</strong>
      Ver&#228;ndert wird ausschlie&#223;lich der Ring und der Hintergrund dahinter.
      Damit bleibt VAR in jeder Edition sofort erkennbar, und niemand muss das Logo
      umzeichnen.</p>
    <div class="pbgrid" style="margin-top:26px">
      <div class="pb"><div class="rund">{{SVG:pb_standard}}</div>
        <b>Grundfassung</b><span>ganzj&#228;hrig</span></div>
      <div class="pb"><div class="rund">{{SVG:pb_pride}}</div>
        <b>Pride</b><span>Juni</span></div>
      <div class="pb"><div class="rund">{{SVG:pb_einheit}}</div>
        <b>Tag der Einheit</b><span>3. Oktober</span></div>
      <div class="pb"><div class="rund">{{SVG:pb_at}}</div>
        <b>Nationalfeiertag AT</b><span>26. Oktober</span></div>
      <div class="pb"><div class="rund">{{SVG:pb_ch}}</div>
        <b>Bundesfeier CH</b><span>1. August</span></div>
      <div class="pb"><div class="rund">{{SVG:pb_halloween}}</div>
        <b>Halloween</b><span>31. Oktober</span></div>
      <div class="pb"><div class="rund">{{SVG:pb_weihnachten}}</div>
        <b>Weihnachten</b><span>Dezember</span></div>
      <div class="pb"><div class="rund">{{SVG:pb_nacht}}</div>
        <b>24-Stunden-Event</b><span>anlassbezogen</span></div>
      <div class="pb"><div class="rund">{{SVG:pb_gold}}</div>
        <b>Invers</b><span>Jubil&#228;en</span></div>
      <div class="pb"><div class="rund">{{SVG:pb_vorlage}}</div>
        <b>Leere Vorlage</b><span>f&#252;r den Generator</span></div>
    </div>

    <h3 style="margin:46px 0 12px">Der Generator</h3>
    <p>Alle Editionen entstehen aus <em>einer</em> Datei. Sie enth&#228;lt eine leere
      Gruppe <code>#hintergrund</code> unter dem Zeichen und einen Ring dar&#252;ber
      &#8212; wer eine neue Edition braucht, ersetzt genau diese beiden Stellen. Kein
      Neuzeichnen, kein Verschieben, keine zweite Wortmarke.</p>
    <div class="grid g2" style="margin-top:22px">
<pre><span class="c">&lt;!-- VAR_profilbild.svg --&gt;</span>
&lt;svg viewBox="0 0 512 512"&gt;
  &lt;clipPath id="rund"&gt;&lt;circle cx="256" cy="256" r="256"/&gt;&lt;/clipPath&gt;
  &lt;g clip-path="url(#rund)"&gt;
    <span class="k">&lt;g id="hintergrund"&gt;</span>
      <span class="c">&lt;!-- hier austauschen --&gt;</span>
    <span class="k">&lt;/g&gt;</span>
    &lt;g id="zeichen"&gt;<span class="c">&lt;!-- unveraendert --&gt;</span>&lt;/g&gt;
  &lt;/g&gt;
  <span class="k">&lt;g id="ring"&gt;</span><span class="c">&lt;!-- Farbring --&gt;</span><span class="k">&lt;/g&gt;</span>
&lt;/svg&gt;</pre>
      <div>
        <ul class="rules">
          <li><b>Ringst&#228;rke</b>26&#8239;px bei 512 &#8212; gut 5&#8201;% des
            Durchmessers. Bei mehrfarbigen Ringen alle Segmente gleich breit.</li>
          <li><b>Was nie ver&#228;ndert wird</b>Hubschrauber, Kante, Wortmarke, deren
            Lage und der Kippwinkel. Wer das anfasst, macht eine neue Marke, keine
            Edition.</li>
          <li><b>Hintergrund</b>Fl&#228;che, Verlauf oder Muster &#8212; aber dunkel
            genug, dass Ivory und Gold darauf stehen. Faustregel: nicht heller als
            Stratos plus ein Viertel.</li>
          <li><b>Laufzeit</b>Editionen laufen h&#246;chstens zwei Wochen um den Anlass,
            dann zur&#252;ck zur Grundfassung. Sonst verliert die Ausnahme ihre
            Wirkung.</li>
        </ul>
      </div>
    </div>

    <h3 style="margin:46px 0 12px">Animierte Fassungen</h3>
    <p>Discord und einige andere Plattformen zeigen animierte Profilbilder. Dieselbe
      Datei, dieselbe Regel &#8212; bewegt wird nur der Hintergrund oder der Ring.</p>
    <div class="grid g3" style="margin-top:22px">
      <div class="card"><h4>Pride</h4><p class="small" style="margin:6px 0 0">
        Der Ring dreht sich einmal in 6&#8239;s gleichm&#228;&#223;ig. Kein Blinken,
        keine Farbwechsel &#8212; die Reihenfolge der Streifen bleibt.</p></div>
      <div class="card"><h4>Weihnachten</h4><p class="small" style="margin:6px 0 0">
        Schnee f&#228;llt langsam von oben nach unten, 12&#8239;s Schleife. Der
        Hubschrauber bleibt still stehen.</p></div>
      <div class="card"><h4>Halloween</h4><p class="small" style="margin:6px 0 0">
        Der orange Schein hinter der Kante pulsiert leicht, 4&#8239;s. Reduziert,
        nicht flackernd.</p></div>
      <div class="card"><h4>24-Stunden-Event</h4><p class="small" style="margin:6px 0 0">
        Sternenfeld zieht sehr langsam, dazu ein blauer Umlauf im Ring &#8212; wie ein
        Blaulicht, das einmal herumgeht.</p></div>
      <div class="card"><h4>Technisch</h4><p class="small" style="margin:6px 0 0">
        APNG bei 512&#8239;px, 20&#8239;fps, unter 8&#8239;MB. GIF nur als
        R&#252;ckfallebene &#8212; es bildet die Goldt&#246;ne nicht sauber ab.</p></div>
      <div class="card" style="border-color:var(--gold)"><h4>Die eine Grenze</h4>
        <p class="small" style="margin:6px 0 0">Nie den Rotor drehen lassen. Das
        Zeichen ist ein <em>stehender</em> Hubschrauber auf einer Kante &#8212; ein
        drehender Rotor macht daraus einen Flug und widerspricht der Idee.</p></div>
    </div>
  </div>
</section>

<!-- ===================================================== Reel-Overlays -->
<section>
  <div class="wrap">
    <div class="kicker">Bewegtbild</div>
    <h2>Das Einsatz-Tagebuch</h2>
    <p>Ein Einsatz hat einen festen Ablauf, und dieser Ablauf ist die Geschichte.
      Sechs Schritte, sechs Fenster f&#252;r Foto oder Video, dazwischen nichts zu
      entscheiden. Wer ein Reel bauen will, f&#252;llt sechs Kacheln &#8212; das
      Overlay ergibt sich von selbst.</p>

    <div class="grid g2" style="margin:28px 0 30px">
      <div class="card">
        <h3 style="margin-bottom:10px">Die sechs Schritte</h3>
        <table style="font-size:14px">
          <tbody>
            <tr><td><span class="stchip" style="background:rgb(140,10,10)">3</span>
              <strong>Alarmierung</strong></td><td>Der Melder geht, Stichwort erscheint</td></tr>
            <tr><td><span class="stchip" style="background:rgb(140,10,10)">3</span>
              <strong>Ausr&#252;cken</strong></td><td>Abflug von der Station</td></tr>
            <tr><td><span class="stchip" style="background:rgb(140,10,10)">4</span>
              <strong>Ankommen</strong></td><td>Landung am Einsatzort</td></tr>
            <tr><td><span class="stchip" style="background:rgb(140,10,10)">7</span>
              <strong>Abflug zur Klinik</strong></td><td>Patient an Bord</td></tr>
            <tr><td><span class="stchip" style="background:rgb(186,105,0)">8</span>
              <strong>Ankunft Klinik</strong></td><td>Am Transportziel eingetroffen</td></tr>
            <tr><td><span class="stchip" style="background:rgb(10,134,25)">1</span>
              <strong>Einsatzklar</strong></td><td>Frei &#252;ber Funk, R&#252;ckflug</td></tr>
          </tbody>
        </table>
        <p class="small" style="margin:14px 0 0">Ziffern und Farben stammen
          unver&#228;ndert aus <code>FMS_STATUS_COLORS</code> der Leitstelle. Das Reel
          spricht damit dieselbe Sprache wie das Lagebild.</p>
      </div>
      <div class="card">
        <h3 style="margin-bottom:14px">Wie daraus ein Reel wird</h3>
        <ul class="rules" style="border:0">
          <li><b>Sechs Fenster f&#252;llen</b>Je Schritt ein Hochformat-Clip von 3 bis
            5&#8239;s oder ein Standbild. Fehlt einer, f&#228;llt der Schritt aus der
            Leiste heraus.</li>
          <li><b>Kopfdaten einmal eingeben</b>Funkrufname, Stichwort, Station,
            Uhrzeiten. Der Rest ist Vorlage.</li>
          <li><b>&#220;berg&#228;nge</b>Harter Schnitt, kein Wischen. Die
            Fortschrittsleiste r&#252;ckt in 0,4&#8239;s weiter, die Statuskachel
            wechselt mit einem kurzen Puls in der neuen Farbe.</li>
          <li><b>L&#228;nge</b>24 bis 36&#8239;s. Dar&#252;ber springen die Leute ab,
            darunter tr&#228;gt der Ablauf nicht.</li>
        </ul>
      </div>
    </div>

    <div class="tbgrid">
      <figure class="tbcard" style="margin:0"><div class="art">{{SVG:tb_1_alarmierung}}</div>
        <figcaption class="cap"><b>1 &#183; Alarmierung</b><span>STATUS 3</span></figcaption></figure>
      <figure class="tbcard" style="margin:0"><div class="art">{{SVG:tb_2_ausruecken}}</div>
        <figcaption class="cap"><b>2 &#183; Ausr&#252;cken</b><span>STATUS 3</span></figcaption></figure>
      <figure class="tbcard" style="margin:0"><div class="art">{{SVG:tb_3_ankommen}}</div>
        <figcaption class="cap"><b>3 &#183; Ankommen</b><span>STATUS 4</span></figcaption></figure>
      <figure class="tbcard" style="margin:0"><div class="art">{{SVG:tb_4_abflug_klinik}}</div>
        <figcaption class="cap"><b>4 &#183; Abflug Klinik</b><span>STATUS 7</span></figcaption></figure>
      <figure class="tbcard" style="margin:0"><div class="art">{{SVG:tb_5_ankunft_klinik}}</div>
        <figcaption class="cap"><b>5 &#183; Ankunft Klinik</b><span>STATUS 8</span></figcaption></figure>
      <figure class="tbcard" style="margin:0"><div class="art">{{SVG:tb_6_einsatzklar}}</div>
        <figcaption class="cap"><b>6 &#183; Einsatzklar</b><span>STATUS 1</span></figcaption></figure>
      <figure class="tbcard" style="margin:0;border-color:var(--gold)">
        <div class="art">{{SVG:tb_leer}}</div>
        <figcaption class="cap"><b>Leeres Fenster</b>
          <span>SO SIEHT DIE VORLAGE AUS</span></figcaption></figure>
    </div>

    <h3 style="margin:46px 0 12px">Dieselbe Leiste, andere Anl&#228;sse</h3>
    <p>Das Ger&#252;st funktioniert auch ohne Einsatz. Nur Anzahl und Beschriftung der
      Schritte &#228;ndern sich, Aufbau und Ma&#223;e bleiben.</p>
    <div class="grid g3" style="margin-top:22px">
      <div class="card"><h4>Veranstaltung</h4><p class="small" style="margin:6px 0 0">
        Briefing &#8250; Start &#8250; Streckenabschnitt &#8250; Ziel &#8250;
        Gruppenbild. Die Statuskachel wird zur Etappennummer, die Farbe bleibt
        Gold.</p></div>
      <div class="card"><h4>Ausbildung</h4><p class="small" style="margin:6px 0 0">
        Ein Schritt je Lerneinheit. Die Fortschrittsleiste zeigt, wie weit der Kurs
        ist &#8212; das tr&#228;gt &#252;ber mehrere Beitr&#228;ge hinweg.</p></div>
      <div class="card"><h4>Normale Story</h4><p class="small" style="margin:6px 0 0">
        Nur Kopfzeile und Absenderkante, keine Leiste. Alles andere geh&#246;rt dem
        Bild.</p></div>
    </div>
  </div>
</section>
"""

MARKER = "<!-- ===================================================== 11 Sichere Zonen -->"
if MARKER not in s:
    MARKER = '<div class="kicker">Spickzettel</div>'
    s = s.replace(MARKER, KAP + "\n<section><div class=\"wrap\">\n" + MARKER, 1)
else:
    s = s.replace(MARKER, KAP + "\n" + MARKER, 1)

# Herleitung: echtes Foto statt Illustration
b64 = base64.b64encode(open("neu/_foto_original.png", "rb").read()).decode()
s = s.replace("{{SVG:_evo_foto}}",
              f'<img src="data:image/png;base64,{b64}" '
              f'alt="Rettungshubschrauber auf dem Dach einer Klinik" '
              f'style="width:100%;height:auto;display:block">')

open(p, "w", encoding="utf-8").write(s)
print("Kapitel ergaenzt, Foto eingebettet:", len(b64) // 1024, "KB")
