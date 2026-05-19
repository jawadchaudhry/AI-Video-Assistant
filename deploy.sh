#!/bin/bash
# Deployment script for AI Video Assistant

set -e

echo "========================================="
echo "AI Video Assistant - Deployment Script"
echo "========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if MISTRAL_API_KEY is set
if [ -z "$MISTRAL_API_KEY" ]; then
    echo -e "${RED}Error: MISTRAL_API_KEY is not set${NC}"
    echo "Please set your Mistral API key:"
    echo "  export MISTRAL_API_KEY=your_api_key_here"
    exit 1
fi

echo -e "${GREEN}MISTRAL_API_KEY is set${NC}"

# Build Docker image
echo -e "${YELLOW}Building Docker image...${NC}"
docker build -t ai-video-assistant .

echo -e "${GREEN}Build complete!${NC}"
echo ""
echo "To run locally:"
echo "  docker run -p 8501:8501 -e MISTRAL_API_KEY=$MISTRAL_API_KEY ai-video-assistant"
echo ""
echo "Or with docker-compose:"
echo "  MISTRAL_API_KEY=$MISTRAL_API_KEY docker-compose up"