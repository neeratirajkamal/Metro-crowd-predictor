# Stage 1: Build the React Frontend
FROM node:20-slim AS build-frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Setup the Python Backend
FROM python:3.12-slim
WORKDIR /app

# Install backend dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ ./backend/

# Copy built frontend assets from Stage 1
COPY --from=build-frontend /app/frontend/dist ./frontend/dist

# Set environment variables
ENV PYTHONPATH="/app/backend:/app"
ENV PORT=8080

# Cloud Run health checks and execution
EXPOSE 8080
CMD ["python", "backend/main.py"]
