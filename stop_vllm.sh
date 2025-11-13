#!/bin/bash
# stop_vllm.sh
# Stop the vLLM server

echo "Stopping vLLM server..."

# Check if PID file exists
if [ -f .vllm_server.pid ]; then
    VLLM_PID=$(cat .vllm_server.pid)
    
    # Check if process is running
    if ps -p $VLLM_PID > /dev/null 2>&1; then
        echo "Killing vLLM server process (PID: $VLLM_PID)..."
        kill $VLLM_PID
        sleep 2
        
        # Force kill if still running
        if ps -p $VLLM_PID > /dev/null 2>&1; then
            echo "Force killing..."
            kill -9 $VLLM_PID
        fi
        
        echo "✓ vLLM server stopped"
    else
        echo "vLLM server is not running (PID: $VLLM_PID)"
    fi
    
    # Clean up PID file
    rm -f .vllm_server.pid
else
    # Try to find and kill by port
    echo "No PID file found. Searching for process on port 8000..."
    VLLM_PID=$(lsof -ti:8000 2>/dev/null)
    
    if [ -n "$VLLM_PID" ]; then
        echo "Found process on port 8000 (PID: $VLLM_PID)"
        kill $VLLM_PID
        echo "✓ Process stopped"
    else
        echo "No vLLM server found running on port 8000"
    fi
fi

echo "Done."
