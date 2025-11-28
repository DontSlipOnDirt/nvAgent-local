# core/openai_vision_client.py
"""
Vision model client using OpenAI API via LangChain.
"""
from langchain_openai import ChatOpenAI
from core.openai_vision_config import (
    OPENAI_API_KEY,
    OPENAI_VISION_MODEL_NAME,
    OPENAI_VISION_TEMPERATURE,
    OPENAI_VISION_MAX_TOKENS
)

def get_vision_model():
    """Get OpenAI vision model client."""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")
        
    return ChatOpenAI(
        model=OPENAI_VISION_MODEL_NAME,
        temperature=OPENAI_VISION_TEMPERATURE,
        max_tokens=OPENAI_VISION_MAX_TOKENS,
        api_key=OPENAI_API_KEY
    )
