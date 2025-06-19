# Build stage
FROM node:18-alpine as build-stage

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY yarn.lock ./

# Install dependencies
RUN yarn install --legacy-peer-deps

# Copy source code
COPY . .

# Set environment variables for build
ENV VITE_BACKEND_URL="http://localhost:2999"
ENV VITE_API_BASE_URL="/api/v1"
ENV VITE_WEBSOCKET_URL="/ws"

# Build the application
RUN yarn build

# Production stage
FROM nginx:alpine as production-stage

# Copy built app from build stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
