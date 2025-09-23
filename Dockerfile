# syntax=docker/dockerfile:1
# Scaffold Forge - Full Stack Application

# ===========================================
# STAGE 1: Frontend Dependencies
# ===========================================
FROM node:20-alpine AS frontend-deps
WORKDIR /app/frontend

# Copy package files
COPY frontend/package.json frontend/yarn.lock ./

# Install dependencies with cache mount
RUN --mount=type=cache,target=/root/.yarn \
    yarn install --silent

# ===========================================
# STAGE 2: Frontend Build
# ===========================================
FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend

# Copy dependencies from previous stage
COPY --from=frontend-deps /app/frontend/node_modules ./node_modules

# Copy package files
COPY frontend/package.json frontend/yarn.lock ./

# Copy source code
COPY frontend/src ./src
COPY frontend/public ./public
COPY frontend/tailwind.config.js ./
COPY frontend/postcss.config.js ./
COPY frontend/craco.config.js ./
COPY frontend/jsconfig.json ./
COPY frontend/components.json ./

# Build arguments
ARG REACT_APP_BACKEND_URL=""

# Build the React app
ENV REACT_APP_BACKEND_URL=$REACT_APP_BACKEND_URL
RUN yarn build

# ===========================================
# STAGE 3: Backend Dependencies
# ===========================================
FROM python:3.11-slim AS backend-deps

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY backend/requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# ===========================================
# STAGE 4: Production Image
# ===========================================
FROM python:3.11-slim AS production

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/app/.local/bin:$PATH"

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Set working directory
WORKDIR /app

# Copy Python dependencies from backend-deps stage
COPY --from=backend-deps /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-deps /usr/local/bin /usr/local/bin

# Copy backend code
COPY --chown=app:app backend/ ./

# Copy built frontend
COPY --from=frontend-build --chown=app:app /app/frontend/build ./static

# Create logs directory
RUN mkdir -p /app/logs && chown -R app:app /app/logs

# Switch to non-root user
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/status/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

# ===========================================
# STAGE 5: Development Image
# ===========================================
FROM python:3.11-slim AS development

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY backend/requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Install development dependencies
RUN pip install --no-cache-dir \
    watchdog \
    python-dotenv

# Copy backend code
COPY backend/ ./

# Copy built frontend
COPY --from=frontend-build /app/frontend/build ./static

# Create logs directory
RUN mkdir -p /app/logs

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/status/health || exit 1

# Run the application in development mode with hot reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ===========================================
# STAGE 6: Frontend Production
# ===========================================
FROM nginx:alpine AS frontend-production

# Copy built frontend from build stage
COPY --from=frontend-build /app/frontend/build /usr/share/nginx/html

# Copy nginx configuration
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]