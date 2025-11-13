# NL2Vis with vLLM Setup Guide

This guide explains how to set up and run NL2Vis with local LLM inference using vLLM instead of Azure OpenAI API.

---

## 📋 Prerequisites

- **Python 3.8+**
- **CUDA-capable GPU** (NVIDIA) with at least 8GB VRAM for 7B models
- **Linux or WSL2** (vLLM has limited Windows support)

---

## 🚀 Setup with uv (Recommended)

### 1. Install uv
```bash
# Linux/Mac/WSL
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

### 2. Create and activate environment
```bash
# Navigate to project directory
cd NL2Vis

# Create virtual environment with uv
uv venv

# Activate it
source .venv/bin/activate  # Linux/Mac/WSL
# Or on Windows PowerShell: .venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
# Install all dependencies including vLLM
uv pip install -r requirements.txt
```

### 4. Configure vLLM
Edit `core/vllm_config.py`:
```python
USE_VLLM = True  # Toggle: True = vLLM, False = Azure API

# Choose your model
VLLM_MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"
# Or for testing (smaller model):
# VLLM_MODEL_NAME = "HuggingFaceTB/SmolLM2-135M-Instruct"

# Adjust GPU memory if needed
VLLM_GPU_MEMORY_UTILIZATION = 0.90  # Use 90% of available VRAM
```

### 5. Authenticate with Hugging Face (for gated models)
```bash
# For Llama models, you need HF access token
pip install huggingface-hub  # or: uv pip install huggingface-hub
huggingface-cli login

# Accept license at: https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct
```

---

## 🎯 Running the System

**Important**: Make sure your virtual environment is activated first!
```bash
# Activate venv (do this once per terminal session)
source .venv/bin/activate  # Linux/Mac/WSL
# Or: .venv\Scripts\Activate.ps1  # Windows PowerShell
```

### Two-Step Process (Recommended)

**Step 1: Start vLLM Server**
```bash
# Terminal 1 - Start the vLLM inference server
python -m core.vllm_server

# Wait for server to load model (may take 1-2 minutes)
# You'll see: "Uvicorn running on http://0.0.0.0:8000"
```

**Step 2: Test Connection**
```bash
# Terminal 2 - Test that server is working (activate venv first!)
python test_vllm.py

# If successful, you'll see:
# ✓ vLLM server connection successful
# ✓ Model response received
```

**Step 3: Run Your Application**
```bash
# Terminal 2 - Run evaluation
python run_evaluate.py

# Or run web interface
python web_vis/app.py
```

### Alternative: Quick Test
```bash
# Test integration end-to-end
python test_nl2vis_vllm.py
```

### Using uv run (alternative)
If you don't want to activate the venv, you can use `uv run` instead:
```bash
uv run test_vllm.py
uv run run_evaluate.py
```

---

## 📁 File Reference

### Configuration Files
- **`core/vllm_config.py`** - Main configuration (toggle USE_VLLM, set model, adjust memory)
- **`core/api_config.py`** - Azure API config (auto-overridden when USE_VLLM=True)

### Core Files
- **`core/vllm_server.py`** - Starts vLLM OpenAI-compatible server
- **`core/vllm_client.py`** - Client that connects to vLLM server
- **`core/agents.py`** - Auto-detects and uses vLLM or Azure based on USE_VLLM
- **`core/chat_manager.py`** - Orchestrates agent communication

### Test/Utility Files
- **`test_vllm.py`** - Test vLLM server connection
- **`test_nl2vis_vllm.py`** - Test full NL2Vis integration
- **`quick_check.py`** - Comprehensive setup verification
- **`monitor_vllm.py`** - Monitor server metrics (requires requests, torch)

### Application Entry Points
- **`run_evaluate.py`** - Run NL2Vis evaluation pipeline
- **`web_vis/app.py`** - Start Flask web interface

---

## 🔄 Usage Scenarios

### Scenario 1: Development & Testing (Local vLLM)
```bash
# 1. Activate venv
source .venv/bin/activate  # or .venv\Scripts\Activate.ps1 on Windows

# 2. Configure
vim core/vllm_config.py  # Set USE_VLLM = True

# 3. Start server (Terminal 1)
python -m core.vllm_server

# 4. Run tests/development (Terminal 2, activate venv there too)
python test_vllm.py
python run_evaluate.py
```

### Scenario 2: Production (Azure OpenAI API)
```bash
# 1. Configure
vim core/vllm_config.py  # Set USE_VLLM = False

# 2. Set Azure credentials
export AZURE_OPENAI_API_KEY="your-key"
export AZURE_OPENAI_ENDPOINT="your-endpoint"

# 3. Run directly (no vLLM server needed)
python run_evaluate.py
python web_vis/app.py
```

### Scenario 3: Switch Between Backends
```bash
# Just toggle the flag in core/vllm_config.py
USE_VLLM = True   # Use local vLLM
USE_VLLM = False  # Use Azure API

# No other code changes needed!
```

---

## ⚙️ Model Selection Guide

| Model | VRAM Needed | Use Case | Note |
|-------|-------------|----------|------|
| **SmolLM2-135M** | ~2GB | Testing, debugging | Very fast, basic quality |
| **Llama-3-8B** | ~16GB | Production | Best quality, requires license |
| **Mistral-7B** | ~14GB | Production | Good quality, open license |
| **Qwen2.5-7B** | ~14GB | Production | Strong multilingual |

### Reducing VRAM Usage
```python
# In core/vllm_config.py

# Option 1: Use quantization
VLLM_QUANTIZATION = "awq"  # 4-bit quantization (~50% less VRAM)

# Option 2: Reduce context length
VLLM_MAX_MODEL_LEN = 4096  # Smaller context window

# Option 3: Lower GPU utilization
VLLM_GPU_MEMORY_UTILIZATION = 0.75  # Use 75% instead of 90%
```

---

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port is in use
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Kill existing process
kill -9 <PID>
```

### Import errors when running vllm_server.py
```bash
# Always run from project root as a module
python -m core.vllm_server

# NOT: python core/vllm_server.py
```

### Out of memory errors
1. Use a smaller model (SmolLM2-135M for testing)
2. Enable quantization: `VLLM_QUANTIZATION = "awq"`
3. Reduce `VLLM_GPU_MEMORY_UTILIZATION` to 0.70
4. Lower `VLLM_MAX_MODEL_LEN` to 4096 or 2048

### Model download issues
```bash
# Check Hugging Face authentication
huggingface-cli whoami

# Manually download model first
python -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('meta-llama/Meta-Llama-3-8B-Instruct')"
```

### Server starts but test_vllm.py fails
```bash
# Wait longer for model to load (can take 2-3 minutes)
# Check server logs for errors

# Test manually with curl
curl http://localhost:8000/v1/models
```

---

## 🔍 Quick Verification

```bash
# 1. Check Python environment
python --version  # Should be 3.8+

# 2. Check vLLM installation
python -c "import vllm; print(vllm.__version__)"

# 3. Check GPU
nvidia-smi  # Should show GPU and CUDA version

# 4. Check configuration
python -c "from core.vllm_config import USE_VLLM, VLLM_MODEL_NAME; print(f'USE_VLLM={USE_VLLM}, Model={VLLM_MODEL_NAME}')"

# 5. Run comprehensive check
python quick_check.py
```

---

## 📊 Performance Notes

- **First request**: Slower (model initialization)
- **Subsequent requests**: Fast (~100-500 tokens/sec on good GPU)
- **Model loading time**: 30 seconds to 2 minutes depending on model size
- **Memory usage**: Primarily GPU memory, ~8-16GB for 7B models

---

## 🔗 Additional Resources

- **vLLM Documentation**: https://docs.vllm.ai/
- **Supported Models**: https://docs.vllm.ai/en/latest/models/supported_models.html
- **uv Documentation**: https://docs.astral.sh/uv/

---

## 💡 Tips

1. **Start with a small model** (SmolLM2-135M) to verify setup before using larger models
2. **Keep the vLLM server running** during development to avoid reload time
3. **Monitor GPU usage** with `nvidia-smi` or `watch -n 1 nvidia-smi`
4. **Use tmux/screen** on Linux to keep server running in background
5. **Check logs** in server terminal if anything fails

---

**Quick Start TL;DR:**
```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
python -m core.vllm_server              # Terminal 1
python test_vllm.py && python run_evaluate.py  # Terminal 2
```
