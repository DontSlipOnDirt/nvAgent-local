# quick_check.py
"""Quick check script to verify vLLM setup and configuration."""

import sys
from pathlib import Path

def print_header(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

def check_imports():
    """Check if required modules can be imported."""
    print_header("Checking Imports")
    
    modules = {
        "vllm": False,
        "openai": False,
        "torch": False,
        "core.vllm_config": False,
        "core.vllm_client": False
    }
    
    for module_name in modules.keys():
        try:
            __import__(module_name)
            modules[module_name] = True
            print(f"✅ {module_name}")
        except ImportError as e:
            print(f"❌ {module_name} - {e}")
    
    return all(modules.values())

def check_config():
    """Check vLLM configuration."""
    print_header("Checking Configuration")
    
    try:
        from core.vllm_config import (
            USE_VLLM,
            VLLM_MODEL_NAME,
            VLLM_HOST,
            VLLM_PORT,
            VLLM_MAX_MODEL_LEN,
            VLLM_GPU_MEMORY_UTILIZATION
        )
        
        print(f"USE_VLLM: {USE_VLLM}")
        print(f"Model: {VLLM_MODEL_NAME}")
        print(f"Server: {VLLM_HOST}:{VLLM_PORT}")
        print(f"Max Length: {VLLM_MAX_MODEL_LEN}")
        print(f"GPU Memory: {VLLM_GPU_MEMORY_UTILIZATION}")
        
        if USE_VLLM:
            print("\n✅ vLLM is ENABLED")
        else:
            print("\n⚠️  vLLM is DISABLED (will use Azure API)")
        
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def check_gpu():
    """Check GPU availability."""
    print_header("Checking GPU")
    
    try:
        import torch
        
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            print(f"✅ CUDA available: {torch.cuda.is_available()}")
            print(f"GPU Count: {gpu_count}")
            
            for i in range(gpu_count):
                gpu_name = torch.cuda.get_device_name(i)
                gpu_memory = torch.cuda.get_device_properties(i).total_memory / 1024**3
                print(f"  GPU {i}: {gpu_name} ({gpu_memory:.1f} GB)")
            
            return True
        else:
            print("❌ CUDA not available")
            print("vLLM requires a CUDA-capable GPU")
            return False
            
    except Exception as e:
        print(f"❌ GPU check error: {e}")
        return False

def check_server():
    """Check if vLLM server is running."""
    print_header("Checking vLLM Server")
    
    try:
        import requests
        from core.vllm_config import VLLM_HOST, VLLM_PORT
        
        url = f"http://{VLLM_HOST}:{VLLM_PORT}/v1/models"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            print(f"✅ Server is running at http://{VLLM_HOST}:{VLLM_PORT}")
            models = response.json()
            print(f"Available models: {models}")
            return True
        else:
            print(f"❌ Server responded with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Server is NOT running")
        print(f"Start it with: python core/vllm_server.py")
        return False
    except ImportError:
        print("⚠️  'requests' module not installed, skipping server check")
        return None
    except Exception as e:
        print(f"❌ Server check error: {e}")
        return False

def check_integration():
    """Check if NL2Vis integration is working."""
    print_header("Checking NL2Vis Integration")
    
    try:
        from core.vllm_config import USE_VLLM
        
        if not USE_VLLM:
            print("⚠️  vLLM is disabled, skipping integration check")
            return None
        
        # Try importing agents
        from core.agents import LLM_API_FUC
        
        if LLM_API_FUC is not None:
            print("✅ LLM_API_FUC is configured")
            print(f"Function: {LLM_API_FUC.__module__}.{LLM_API_FUC.__name__}")
            
            # Check if it's using vLLM
            if "vllm" in LLM_API_FUC.__module__:
                print("✅ Using vLLM client")
                return True
            else:
                print("⚠️  Not using vLLM client (using API instead)")
                return False
        else:
            print("❌ LLM_API_FUC is None")
            return False
            
    except Exception as e:
        print(f"❌ Integration check error: {e}")
        return False

def main():
    """Run all checks."""
    print("\n" + "=" * 60)
    print("vLLM Setup Quick Check")
    print("=" * 60)
    
    results = {
        "Imports": check_imports(),
        "Configuration": check_config(),
        "GPU": check_gpu(),
        "Server": check_server(),
        "Integration": check_integration()
    }
    
    print_header("Summary")
    
    for check_name, result in results.items():
        if result is True:
            status = "✅ PASS"
        elif result is False:
            status = "❌ FAIL"
        else:
            status = "⚠️  SKIP"
        print(f"{status} - {check_name}")
    
    print("\n" + "=" * 60)
    
    # Final recommendation
    failed_checks = [name for name, result in results.items() if result is False]
    
    if not failed_checks:
        print("✅ All checks passed! You're ready to use vLLM.")
        print("\nNext steps:")
        print("1. Start vLLM server: python core/vllm_server.py")
        print("2. Test server: python test_vllm.py")
        print("3. Run NL2Vis: python run_evaluate.py")
    else:
        print(f"❌ Some checks failed: {', '.join(failed_checks)}")
        print("\nPlease fix the issues above before using vLLM.")
        print("\nYou can:")
        print("1. Install missing packages: pip install vllm")
        print("2. Start the server: python core/vllm_server.py")
        print("3. Set USE_VLLM = False to use Azure API instead")
    
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
