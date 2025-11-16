import argparse
from pathlib import Path
import os
from core.chat_manager import ChatManager
from viseval import Dataset, Evaluator
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

def _main():
    # config vision model
    # Option 1: Use local vision vLLM
    try:
        from core.vision_vllm_config import USE_VISION_VLLM
        from core.vision_vllm_client import get_vision_model
        
        if USE_VISION_VLLM:
            print("Using local vision vLLM model...")
            vision_model = get_vision_model()
        else:
            print("USE_VISION_VLLM=False, vision model disabled")
            vision_model = None
    except ImportError:
        print("Vision vLLM not configured, vision model disabled")
        vision_model = None
    
    # Option 2: Use GPT-4o-mini API
    # load_dotenv()  # Load environment variables from .env file
    # vision_model = ChatOpenAI(
    #     api_key=os.getenv("OPENAI_API_KEY"),
    #     base_url=os.getenv("OPENAI_API_BASE"),
    #     model_name="gpt-4o-mini",
    #     max_retries=999,
    #     temperature=0.0,
    #     request_timeout=20,
    #     max_tokens=4096,
    # )

    folder = "visEval_dataset"
    library = 'matplotlib'
    # webdriver = Path("C:\Program Files\Google\Chrome\Application\chromedriver.exe") # set your chromedriver path here for layout check
    log_folder = Path("evaluate_logs")

    # config dataset
    dataset = Dataset(Path(folder))
    # config agent # API config in api_config.py
    agent = ChatManager(data_path=folder, log_path=str("agent_logs.txt"))

    # config evaluator
    evaluator = Evaluator(webdriver_path=None, vision_model=vision_model)
    # evaluate agent
    config = {"library": library, "logs": log_folder}
    result = evaluator.evaluate(agent, dataset, config)
    
    # Print results
    print("\n" + "="*60)
    print("EVALUATION COMPLETE")
    print("="*60)
    print(result)
    score = result.score()
    print(f"\nFinal Scores:\n{score}")
    
    # Save results to files
    import json
    result.detail_records().to_csv(log_folder / "detailed_results.csv", index=False)
    with open(log_folder / "final_scores.json", "w") as f:
        json.dump(score, f, indent=2)
    
    print(f"\n✅ Results saved to:")
    print(f"   - {log_folder / 'detailed_results.csv'}")
    print(f"   - {log_folder / 'final_scores.json'}")
    print("="*60)


if __name__ == "__main__":
    _main()
