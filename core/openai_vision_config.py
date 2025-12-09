# core/openai_vision_config.py
"""
Configuration for OpenAI vision model inference.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Toggle for using OpenAI vision model
USE_OPENAI_VISION = True

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_VISION_MODEL_NAME = "gpt-4o-mini"

# Inference Parameters
OPENAI_VISION_TEMPERATURE = 0.0
OPENAI_VISION_MAX_TOKENS = 1024

OPENAI_VISION_MAX_RETRIES = 10
OPENAI_VISION_TIMEOUT = 60