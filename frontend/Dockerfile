# Frontend multi-stage build for Next.js (Node 20)
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json* ./
COPY . .
RUN npm ci --legacy-peer-deps || npm install
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next .next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json
RUN npm ci --production --legacy-peer-deps || true
EXPOSE 3000
CMD ["npm", "start"]
