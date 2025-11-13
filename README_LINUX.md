# Linux Setup Guide for vLLM

## 🐧 Quick Start for Linux/Unix Systems

### Shell Scripts Available

All bash scripts are provided for easy server management:

```bash
# Make scripts executable (first time only)
chmod +x *.sh

# Install vLLM and dependencies
./install_vllm.sh

# Start vLLM server
./start_vllm.sh

# Start complete NL2Vis with vLLM
./start_nl2vis_vllm.sh

# Check server status
./check_status.sh

# Stop vLLM server
./stop_vllm.sh
```

---

## 📋 Detailed Instructions

### 1. Installation

#### Option A: Automated Installation
```bash
# Make install script executable
chmod +x install_vllm.sh

# Run installation script
./install_vllm.sh
```

#### Option B: Manual Installation
```bash
# Install vLLM
pip3 install vllm

# Install Ray (dependency)
pip3 install "ray>=2.9.0"

# Install other dependencies
pip3 install -r requirements.txt

# Make scripts executable
chmod +x start_vllm.sh start_nl2vis_vllm.sh stop_vllm.sh check_status.sh
```

### 2. Configuration

Edit `core/vllm_config.py`:
```python
USE_VLLM = True
VLLM_MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"
```

### 3. Verify Installation

```bash
# Run quick check
python3 quick_check.py

# Check GPU
nvidia-smi

# Verify vLLM installation
python3 -c "import vllm; print(f'vLLM version: {vllm.__version__}')"
```

---

## 🚀 Usage

### Basic Usage (2 Terminal Setup)

**Terminal 1 - Start Server:**
```bash
./start_vllm.sh
```

**Terminal 2 - Run NL2Vis:**
```bash
python3 run_evaluate.py
```

### Background Server (1 Terminal)

```bash
# Start server in background
./start_nl2vis_vllm.sh
```

This will:
1. Start vLLM server in background
2. Wait for initialization
3. Test connection
4. Run your NL2Vis application
5. Keep server running

---

## 🔧 Management Commands

### Start Server
```bash
# Foreground (blocks terminal)
./start_vllm.sh

# Background (with nohup)
nohup python3 core/vllm_server.py > vllm_server.log 2>&1 &
echo $! > .vllm_server.pid
```

### Check Status
```bash
# Comprehensive status check
./check_status.sh

# Quick check
curl http://localhost:8000/v1/models

# Check if running
ps aux | grep vllm

# Check port
lsof -i :8000
```

### Stop Server
```bash
# Using stop script
./stop_vllm.sh

# Manual stop
kill $(cat .vllm_server.pid)

# Force stop
kill -9 $(lsof -ti:8000)
```

### View Logs
```bash
# View server log (if running in background)
tail -f vllm_server.log

# Follow in real-time
tail -f vllm_server.log -n 100
```

---

## 🐛 Troubleshooting

### Permission Denied
```bash
# Make scripts executable
chmod +x *.sh

# If still issues
bash start_vllm.sh
```

### Command Not Found

**Python3:**
```bash
# Use python instead of python3
alias python3=python

# Or install python3
sudo apt-get install python3  # Debian/Ubuntu
sudo yum install python3      # RHEL/CentOS
```

**nvidia-smi:**
```bash
# Check NVIDIA driver
nvidia-smi

# If not found, install NVIDIA drivers
# See: https://docs.nvidia.com/cuda/cuda-installation-guide-linux/
```

### Port Already in Use
```bash
# Find process using port 8000
lsof -ti:8000

# Kill it
kill $(lsof -ti:8000)

# Or change port in core/vllm_config.py
VLLM_PORT = 8001
```

### GPU Not Detected
```bash
# Check GPU
lspci | grep -i nvidia

# Check CUDA
nvcc --version

# Check NVIDIA driver
nvidia-smi

# Install CUDA if needed
# See: https://developer.nvidia.com/cuda-downloads
```

### Out of Memory
```bash
# Edit core/vllm_config.py
VLLM_GPU_MEMORY_UTILIZATION = 0.75
VLLM_MAX_MODEL_LEN = 4096
```

---

## 📦 System Requirements

### Minimum
- **OS**: Ubuntu 20.04+ / Debian 11+ / RHEL 8+ / similar
- **Python**: 3.8 or higher
- **GPU**: NVIDIA GPU with 8GB+ VRAM
- **CUDA**: 11.8 or higher
- **RAM**: 16GB system RAM
- **Storage**: 20GB free space

### Recommended
- **OS**: Ubuntu 22.04 LTS
- **Python**: 3.10
- **GPU**: RTX 3090 / 4090 (24GB VRAM)
- **CUDA**: 12.1
- **RAM**: 32GB system RAM
- **Storage**: 50GB SSD

---

## 🔐 For Llama Models

### Accept License & Login

```bash
# Install HuggingFace CLI
pip3 install huggingface_hub

# Login to HuggingFace
huggingface-cli login

# Accept license at:
# https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct
```

---

## ⚙️ Advanced Configuration

### Run as System Service (systemd)

Create `/etc/systemd/system/vllm.service`:
```ini
[Unit]
Description=vLLM Server
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/NL2Vis
ExecStart=/usr/bin/python3 core/vllm_server.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable vllm
sudo systemctl start vllm
sudo systemctl status vllm
```

### Environment Variables

```bash
# Set in ~/.bashrc or ~/.profile
export VLLM_MODEL=/path/to/local/model
export CUDA_VISIBLE_DEVICES=0,1  # Use specific GPUs

# Reload
source ~/.bashrc
```

### Multiple GPU Setup

```bash
# In core/vllm_server.py, add to command:
--tensor-parallel-size 2  # For 2 GPUs
```

---

## 📊 Performance Optimization

### Monitor GPU Usage
```bash
# Watch GPU usage
watch -n 1 nvidia-smi

# Or use htop/gpustat
pip3 install gpustat
gpustat -i 1
```

### Benchmark
```bash
# Time server startup
time ./start_vllm.sh

# Benchmark inference
time python3 test_vllm.py
```

### Profile Memory
```bash
# Check memory before starting
free -h

# Monitor during runtime
watch -n 1 free -h
```

---

## 🔄 Development Workflow

### Development Mode
```bash
# Terminal 1: Server with auto-restart
while true; do
    python3 core/vllm_server.py
    echo "Server crashed. Restarting in 5 seconds..."
    sleep 5
done

# Terminal 2: Your development
python3 run_evaluate.py
```

### Testing
```bash
# Run all tests
python3 test_vllm.py
python3 test_nl2vis_vllm.py
python3 quick_check.py

# Test specific query
python3 -c "from core.vllm_client import safe_call_llm; print(safe_call_llm('Hello'))"
```

---

## 📝 Script Reference

### start_vllm.sh
Simple server launcher (foreground)

### start_nl2vis_vllm.sh
Complete startup with:
- Background server start
- Automatic testing
- Application launch

### stop_vllm.sh
Clean server shutdown:
- Reads PID file
- Sends SIGTERM
- Force kills if needed
- Cleans up resources

### check_status.sh
Comprehensive status check:
- Process status
- Port availability
- HTTP connectivity
- GPU status
- Configuration

### install_vllm.sh
Automated installation:
- Python version check
- CUDA detection
- GPU detection
- vLLM installation
- Dependency installation
- Script permissions

---

## 🆘 Common Issues

### Issue: "ImportError: No module named 'vllm'"
```bash
pip3 install vllm
```

### Issue: "CUDA out of memory"
```bash
# Reduce memory usage
vim core/vllm_config.py
# Set: VLLM_GPU_MEMORY_UTILIZATION = 0.70
```

### Issue: "Port 8000 already in use"
```bash
# Kill existing process
./stop_vllm.sh

# Or use different port
vim core/vllm_config.py
# Set: VLLM_PORT = 8001
```

### Issue: Scripts not executable
```bash
chmod +x *.sh
```

### Issue: Server starts but crashes immediately
```bash
# Check logs
tail -f vllm_server.log

# Common causes:
# - Wrong model name
# - Insufficient VRAM
# - CUDA not properly installed
```

---

## 🔗 Useful Commands

```bash
# View running processes
ps aux | grep python

# Check all Python processes
pgrep -af python

# Monitor system resources
htop

# Disk usage
df -h

# Check CUDA version
nvcc --version

# Python packages
pip3 list | grep vllm
pip3 list | grep torch

# Network connections
netstat -tlnp | grep 8000
```

---

## 📚 Additional Resources

- **CUDA Installation**: https://docs.nvidia.com/cuda/cuda-installation-guide-linux/
- **vLLM Documentation**: https://docs.vllm.ai/
- **HuggingFace Models**: https://huggingface.co/models
- **systemd Services**: https://www.freedesktop.org/software/systemd/man/systemd.service.html

---

## ✅ Quick Checklist

- [ ] Install Python 3.8+
- [ ] Install CUDA and NVIDIA drivers
- [ ] Install vLLM: `pip3 install vllm`
- [ ] Make scripts executable: `chmod +x *.sh`
- [ ] Configure model in `core/vllm_config.py`
- [ ] Accept Llama license (if using Llama)
- [ ] Test installation: `python3 quick_check.py`
- [ ] Start server: `./start_vllm.sh`
- [ ] Test connection: `python3 test_vllm.py`
- [ ] Run application: `python3 run_evaluate.py`

---

**For Windows users, see the `.bat` files instead.**
**For detailed setup, see `VLLM_SETUP_INSTRUCTIONS.md`**
