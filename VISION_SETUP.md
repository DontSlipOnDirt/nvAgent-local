# Vision Model Setup and Usage

## Quick Start

### 1. Start Vision vLLM Server
```bash
# Terminal 1 - Text model for agents (port 8000)
python -m core.vllm_server

# Terminal 2 - Vision model for readability scoring (port 8001)
python -m core.vision_vllm_server
```

### 2. Run Evaluation
```bash
# Terminal 3 - Run evaluation with both models
python run_evaluate.py
```

## Configuration

### Vision Model Settings (`core/vision_vllm_config.py`)

```python
USE_VISION_VLLM = True  # Toggle local vision model

# Model choice (pick one):
VISION_VLLM_MODEL_NAME = "Qwen/Qwen2-VL-7B-Instruct-AWQ"  # Recommended (4-bit, ~3.5GB)
# VISION_VLLM_MODEL_NAME = "Qwen/Qwen2-VL-7B-Instruct"    # Full precision (~14GB)
# VISION_VLLM_MODEL_NAME = "microsoft/Phi-3-vision-128k-instruct"  # Smaller alternative

VISION_VLLM_PORT = 8001  # Different from text model (8000)
VISION_VLLM_GPU_MEMORY_UTILIZATION = 0.40  # Share GPU with text model
```

## Memory Requirements

### With AWQ Quantization (Recommended)
- Text model (Qwen2.5-7B-AWQ): ~3.5GB
- Vision model (Qwen2-VL-7B-AWQ): ~3.5GB
- **Total**: ~7GB (fits comfortably in 20GB)

### Without Quantization
- Text model (Qwen2.5-7B): ~14GB
- Vision model (Qwen2-VL-7B): ~14GB
- **Total**: ~28GB (won't fit in 20GB)

**Solution**: Use quantized models or run sequentially

## Running Both Models Simultaneously

### Option 1: Both Quantized (Recommended)
```python
# core/vllm_config.py
VLLM_MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct-AWQ"
VLLM_QUANTIZATION = "awq"
VLLM_GPU_MEMORY_UTILIZATION = 0.50

# core/vision_vllm_config.py
VISION_VLLM_MODEL_NAME = "Qwen/Qwen2-VL-7B-Instruct-AWQ"
VISION_VLLM_QUANTIZATION = "awq"
VISION_VLLM_GPU_MEMORY_UTILIZATION = 0.40
```

### Option 2: Sequential (Full Precision)
Run text model first, then stop it and run vision model for readability scoring.

## Testing

### Test Vision Server
```bash
# Start vision server
python -m core.vision_vllm_server

# In another terminal, test the client
python -m core.vision_vllm_client
```

### Test Full Pipeline
```bash
# Start both servers
python -m core.vllm_server          # Terminal 1
python -m core.vision_vllm_server   # Terminal 2

# Run test suite
python test_suite.py --all          # Terminal 3
```

## What Gets Evaluated

With vision model enabled:
- ✅ Invalid Rate (code execution)
- ✅ Illegal Rate (chart type, data correctness)
- ✅ Pass Rate (valid + legal)
- ✅ **Scale and Ticks Check** (vision model)
- ✅ **Readability Score** (vision model, 1-5)
- ✅ Quality Score (combines all above)

Without vision model:
- ✅ Invalid, Illegal, Pass rates still work
- ❌ Readability and Quality scores unavailable

## Troubleshooting

### Vision server won't start
```bash
# Check vLLM version supports vision models
pip show vllm  # Should be >= 0.4.0

# Install vision dependencies
pip install pillow
```

### Out of memory
```bash
# Use smaller memory allocation
VISION_VLLM_GPU_MEMORY_UTILIZATION = 0.30

# Or use quantized model
VISION_VLLM_MODEL_NAME = "Qwen/Qwen2-VL-7B-Instruct-AWQ"
```

### Vision model not being used
```bash
# Check configuration
python -c "from core.vision_vllm_config import USE_VISION_VLLM; print(f'USE_VISION_VLLM={USE_VISION_VLLM}')"

# Verify server is running
curl http://localhost:8001/v1/models
```

## Model Comparison

| Model | Size | VRAM (FP16) | VRAM (AWQ) | Quality | Speed |
|-------|------|-------------|------------|---------|-------|
| Qwen2-VL-7B | 7B | ~14GB | ~3.5GB | Best | Medium |
| Phi-3-Vision | 4B | ~8GB | ~2GB | Good | Fast |
| MiniCPM-V-2.6 | 8B | ~16GB | ~4GB | Good | Medium |

## Next Steps

1. Download AWQ quantized models for both text and vision
2. Start both vLLM servers
3. Run evaluation on small subset (100 samples)
4. Compare results with paper's Qwen2.5-7B baseline
5. Full evaluation on 1,150 samples
