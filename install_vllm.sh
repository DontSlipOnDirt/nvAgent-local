#!/bin/bash
# install_vllm.sh
# Installation script for vLLM and dependencies

echo "============================================================"
echo "vLLM Installation Script for NL2Vis"
echo "============================================================"
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

# Check if Python 3.8+
if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "✓ Python version is compatible"
else
    echo "✗ Python 3.8+ is required"
    exit 1
fi

echo ""

# Check CUDA
echo "Checking CUDA installation..."
if command -v nvcc &> /dev/null; then
    CUDA_VERSION=$(nvcc --version | grep "release" | awk '{print $5}' | sed 's/,//')
    echo "✓ CUDA version: $CUDA_VERSION"
else
    echo "⚠ nvcc not found - CUDA may not be installed"
    echo "  vLLM requires CUDA for GPU acceleration"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""

# Check GPU
echo "Checking GPU..."
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader | while read line; do
        echo "  $line"
    done
    echo "✓ GPU detected"
else
    echo "⚠ nvidia-smi not found - cannot detect GPU"
fi

echo ""

# Install vLLM
echo "============================================================"
echo "Installing vLLM..."
echo "============================================================"
echo ""

read -p "Install vLLM now? (Y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    pip3 install vllm
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✓ vLLM installed successfully"
        
        # Verify installation
        VLLM_VERSION=$(python3 -c "import vllm; print(vllm.__version__)" 2>/dev/null)
        echo "  Version: $VLLM_VERSION"
    else
        echo ""
        echo "✗ vLLM installation failed"
        exit 1
    fi
else
    echo "Skipping vLLM installation"
fi

echo ""

# Install other dependencies
echo "============================================================"
echo "Installing other dependencies..."
echo "============================================================"
echo ""

read -p "Install Ray (required by vLLM)? (Y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    pip3 install "ray>=2.9.0"
fi

echo ""

# Check requirements.txt
if [ -f requirements.txt ]; then
    echo "Found requirements.txt"
    read -p "Install all requirements from requirements.txt? (Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        pip3 install -r requirements.txt
    fi
fi

echo ""

# Make scripts executable
echo "============================================================"
echo "Making scripts executable..."
echo "============================================================"
echo ""

chmod +x start_vllm.sh
chmod +x start_nl2vis_vllm.sh
chmod +x stop_vllm.sh
chmod +x check_status.sh
chmod +x install_vllm.sh

echo "✓ Scripts are now executable"

echo ""

# Final checks
echo "============================================================"
echo "Running quick check..."
echo "============================================================"
echo ""

python3 quick_check.py

echo ""
echo "============================================================"
echo "Installation Complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "  1. Configure model in core/vllm_config.py"
echo "  2. Accept model license (for Llama models):"
echo "     pip3 install huggingface_hub"
echo "     huggingface-cli login"
echo "  3. Start server: ./start_vllm.sh"
echo "  4. Test: python3 test_vllm.py"
echo ""
echo "For more information, see:"
echo "  - README_VLLM.md"
echo "  - VLLM_SETUP_INSTRUCTIONS.md"
echo "============================================================"
echo ""
