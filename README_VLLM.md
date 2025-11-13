# vLLM Setup Guide

## Quick Start

1. **Install vLLM:**
   ```bash
   pip install vllm
   ```

2. **Start vLLM Server:**
   
   **Windows:**
   ```bash
   start_vllm.bat
   ```
   Or:
   ```bash
   python core/vllm_server.py
   ```
   
   **Linux/Mac:**
   ```bash
   chmod +x start_vllm.sh
   ./start_vllm.sh
   ```
   Or:
   ```bash
   python3 core/vllm_server.py
   ```

3. **Run NL2Vis:**
   ```bash
   python run_evaluate.py
   ```

## Configuration

Edit `core/vllm_config.py` to:
- Toggle between API and vLLM (`USE_VLLM`)
- Change model (`VLLM_MODEL_NAME`)
- Adjust memory settings
- Modify inference parameters

## Switching Between Azure API and vLLM

To use **vLLM** (local):
```python
# core/vllm_config.py
USE_VLLM = True
```

To use **Azure OpenAI API**:
```python
# core/vllm_config.py
USE_VLLM = False
```

## Model Recommendations

| VRAM | Model | Speed |
|------|-------|-------|
| 8GB  | Llama-3-8B (with quantization) | Medium |
| 12GB | Llama-3-8B (fp16) | Fast |
| 16GB | Mistral-7B or Llama-3-13B | Fast |
| 24GB | Llama-3-70B | Very Fast |

## Available Models

Edit `VLLM_MODEL_NAME` in `core/vllm_config.py`:

```python
# Recommended for SQL/code generation
VLLM_MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"

# Alternative: Smaller, faster
VLLM_MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"

# Alternative: Better for Chinese
VLLM_MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
```

## Troubleshooting

### Server won't start

**Check GPU availability:**
```bash
nvidia-smi
```

**Solutions:**
- Reduce `VLLM_GPU_MEMORY_UTILIZATION` to 0.80 or 0.70
- Try a smaller model
- Check CUDA is installed properly

### Out of memory errors

**Solutions:**
1. Enable quantization:
   ```python
   VLLM_QUANTIZATION = "awq"
   ```

2. Reduce context length:
   ```python
   VLLM_MAX_MODEL_LEN = 4096  # Instead of 8192
   ```

3. Reduce GPU memory usage:
   ```python
   VLLM_GPU_MEMORY_UTILIZATION = 0.70
   ```

4. Use a smaller model

### Slow inference

**Check GPU utilization:**
```bash
nvidia-smi
```

**Solutions:**
- Increase `VLLM_GPU_MEMORY_UTILIZATION`
- Make sure you're using GPU (check dtype is not "cpu")
- Try different dtype: `VLLM_DTYPE = "float16"`

### Connection refused

**Make sure server is running:**
```bash
python test_vllm.py
```

If server is not running, start it:
```bash
python core/vllm_server.py
```

### Model download issues

For Llama models, you need:
1. HuggingFace account
2. Accept license at: https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct
3. Login: `huggingface-cli login`

## Testing

### Test vLLM Server Connection
```bash
python test_vllm.py
```

### Test NL2Vis Integration
```bash
python test_nl2vis_vllm.py
```

### Monitor Server
```bash
python monitor_vllm.py
```

## Performance Tips

1. **Use tensor parallelism** (if you have multiple GPUs):
   ```python
   # Add to vllm_server.py command
   --tensor-parallel-size 2
   ```

2. **Adjust batch size** for throughput:
   ```python
   VLLM_MAX_NUM_SEQS = 256
   ```

3. **Use flash attention** (automatic in vLLM 0.6+)

## Common vLLM Commands

### Start server with custom settings:
```bash
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Meta-Llama-3-8B-Instruct \
    --host localhost \
    --port 8000 \
    --max-model-len 8192 \
    --gpu-memory-utilization 0.90 \
    --dtype auto
```

### With quantization:
```bash
python -m vllm.entrypoints.openai.api_server \
    --model TheBloke/Llama-2-7B-Chat-AWQ \
    --quantization awq \
    --dtype auto
```

## File Structure

```
NL2Vis/
├── core/
│   ├── vllm_config.py      # Configuration settings
│   ├── vllm_client.py      # Client wrapper
│   ├── vllm_server.py      # Server startup script
│   ├── agents.py           # Modified to use vLLM
│   └── chat_manager.py     # Modified to use vLLM
├── web_vis/
│   └── core/
│       ├── vllm_config.py  # Config import
│       └── vllm_client.py  # Client import
├── test_vllm.py            # Server connection test
├── test_nl2vis_vllm.py     # Integration test
├── monitor_vllm.py         # Server monitor
└── start_vllm.bat          # Windows launcher
```

## Support

For vLLM issues, see:
- GitHub: https://github.com/vllm-project/vllm
- Docs: https://docs.vllm.ai/

For NL2Vis-specific integration issues, check the console output for error messages.
