# monitor_vllm.py
"""Monitor vLLM server performance."""

import time
import requests
from datetime import datetime

VLLM_URL = "http://localhost:8000/v1"

def check_server():
    """Check if vLLM server is responsive."""
    try:
        response = requests.get(f"{VLLM_URL}/models", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_metrics():
    """Get server metrics (if available)."""
    try:
        response = requests.get("http://localhost:8000/metrics", timeout=5)
        return response.text
    except:
        return None

def monitor(interval=30):
    """Monitor server continuously."""
    print("vLLM Server Monitor")
    print("=" * 60)
    
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "✅ ONLINE" if check_server() else "❌ OFFLINE"
        
        print(f"[{timestamp}] Server Status: {status}")
        
        metrics = get_metrics()
        if metrics:
            print(f"Metrics available at: http://localhost:8000/metrics")
        
        time.sleep(interval)

if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
