FROM node:19-alpine
RUN apk update && apk add --no-cache libc6-compat
RUN npm install -g pnpm

WORKDIR /app
COPY .env ./
COPY package.json pnpm-lock.yaml ./
RUN pnpm install

COPY . .
RUN pnpm build

