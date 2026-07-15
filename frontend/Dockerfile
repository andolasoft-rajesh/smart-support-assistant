# FILE: frontend/Dockerfile
FROM node:20-slim

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy application code
COPY . .

EXPOSE 5173

# Expose to 0.0.0.0 so we can access it from our browser
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]