# frontend/support-assistant-frontend/Dockerfile
# Builds the Next.js app and serves it with `next start` on port 3000.
FROM node:20-slim

WORKDIR /app

# Install deps first so this layer caches when only source changes.
COPY package.json package-lock.json* ./
RUN npm ci

# App source. (.dockerignore keeps node_modules/.next out of the context.)
COPY . .

RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "start"]
