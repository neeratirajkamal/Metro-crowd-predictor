#!/bin/bash
# Build script for Render static site deployment

echo "Installing frontend dependencies..."
cd frontend
npm install

echo "Building frontend for production..."
npm run build

echo "Build complete! Output in frontend/dist"
