# Reel-Overlays — Einsatz-Tagebuch

Sechs Schritte, je ein Fenster für Foto oder Video. Statusziffern und Farben
stammen aus `FMS_STATUS_COLORS` in
`apps/dispatch/app/_helpers/fmsStatusColors.ts` des var-monorepo.

| Datei | Schritt | Status |
|---|---|---|
| `tb_1_alarmierung.svg` | Alarmierung | 3 |
| `tb_2_ausruecken.svg` | Ausrücken | 3 |
| `tb_3_ankommen.svg` | Ankommen | 4 |
| `tb_4_abflug_klinik.svg` | Abflug zur Klinik | 7 |
| `tb_5_ankunft_klinik.svg` | Ankunft Klinik | 8 |
| `tb_6_einsatzklar.svg` | Einsatzklar | 1 |
| `tb_leer.svg` | leere Vorlage | — |

1080 × 1920. Der Fußbereich ist 470 px hoch, darüber liegt ein Verlauf — dort
darf im Bild nichts Wichtiges sein. Texte über `../werkzeug/tagebuch.py`
ändern, dann neu erzeugen.
