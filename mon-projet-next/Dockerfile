# Étape 1 : Build de l'application
FROM node:20-alpine AS builder

# Définir le répertoire de travail
WORKDIR /app

# Copier package.json et yarn.lock/npm lockfile
COPY package.json yarn.lock* package-lock.json* ./

# Installer les dépendances
RUN yarn install --frozen-lockfile || npm install

# Copier le reste du code source
COPY . .

# Construire l'application pour la production
RUN yarn build || npm run build

# Étape 2 : Image de production
FROM node:20-alpine AS runner

WORKDIR /app

# Copier seulement les fichiers nécessaires depuis le builder
COPY --from=builder /app/package.json /app/yarn.lock* /app/package-lock.json* ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules

# Exposer le port de l'app Next.js
EXPOSE 3000

# Démarrer l'application
CMD ["yarn", "start"]
CMD ["npm", "start"]
# ou si npm: CMD ["npm", "start"]
