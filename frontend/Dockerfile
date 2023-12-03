FROM node:21-alpine3.17
WORKDIR /usr/src/app
COPY geneappexplorer .
RUN npm ci && npm run build
CMD ["node",  ".output/server/index.mjs"]
