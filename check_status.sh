#!/bin/bash
# check_status.sh
# Check vLLM server status and system info

echo "============================================================"
echo "vLLM Server Status Check"
echo "============================================================"
echo ""

# Check if server PID file exists
if [ -f .vllm_server.pid ]; then
    VLLM_PID=$(cat .vllm_server.pid)
    echo "Server PID file found: $VLLM_PID"
    
    if ps -p $VLLM_PID > /dev/null 2>&1; then
        echo "✓ Server process is running"
    else
        echo "✗ Server process is NOT running (stale PID file)"
    fi
else
    echo "No PID file found"
fi

echo ""

# Check port 8000
echo "Checking port 8000..."
PORT_PID=$(lsof -ti:8000 2>/dev/null)
if [ -n "$PORT_PID" ]; then
    echo "✓ Process listening on port 8000 (PID: $PORT_PID)"
else
    echo "✗ No process listening on port 8000"
fi

echo ""

# Test HTTP connection
echo "Testing HTTP connection..."
if curl -s http://localhost:8000/v1/models > /dev/null 2>&1; then
    echo "✓ Server is responding to HTTP requests"
else
    echo "✗ Server is NOT responding"
fi

echo ""

# Check GPU
echo "GPU Status:"
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits | \
    while IFS=',' read -r idx name mem_used mem_total util; do
        echo "  GPU $idx: $name"
        echo "    Memory: ${mem_used}MB / ${mem_total}MB"
        echo "    Utilization: ${util}%"
    done
else
    echo "  nvidia-smi not found - cannot check GPU status"
fi

echo ""

# Check Python environment
echo "Python Environment:"
python3 --version 2>/dev/null || echo "  Python3 not found"

if python3 -c "import vllm" 2>/dev/null; then
    VLLM_VERSION=$(python3 -c "import vllm; print(vllm.__version__)" 2>/dev/null)
    echo "  vLLM version: $VLLM_VERSION"
else
    echo "  vLLM not installed"
fi

echo ""

# Check configuration
echo "Configuration:"
if python3 -c "from core.vllm_config import USE_VLLM, VLLM_MODEL_NAME; print(f'USE_VLLM={USE_VLLM}\nMODEL={VLLM_MODEL_NAME}')" 2>/dev/null; then
    python3 -c "from core.vllm_config import USE_VLLM, VLLM_MODEL_NAME; print(f'  USE_VLLM: {USE_VLLM}\n  Model: {VLLM_MODEL_NAME}')"
else
    echo "  Cannot read vLLM config"
fi

echo ""
echo "============================================================"

# Provide suggestions
if [ -f .vllm_server.pid ]; then
    VLLM_PID=$(cat .vllm_server.pid)
    if ! ps -p $VLLM_PID > /dev/null 2>&1; then
        echo "Suggestion: Clean up stale PID file with: rm .vllm_server.pid"
    fi
fi

PORT_PID=$(lsof -ti:8000 2>/dev/null)
if [ -z "$PORT_PID" ]; then
    echo "Suggestion: Start server with: ./start_vllm.sh"
fi

echo ""
