#!/bin/bash

# Environment Setup Script for AI Math Tutor

set -e

echo "🚀 Setting up AI Math Tutor environment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    if [ -f backend/env.example ]; then
        cp backend/env.example .env
        echo "✅ Created .env file. Please edit it with your Azure OpenAI credentials."
        echo ""
        echo "Required environment variables:"
        echo "  - AZURE_OPENAI_API_KEY"
        echo "  - AZURE_OPENAI_ENDPOINT"
        echo "  - AZURE_OPENAI_API_VERSION"
        echo ""
        echo "⚠️  Please update .env file before continuing!"
        exit 1
    else
        echo "❌ env.example not found!"
        exit 1
    fi
else
    echo "✅ .env file already exists"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p data/vector_db
mkdir -p data/documents
mkdir -p data/sessions
echo "✅ Directories created"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Validate .env file has required variables
echo "🔍 Validating environment variables..."
if ! grep -q "AZURE_OPENAI_API_KEY =.*[^-]" .env; then
    echo "⚠️  AZURE_OPENAI_API_KEY is not set in .env file"
    echo "Please update .env file with your Azure OpenAI credentials"
    exit 1
fi

if ! grep -q "AZURE_OPENAI_ENDPOINT =.*[^-]" .env; then
    echo "⚠️  AZURE_OPENAI_ENDPOINT is not set in .env file"
    echo "Please update .env file with your Azure OpenAI credentials"
    exit 1
fi

echo "✅ Environment variables validated"

echo ""
echo "✨ Setup complete! You can now run:"
echo ""
echo "  Development mode:"
echo "    docker-compose -f docker-compose.dev.yml up"
echo ""
echo "  Production mode:"
echo "    docker-compose up -d"
echo ""
echo "  Access the application:"
echo "    - Web UI: http://localhost:3000"
echo "    - API: http://localhost:8000"
echo "    - API Docs: http://localhost:8000/docs"
echo ""

