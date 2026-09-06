# Keine Abhaengigkeiten, kein Build: der Dienst kommt mit dem aus, was Node
# mitbringt (node:http, node:crypto, fetch). Damit gibt es hier auch nichts,
# was veralten und zur Luecke werden koennte.
FROM node:22-alpine

WORKDIR /app
COPY package.json ./
COPY *.mjs ./

# Nicht als root. Das Bild bringt den Nutzer `node` bereits mit.
USER node

ENV NODE_ENV=production
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1:8080/api/auth/gesundheit >/dev/null || exit 1

CMD ["node", "server.mjs"]
