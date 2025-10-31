#!/bin/bash

# AI Math Tutor Setup Script

echo "🎓 Setting up AI Math Tutor..."
echo ""

# Check Python version
echo "1. Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "   Found Python $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "2. Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   ✅ Virtual environment created"
else
    echo "   ℹ️  Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "3. Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "4. Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "   ✅ Dependencies installed successfully"
else
    echo "   ❌ Error installing dependencies"
    exit 1
fi

# Create .env file if it doesn't exist
echo ""
echo "5. Checking environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "   ✅ Created .env file from template"
    echo ""
    echo "   ⚠️  IMPORTANT: Edit .env and add your OPENAI_API_KEY"
    echo "   Run: nano .env (or use your preferred editor)"
else
    echo "   ℹ️  .env file already exists"
fi

# Create data directories
echo ""
echo "6. Creating data directories..."
mkdir -p data/documents data/vector_db
echo "   ✅ Data directories created"

echo ""
echo "============================================"
echo "✨ Setup complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OPENAI_API_KEY"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Run the tutor: python main.py"
echo ""
echo "Happy learning! 🎓"

