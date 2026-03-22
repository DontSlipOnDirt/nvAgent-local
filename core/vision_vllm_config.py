# core/vision_vllm_config.py
"""
Configuration for local vision model inference via vLLM.
Separate from text model to allow different configurations.
"""

# Toggle for using local vision model
USE_VISION_VLLM = True  # Set to True when server is running

# Toggle for Visual Feedback Agent (Reviewer)
# Set to False to disable the agent loop intervention, while keeping vision for evaluation metrics
ENABLE_REVIEWER_AGENT = True

# Vision vLLM Server Configuration
VISION_VLLM_HOST = "localhost"
VISION_VLLM_PORT = 8001  # Different port from text model (8000)
VISION_VLLM_BASE_URL = f"http://{VISION_VLLM_HOST}:{VISION_VLLM_PORT}/v1"

# Vision Model Configuration
# Recommended models for vision tasks:
# VISION_VLLM_MODEL_NAME = "Qwen/Qwen2-VL-7B-Instruct"  # Best for general vision
# VISION_VLLM_MODEL_NAME = "Qwen/Qwen2-VL-7B-Instruct-AWQ"  # 4-bit quantized, saves memory
# VISION_VLLM_MODEL_NAME = "microsoft/Phi-3-vision-128k-instruct"  # Smaller, faster
VISION_VLLM_MODEL_NAME = "Qwen/Qwen2-VL-7B-Instruct-AWQ"

# Inference Parameters
VISION_VLLM_MAX_MODEL_LEN = 8192  # Vision models need less context
VISION_VLLM_MAX_TOKENS = 512      # Short responses for readability scores
VISION_VLLM_TEMPERATURE = 0.0     # Deterministic for consistent scoring
VISION_VLLM_GPU_MEMORY_UTILIZATION = 0.40  # Share GPU with text model

# Quantization (for lower VRAM)
VISION_VLLM_QUANTIZATION = "awq"  # Use AWQ for quantized models, None for full precision
# If using non-AWQ model, set to None

# dtype configuration
VISION_VLLM_DTYPE = "auto"  # Options: "auto", "float16", "bfloat16"
