# png

Rasterfassungen, erzeugt aus den SVGs in `../logo`, `../icon`, `../lockup` und
`../vorlagen`. **Nie umgekehrt** — die SVG ist der Master.

    VAR_logo_*        Hauptfassung, 512 bis 16 px
    VAR_signet_*      Signet ohne Wortmarke
    VAR_appicon_*     App-Icon, für alles unter 32 px
    VAR_profilbild_*  Profilbild-Grundfassung
    VAR_lockup_*      waagerechte und senkrechte Sperrung
    vorlage_*         fünf Social-Media-Vorlagen in 1080 px

Wer eine Größe braucht, die hier fehlt, rendert sie aus der passenden SVG
(Schrift Uniform aus `../schrift`) und legt sie mit demselben Namensschema ab.
