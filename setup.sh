#!/bin/bash
# 🚀 Workshop MCP Server - Quick Setup Script (macOS/Linux)
# ===========================================================

set -e  # Exit on any error

# Color functions
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

success() { echo -e "${GREEN}✅ $1${NC}"; }
info() { echo -e "${CYAN}ℹ️  $1${NC}"; }
warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; }
step() { echo -e "${BLUE}🔧 $1${NC}"; }

echo -e "${BLUE}🚀 Workshop MCP Server - Quick Setup${NC}"
echo "====================================="
echo

# Check Python version
step "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        error "Python is not installed or not in PATH"
        info "Please install Python 3.12+ from https://python.org"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
success "Python found: $PYTHON_VERSION"

# Check if we're in the right directory
step "Verifying workshop directory..."
if [ ! -f "requirements.txt" ] || [ ! -f "server_workshop.py" ]; then
    error "Workshop files not found. Please run this script from the workshop directory."
    exit 1
fi
success "Workshop directory verified"

# Create virtual environment
step "Creating virtual environment..."
if [ -d "workshop-env" ]; then
    warning "Virtual environment already exists"
    read -p "Recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf workshop-env
        $PYTHON_CMD -m venv workshop-env
        success "Virtual environment recreated"
    else
        info "Using existing virtual environment"
    fi
else
    $PYTHON_CMD -m venv workshop-env
    success "Virtual environment created"
fi

# Activate virtual environment
step "Activating virtual environment..."
source workshop-env/bin/activate
success "Virtual environment activated"

# Upgrade pip
step "Upgrading pip..."
python -m pip install --upgrade pip --quiet
success "pip upgraded"

# Install dependencies
step "Installing workshop dependencies..."
info "This may take a few minutes..."
python -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    success "All dependencies installed successfully"
else
    error "Failed to install dependencies"
    exit 1
fi

# Verify installation
step "Verifying installation..."
python -c "import mcp, fastmcp; print('✅ Core dependencies working')"
if [ $? -eq 0 ]; then
    success "Installation verification completed"
else
    error "Verification failed"
    exit 1
fi

# Test server
step "Testing server script..."
python server_workshop.py --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    success "Server script is working"
else
    warning "Server script test had issues (may need .env configuration)"
fi

echo
echo -e "${GREEN}🎉 SETUP COMPLETED SUCCESSFULLY!${NC}"
echo "=================================="
echo
echo "NEXT STEPS:"
echo "1. 📖 Read: WORKSHOP_GUIDE_EN.md"
echo "2. 🚀 Test: python server_workshop.py --help"
echo "3. 🔧 Configure Claude Desktop"
echo
echo "REMEMBER:"
echo "⚠️  Always activate the environment: source workshop-env/bin/activate"
echo "⚠️  Your prompt should show (workshop-env) when active"
echo
echo "🆘 NEED HELP? Check SETUP_TROUBLESHOOTING.md"
echo
echo "Happy coding! 🚀"