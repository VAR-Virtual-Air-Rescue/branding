# Das Brandbook ist eine fertige HTML-Datei -- es gibt nichts zu uebersetzen.
# Gebaut wird trotzdem im Container, damit die Zahlen im Buch (Dateien je
# Ordner) zum Stand des Images passen und nicht zum Stand des letzten Rechners,
# auf dem jemand das Skript laufen liess.
FROM python:3.12-alpine AS bau
WORKDIR /bau
# Der ganze Werkzeugordner, nicht nur die drei gebrauchten Dateien: das Buch
# zaehlt die Skripte darin und schriebe sonst "werkzeug/ 1" in die
# Bestandstabelle.
COPY werkzeug/ ./werkzeug/
COPY logo/ ./logo/
COPY lockup/ ./lockup/
COPY icon/ ./icon/
COPY profilbilder/ ./profilbilder/
COPY reel/ ./reel/
COPY vorlagen/ ./vorlagen/
COPY karte/ ./karte/
COPY herleitung/ ./herleitung/
COPY png/ ./png/
RUN python werkzeug/brandbook.py brandbook/index.html

FROM nginx:1.27-alpine

# Das Buch selbst.
COPY --from=bau /bau/brandbook/index.html /var/www/branding/index.html

# Danebengelegt, was das Buch verspricht: die Originaldateien, direkt
# abrufbar unter branding.virtualairrescue.com/logo/VAR_logo.svg usw.
COPY logo/        /var/www/branding/logo/
COPY lockup/      /var/www/branding/lockup/
COPY icon/        /var/www/branding/icon/
COPY profilbilder/ /var/www/branding/profilbilder/
COPY reel/        /var/www/branding/reel/
COPY vorlagen/    /var/www/branding/vorlagen/
COPY karte/       /var/www/branding/karte/
COPY herleitung/  /var/www/branding/herleitung/
COPY png/         /var/www/branding/png/
COPY README.md    /var/www/branding/README.md

# Der Onepager als Anschauungsstueck.
COPY website/ /var/www/branding/website/

# Die Kontoseite. Sie liegt hinter `auth_request` -- nginx laesst sie nur an
# Angemeldete heraus.
COPY konto/ /var/www/branding/konto/

COPY nginx.conf /etc/nginx/conf.d/default.conf

# nginx:alpine bringt einen eigenen Healthcheck nicht mit; Traefik nimmt einen
# Container sonst in den Lastverteiler, bevor er antwortet.
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1/ >/dev/null || exit 1

EXPOSE 80
