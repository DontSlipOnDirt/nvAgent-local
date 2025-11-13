# Platform-Specific Quick Start Guide

## 🪟 Windows

### Installation
```powershell
pip install vllm
```

### Start Server
```powershell
# Option 1: Direct
python core/vllm_server.py

# Option 2: Batch file
start_vllm.bat

# Option 3: Complete startup
start_nl2vis_vllm.bat
```

### Testing
```powershell
python test_vllm.py
python test_nl2vis_vllm.py
python quick_check.py
```

### Stop Server
Press `Ctrl+C` in server terminal

---

## 🐧 Linux / Mac

### Installation
```bash
# Automated
chmod +x install_vllm.sh
./install_vllm.sh

# Manual
pip3 install vllm
```

### Start Server
```bash
# Option 1: Direct (foreground)
python3 core/vllm_server.py

# Option 2: Shell script (foreground)
chmod +x start_vllm.sh
./start_vllm.sh

# Option 3: Background with logging
nohup python3 core/vllm_server.py > vllm_server.log 2>&1 &
echo $! > .vllm_server.pid

# Option 4: Complete startup (background)
chmod +x start_nl2vis_vllm.sh
./start_nl2vis_vllm.sh
```

### Testing
```bash
python3 test_vllm.py
python3 test_nl2vis_vllm.py
python3 quick_check.py
```

### Management
```bash
# Check status
./check_status.sh

# Stop server
./stop_vllm.sh

# View logs (if running in background)
tail -f vllm_server.log
```

---

## 📋 Command Comparison

| Task | Windows | Linux/Mac |
|------|---------|-----------|
| **Install** | `pip install vllm` | `pip3 install vllm` or `./install_vllm.sh` |
| **Start Server** | `start_vllm.bat` | `./start_vllm.sh` |
| **Complete Startup** | `start_nl2vis_vllm.bat` | `./start_nl2vis_vllm.sh` |
| **Stop Server** | `Ctrl+C` | `./stop_vllm.sh` or `Ctrl+C` |
| **Check Status** | Check terminal | `./check_status.sh` |
| **View Logs** | Terminal output | `tail -f vllm_server.log` |
| **Python Command** | `python` | `python3` |
| **Make Executable** | N/A | `chmod +x *.sh` |

---

## 🔧 Configuration (Same for All Platforms)

Edit `core/vllm_config.py`:
```python
USE_VLLM = True  # Toggle
VLLM_MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"
VLLM_MAX_MODEL_LEN = 8192
VLLM_GPU_MEMORY_UTILIZATION = 0.90
```

---

## 📁 Available Scripts

### Windows Only
- `start_vllm.bat` - Start server
- `start_nl2vis_vllm.bat` - Complete startup

### Linux/Mac Only
- `start_vllm.sh` - Start server (foreground)
- `start_nl2vis_vllm.sh` - Complete startup (background)
- `stop_vllm.sh` - Stop server
- `check_status.sh` - Status check
- `install_vllm.sh` - Automated installer

### Cross-Platform (Python)
- `test_vllm.py` - Test server
- `test_nl2vis_vllm.py` - Test integration
- `quick_check.py` - Setup verification
- `monitor_vllm.py` - Server monitoring
- `core/vllm_server.py` - Server script

---

## 🚀 Typical Workflow

### Windows Development
```powershell
# Terminal 1
start_vllm.bat

# Terminal 2
python run_evaluate.py
```

### Linux Development
```bash
# Terminal 1
./start_vllm.sh

# Terminal 2
python3 run_evaluate.py
```

### Linux Production (Background)
```bash
# Start everything in background
./start_nl2vis_vllm.sh

# Check status
./check_status.sh

# View logs
tail -f vllm_server.log

# Stop when done
./stop_vllm.sh
```

---

## 🆘 Platform-Specific Issues

### Windows Issues

**Issue: "python not found"**
```powershell
# Try python3 or py
python3 core/vllm_server.py
# Or
py core/vllm_server.py
```

**Issue: "Access denied"**
- Run PowerShell as Administrator
- Check antivirus settings

**Issue: Port blocked by firewall**
- Allow Python through Windows Firewall
- Or change port in `core/vllm_config.py`

### Linux Issues

**Issue: "Permission denied" on scripts**
```bash
chmod +x *.sh
```

**Issue: "python3 not found"**
```bash
# Install Python 3
sudo apt-get install python3 python3-pip  # Debian/Ubuntu
sudo yum install python3 python3-pip      # RHEL/CentOS
```

**Issue: "nvidia-smi not found"**
```bash
# Install NVIDIA drivers
# See: https://docs.nvidia.com/cuda/cuda-installation-guide-linux/
```

**Issue: Process won't stop**
```bash
# Force kill
kill -9 $(lsof -ti:8000)

# Or
./stop_vllm.sh
```

---

## 📚 Documentation by Platform

### Windows Users
1. **Start here**: `QUICK_REFERENCE.md`
2. **Setup guide**: `VLLM_SETUP_INSTRUCTIONS.md`
3. **Full details**: `README_VLLM.md`

### Linux/Mac Users
1. **Start here**: `README_LINUX.md`
2. **Quick reference**: `QUICK_REFERENCE.md`
3. **Full details**: `README_VLLM.md`

### All Platforms
- **Implementation details**: `IMPLEMENTATION_SUMMARY.md`
- **Feature overview**: `IMPLEMENTATION_COMPLETE.md`

---

## ✅ Quick Verification

### Windows
```powershell
python quick_check.py
python test_vllm.py
```

### Linux/Mac
```bash
python3 quick_check.py
./check_status.sh
python3 test_vllm.py
```

---

## 🎯 Next Steps by Platform

### Windows
1. Install vLLM: `pip install vllm`
2. Start server: `start_vllm.bat`
3. Test: `python test_vllm.py`
4. Run: `python run_evaluate.py`

### Linux/Mac
1. Install: `./install_vllm.sh`
2. Start server: `./start_vllm.sh`
3. Test: `python3 test_vllm.py`
4. Run: `python3 run_evaluate.py`

---

**Choose the approach that fits your platform and workflow!**
