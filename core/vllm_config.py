# core/vllm_config.py
"""
Configuration for local vLLM inference.
"""

# Toggle between Azure API and local vLLM
USE_VLLM = True  # Set to False to use Azure API

# vLLM Server Configuration
VLLM_HOST = "localhost"
VLLM_PORT = 8000
VLLM_BASE_URL = f"http://{VLLM_HOST}:{VLLM_PORT}/v1"

# Model Configuration
# VLLM_MODEL_NAME = "HuggingFaceTB/SmolLM2-135M-Instruct"
# VLLM_MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"
# VLLM_MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"
# VLLM_MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct-AWQ"  # 4-bit quantized version

# actually used models
# VLLM_MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
VLLM_MODEL_NAME = "Qwen/Qwen2.5-Coder-7B-Instruct"
# VLLM_MODEL_NAME = "Qwen/Qwen2.5-Coder-14B-Instruct-AWQ"

# VLLM_MODEL_NAME = "Qwen/Qwen2.5-Coder-32B-Instruct-AWQ"
# VLLM_MODEL_NAME = "Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8"

# Inference Parameters, optimized for H100 with 20GB MiG slice
VLLM_MAX_MODEL_LEN = 8192  # Maximum context length
VLLM_MAX_TOKENS = 2048     # Maximum tokens to generate
VLLM_TEMPERATURE = 0.0     # Deterministic output
VLLM_GPU_MEMORY_UTILIZATION = 0.90  # Percentage of GPU usage

# Quantization (for lower VRAM)
VLLM_QUANTIZATION = None  # Options: None, "awq", "gptq", "squeezellm"
# Set to "awq" for 4-bit quantization if memory constrained

# dtype configuration
VLLM_DTYPE = "auto"  # Options: "auto", "float16", "bfloat16"
