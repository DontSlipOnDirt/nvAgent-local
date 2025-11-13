# 🚀 vLLM Quick Reference Card

## 📌 Most Important Commands

### First Time Setup

**Windows:**
```powershell
# 1. Install
pip install vllm

# 2. Check
python quick_check.py

# 3. Start server
python core/vllm_server.py
```

**Linux/Mac:**
```bash
# 1. Install
./install_vllm.sh

# 2. Check
python3 quick_check.py

# 3. Start server
./start_vllm.sh
```

### Daily Use

**Windows:**
```powershell
# Terminal 1: Server (keep running)
python core/vllm_server.py

# Terminal 2: Your work
python run_evaluate.py
```

**Linux/Mac:**
```bash
# Terminal 1: Server (keep running)
./start_vllm.sh

# Terminal 2: Your work
python3 run_evaluate.py
```

---

## ⚙️ Configuration (core/vllm_config.py)

```python
# Toggle backend
USE_VLLM = True   # Local vLLM
USE_VLLM = False  # Azure API

# Change model
VLLM_MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"

# Reduce memory
VLLM_MAX_MODEL_LEN = 4096
VLLM_GPU_MEMORY_UTILIZATION = 0.80
VLLM_QUANTIZATION = "awq"
```

---

## 🧪 Testing Commands

```powershell
python quick_check.py           # Full system check
python test_vllm.py             # Server test
python test_nl2vis_vllm.py      # Integration test
python monitor_vllm.py          # Monitor server
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Out of memory | Lower `VLLM_GPU_MEMORY_UTILIZATION` |
| Server won't start | Check GPU: `nvidia-smi` |
| Connection refused | Start server first |
| Want Azure API | Set `USE_VLLM = False` |

---

## 📚 Documentation Files

| File | Use When |
|------|----------|
| `IMPLEMENTATION_SUMMARY.md` | Overview of changes |
| `README_VLLM.md` | Quick reference |
| `VLLM_SETUP_INSTRUCTIONS.md` | Full setup guide |

---

## ✅ Quick Checklist

- [ ] Install vLLM: `pip install vllm`
- [ ] Run check: `python quick_check.py`
- [ ] Start server: `python core/vllm_server.py`
- [ ] Test: `python test_vllm.py`
- [ ] Use: `python run_evaluate.py`

---

## 💡 Pro Tips

1. Keep server running in background
2. Use `monitor_vllm.py` to check health
3. Start with defaults, optimize later
4. First run downloads model (~15GB)
5. Test simple queries first

---

## 🎯 File Structure

```
NL2Vis/
├── core/
│   ├── vllm_config.py       # Settings here! ⚙️
│   ├── vllm_client.py       # Client
│   └── vllm_server.py       # Server
├── test_vllm.py             # Quick test 🧪
├── quick_check.py           # Setup check ✅
└── start_vllm.bat           # Launcher 🚀
```

---

**For more details, see README_VLLM.md**
