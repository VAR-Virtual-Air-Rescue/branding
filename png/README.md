# png

Rasterfassungen, erzeugt aus den SVGs in `../logo`, `../icon`, `../lockup` und
`../vorlagen`. **Nie umgekehrt** — die SVG ist der Master.

    VAR_logo_*        Hauptfassung, 512 bis 16 px
    VAR_signet_*      Signet ohne Wortmarke
    VAR_appicon_*     App-Icon, für alles unter 32 px
    VAR_profilbild_*  Profilbild-Grundfassung
    VAR_lockup_*      waagerechte und senkrechte Sperrung
    vorlage_*         fünf Social-Media-Vorlagen in 1080 px

Neu erzeugen aus `../werkzeug`:

    node render.mjs neu/n1_kante.svg ../../brand/png/VAR_logo_512.png 512

Der Renderer lädt die Schriften aus `fonts/` relativ zum Arbeitsverzeichnis —
also immer aus `brand/werkzeug` heraus aufrufen, sonst bricht er ab.
