# -------------------------
# Étape 1 : Build Next.js
# -------------------------
FROM node:20-alpine AS builder

WORKDIR /app

# Copier uniquement package.json et lockfile
COPY package.json yarn.lock* package-lock.json* ./

# Installer les dépendances
RUN yarn install --frozen-lockfile || npm install

# Copier le reste du code
COPY . .

# Build Next.js pour la production
RUN yarn build || npm run build

# -------------------------
# Étape 2 : Image de production
# -------------------------
FROM node:20-alpine AS runner

WORKDIR /app

# Copier package.json + node_modules depuis le builder
COPY --from=builder /app/package.json /app/yarn.lock* /app/package-lock.json* ./
COPY --from=builder /app/node_modules ./node_modules

# Copier le build Next.js et le frontend public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

# Copier le backend Express.js
COPY . .

# Exposer le port de l'application (Express.js + Next.js)
EXPOSE 3000

# Commande pour démarrer Express.js (qui servira Next.js via middleware)
CMD ["node", "server.js"]
