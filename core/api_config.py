# core/api_config.py
"""
Configuration for API (Azure OpenAI / vLLM).
Delegates to centralized config.
"""
from core.config import (
    API_KEY,
    AZURE_OPENAI_ENDPOINT,
    OPENAI_API_VERSION,
    MODEL_NAME,
    USE_VLLM
)