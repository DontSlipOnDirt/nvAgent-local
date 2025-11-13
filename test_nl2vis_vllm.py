# test_nl2vis_vllm.py
"""Test NL2Vis with vLLM backend."""

import sys
from pathlib import Path

# Ensure vLLM is enabled
sys.path.insert(0, str(Path(__file__).parent / "core"))
from core.vllm_config import USE_VLLM

print(f"USE_VLLM: {USE_VLLM}")

if not USE_VLLM:
    print("Warning: vLLM not enabled. Edit core/vllm_config.py and set USE_VLLM=True")
    sys.exit(1)

# Test vLLM client
from core.vllm_client import safe_call_llm

print("\n" + "=" * 60)
print("Testing vLLM Client Integration")
print("=" * 60)

try:
    response = safe_call_llm("Hello! Please respond with a short greeting.")
    print(f"\n✅ Success! Response:\n{response}")
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nMake sure vLLM server is running!")
    sys.exit(1)

print("\n" + "=" * 60)
print("Testing with Agent Import")
print("=" * 60)

from core.agents import LLM_API_FUC

try:
    response2 = LLM_API_FUC("What is data visualization? Answer in one sentence.")
    print(f"\n✅ Agent integration working! Response:\n{response2}")
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ All tests passed! vLLM is properly integrated.")
print("=" * 60)
