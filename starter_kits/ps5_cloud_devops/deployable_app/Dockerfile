# Use Node.js Alpine base image for minimal footprint
FROM node:18-alpine

WORKDIR /app

# Copy dependency manifests and install dependencies
COPY backend/package*.json ./
RUN npm ci --only=production

# Copy backend application source code
COPY backend/ ./

# Expose port
EXPOSE 5000

# Set non-root user execution for security
USER node

CMD ["node", "server.js"]
