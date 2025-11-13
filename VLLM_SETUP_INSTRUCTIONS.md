# VLLM_SETUP_INSTRUCTIONS.md
# Complete vLLM Setup Instructions for NL2Vis

## 🎯 What Was Implemented

Your NL2Vis system now supports **two modes**:
1. **Azure OpenAI API** (original, cloud-based)
2. **vLLM** (new, local LLM inference)

You can switch between them with a single configuration change!

---

## 📦 Step-by-Step Installation

### Step 1: Verify Hardware Requirements

Run this in PowerShell:
```powershell
nvidia-smi
```

**What you need:**
- NVIDIA GPU with 8GB+ VRAM
- 16GB+ system RAM
- CUDA 12.1+ (install if missing from https://developer.nvidia.com/cuda-downloads)

### Step 2: Install vLLM

```powershell
pip install vllm
```

This will take a few minutes as it installs PyTorch and other dependencies.

### Step 3: Configure vLLM

The configuration is already set in `core/vllm_config.py`. 

**To use vLLM (default):**
```python
# core/vllm_config.py
USE_VLLM = True
```

**To use Azure API:**
```python
# core/vllm_config.py
USE_VLLM = False
```

### Step 4: Choose Your Model

Edit `core/vllm_config.py`:

```python
# For best SQL/code generation (recommended)
VLLM_MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"

# Or use a different model:
# VLLM_MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"
# VLLM_MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
```

### Step 5: Accept Model License (for Llama models)

If using Llama models:

1. Go to: https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct
2. Click "Agree and access repository"
3. Login to HuggingFace CLI:
   ```powershell
   pip install huggingface_hub
   huggingface-cli login
   ```
4. Enter your HuggingFace token when prompted

---

## 🚀 Usage

### Quick Start (2 Terminal Setup)

**Terminal 1 - Start vLLM Server:**
```powershell
python core/vllm_server.py
```

Wait until you see:
```
INFO:     Uvicorn running on http://localhost:8000
INFO:     Application startup complete.
```

**Terminal 2 - Run NL2Vis:**
```powershell
python run_evaluate.py
```

Or for the web app:
```powershell
cd web_vis
python app.py
```

### Using the Batch File (Windows)

Double-click `start_vllm.bat` or run:
```powershell
.\start_vllm.bat
```

---

## 🧪 Testing

### Test 1: vLLM Server Connection
```powershell
python test_vllm.py
```

Expected output:
```
Testing vLLM server...
Response: 4
Tokens - Prompt: 12, Completion: 3
✅ vLLM server is working correctly!
```

### Test 2: NL2Vis Integration
```powershell
python test_nl2vis_vllm.py
```

Expected output:
```
USE_VLLM: True
Testing vLLM Client Integration
✅ Success! Response: [greeting]
Testing with Agent Import
✅ Agent integration working! Response: [answer]
✅ All tests passed! vLLM is properly integrated.
```

---

## ⚙️ Configuration Reference

### Memory Settings

If you get out-of-memory errors, edit `core/vllm_config.py`:

```python
# Reduce context length
VLLM_MAX_MODEL_LEN = 4096  # Default: 8192

# Reduce GPU memory usage
VLLM_GPU_MEMORY_UTILIZATION = 0.80  # Default: 0.90

# Enable quantization (uses ~4x less memory)
VLLM_QUANTIZATION = "awq"  # Default: None
```

### Performance Settings

```python
# Maximum tokens per response
VLLM_MAX_TOKENS = 4096  # Default: 4096

# Temperature (0.0 = deterministic)
VLLM_TEMPERATURE = 0.0  # Default: 0.0

# Data type
VLLM_DTYPE = "float16"  # Options: "auto", "float16", "bfloat16"
```

---

## 🔄 Switching Between Azure API and vLLM

### Method 1: Edit Config File

Edit `core/vllm_config.py`:
```python
USE_VLLM = True   # Use local vLLM
USE_VLLM = False  # Use Azure API
```

### Method 2: Check Current Mode

The system prints which mode it's using:
```
[CONFIG] Using vLLM with model: meta-llama/Meta-Llama-3-8B-Instruct
[AGENTS] Using vLLM client
[CHAT_MANAGER] Using vLLM client
```

Or:
```
[CONFIG] vLLM not configured, using Azure OpenAI API
[AGENTS] Using core.llm (Azure OpenAI)
[CHAT_MANAGER] Using core.llm (Azure OpenAI)
```

---

## 🐛 Troubleshooting

### Problem: "CUDA out of memory"

**Solutions (try in order):**

1. Reduce context length:
   ```python
   VLLM_MAX_MODEL_LEN = 4096
   ```

2. Lower GPU memory usage:
   ```python
   VLLM_GPU_MEMORY_UTILIZATION = 0.75
   ```

3. Enable quantization:
   ```python
   VLLM_QUANTIZATION = "awq"
   # Note: Model must support AWQ quantization
   ```

4. Use a smaller model:
   ```python
   VLLM_MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
   ```

### Problem: "Connection refused" or "Server not responding"

**Check if server is running:**
```powershell
# In a new terminal
python test_vllm.py
```

**Start the server:**
```powershell
python core/vllm_server.py
```

### Problem: "Model not found" or download errors

**For Llama models:**
1. Accept the license: https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct
2. Login: `huggingface-cli login`

**For other models:**
- Check model name is correct
- Ensure you have internet connection for first download

### Problem: Slow inference

**Check GPU usage:**
```powershell
nvidia-smi
```

**Solutions:**
1. Increase GPU memory:
   ```python
   VLLM_GPU_MEMORY_UTILIZATION = 0.95
   ```

2. Use float16:
   ```python
   VLLM_DTYPE = "float16"
   ```

3. Check you're using GPU (not CPU)

### Problem: Server crashes or hangs

**Restart the server:**
1. Press Ctrl+C in the server terminal
2. Wait a few seconds
3. Restart: `python core/vllm_server.py`

**Check logs for errors**

---

## 📊 Model Recommendations by Hardware

| Your GPU | Recommended Model | Config |
|----------|-------------------|--------|
| RTX 3060 (8GB) | Llama-3-8B + quantization | `VLLM_QUANTIZATION = "awq"` |
| RTX 3070 (8GB) | Llama-3-8B | Default |
| RTX 3080 (10GB) | Llama-3-8B | Default |
| RTX 3090 (24GB) | Llama-3-70B | `VLLM_MODEL_NAME = "meta-llama/Meta-Llama-3-70B-Instruct"` |
| RTX 4060 (8GB) | Llama-3-8B | Default |
| RTX 4070 (12GB) | Mistral-7B or Llama-3-8B | Default |
| RTX 4080 (16GB) | Llama-3-13B | Default |
| RTX 4090 (24GB) | Llama-3-70B | `tensor_parallel_size = 2` if needed |

---

## 📁 File Structure Created

```
NL2Vis/
├── core/
│   ├── vllm_config.py          ✅ NEW - vLLM configuration
│   ├── vllm_client.py          ✅ NEW - vLLM client wrapper
│   ├── vllm_server.py          ✅ NEW - Server startup script
│   ├── api_config.py           ✏️ MODIFIED - Added vLLM toggle
│   ├── agents.py               ✏️ MODIFIED - Use vLLM or API
│   └── chat_manager.py         ✏️ MODIFIED - Use vLLM or API
│
├── web_vis/core/
│   ├── vllm_config.py          ✅ NEW - Config import
│   ├── vllm_client.py          ✅ NEW - Client import
│   ├── agents.py               ✏️ MODIFIED - Use vLLM or API
│   └── chat_manager.py         ✏️ MODIFIED - Use vLLM or API
│
├── test_vllm.py                ✅ NEW - Test server
├── test_nl2vis_vllm.py         ✅ NEW - Test integration
├── monitor_vllm.py             ✅ NEW - Monitor server
├── start_vllm.bat              ✅ NEW - Windows launcher
├── README_VLLM.md              ✅ NEW - Quick reference
├── VLLM_SETUP_INSTRUCTIONS.md  ✅ NEW - This file
└── requirements.txt            ✏️ MODIFIED - Added vLLM
```

---

## 🎓 Understanding the Architecture

### How It Works

1. **Configuration Layer** (`vllm_config.py`):
   - Stores all vLLM settings
   - `USE_VLLM` flag controls which backend to use

2. **Client Layer** (`vllm_client.py`):
   - Wraps vLLM's OpenAI-compatible API
   - Mirrors the interface of `llm.py` for compatibility
   - Handles logging, retries, token counting

3. **Server Layer** (`vllm_server.py`):
   - Starts vLLM's OpenAI-compatible server
   - Loads model and serves requests

4. **Integration Layer** (`agents.py`, `chat_manager.py`):
   - Automatically detects if vLLM is enabled
   - Falls back to Azure API if vLLM is disabled
   - No code changes needed to switch!

### Request Flow (vLLM Mode)

```
User Query
    ↓
ChatManager
    ↓
Agent (Processor/Composer/Validator)
    ↓
LLM_API_FUC → vllm_client.safe_call_llm()
    ↓
vLLM Server (localhost:8000)
    ↓
Local LLM (e.g., Llama-3-8B)
    ↓
Response → Agent → ChatManager → User
```

### Request Flow (Azure API Mode)

```
User Query
    ↓
ChatManager
    ↓
Agent (Processor/Composer/Validator)
    ↓
LLM_API_FUC → llm.safe_call_llm()
    ↓
Azure OpenAI API
    ↓
GPT-4o
    ↓
Response → Agent → ChatManager → User
```

---

## 🚦 Next Steps

1. **Start the vLLM server** (Terminal 1)
2. **Run a test** to verify it works
3. **Try your NL2Vis workflow** (Terminal 2)
4. **Monitor performance** and adjust settings if needed
5. **Compare results** between vLLM and Azure API

---

## 📚 Additional Resources

- **vLLM Documentation**: https://docs.vllm.ai/
- **vLLM GitHub**: https://github.com/vllm-project/vllm
- **Model Hub**: https://huggingface.co/models
- **CUDA Toolkit**: https://developer.nvidia.com/cuda-downloads

---

## ✅ Verification Checklist

- [ ] GPU has 8GB+ VRAM
- [ ] CUDA is installed
- [ ] vLLM is installed (`pip install vllm`)
- [ ] Model license accepted (for Llama)
- [ ] HuggingFace CLI logged in
- [ ] `USE_VLLM = True` in `core/vllm_config.py`
- [ ] vLLM server started and ready
- [ ] `test_vllm.py` passes
- [ ] `test_nl2vis_vllm.py` passes
- [ ] NL2Vis works with vLLM backend

---

## 🆘 Getting Help

If you encounter issues:

1. **Check the console output** for error messages
2. **Run the test scripts** to isolate the problem
3. **Try reducing memory settings** if OOM errors
4. **Switch to Azure API temporarily** to verify NL2Vis still works
5. **Check vLLM GitHub issues** for similar problems

Remember: You can always switch back to Azure API by setting `USE_VLLM = False`!
