#!/bin/bash
# start_nl2vis_vllm.sh
# Complete startup script for NL2Vis with vLLM

echo "============================================================"
echo "Starting NL2Vis with vLLM Backend"
echo "============================================================"
echo ""

# Check if vLLM is enabled
python3 -c "from core.vllm_config import USE_VLLM; print(f'vLLM Enabled: {USE_VLLM}')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Cannot import vLLM config. Please check installation."
    exit 1
fi

echo "Step 1: Starting vLLM server in background..."
echo "Note: Server output will be saved to vllm_server.log"
echo ""

# Start vLLM server in background
nohup python3 core/vllm_server.py > vllm_server.log 2>&1 &
VLLM_PID=$!
echo "vLLM server started with PID: $VLLM_PID"

# Save PID to file for later cleanup
echo $VLLM_PID > .vllm_server.pid

echo ""
echo "Step 2: Waiting for server to initialize (30 seconds)..."
echo "You can check vllm_server.log for server status."
echo ""
sleep 30

echo ""
echo "Step 3: Testing server connection..."
python3 test_vllm.py 2>/dev/null
if [ $? -ne 0 ]; then
    echo ""
    echo "WARNING: Server test failed. The server might still be starting."
    echo "Options:"
    echo "  1. Wait a bit longer and press Enter to continue"
    echo "  2. Check vllm_server.log for errors"
    echo ""
    read -p "Press Enter to continue or Ctrl+C to abort..."
fi

echo ""
echo "============================================================"
echo "Step 4: Running NL2Vis..."
echo "============================================================"
echo ""

# Run NL2Vis (customize this to your needs)
python3 run_evaluate.py

echo ""
echo "============================================================"
echo "NL2Vis execution completed!"
echo ""
echo "To stop the vLLM server, run:"
echo "  kill $VLLM_PID"
echo "Or use: ./stop_vllm.sh"
echo "============================================================"
