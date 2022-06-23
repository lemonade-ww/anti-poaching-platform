FROM node:18-alpine AS dev
WORKDIR /opt/app
COPY package.json yarn.lock .
RUN yarn install
COPY craco.config.js .
# Workaround for the latest node
ENV NODE_OPTIONS="--openssl-legacy-provider"
CMD ["yarn", "start"]

FROM node:18-alpine AS builder
WORKDIR /opt/app
COPY --from=dev /opt/app/node_modules node_modules
COPY public public
COPY src src
COPY package.json yarn.lock craco.config.js .
ENV NODE_OPTIONS="--openssl-legacy-provider"
RUN yarn build

FROM node:18-alpine AS production
WORKDIR /opt/app
RUN yarn global add serve
COPY --from=builder opt/app/build build
CMD ["serve", "build"]
