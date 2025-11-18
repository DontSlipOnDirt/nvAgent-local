import json
from datetime import datetime
from pathlib import Path
from typing import Tuple, Optional

from core.chat_manager import ChatManager
from viseval import Dataset, Evaluator


def setup_vision_model() -> Tuple[Optional[object], Optional[str]]:
    """
    Configure and initialize the vision model.
    
    Returns:
        Tuple of (vision_model, vision_model_name)
    """
    try:
        from core.vision_vllm_config import USE_VISION_VLLM, VISION_VLLM_MODEL_NAME
        from core.vision_vllm_client import get_vision_model
        
        if USE_VISION_VLLM:
            print("Using local vision vLLM model...")
            return get_vision_model(), VISION_VLLM_MODEL_NAME
        else:
            print("USE_VISION_VLLM=False, vision model disabled")
            return None, None
    except ImportError:
        print("Vision vLLM not configured, vision model disabled")
        return None, None


def get_text_model_name() -> str:
    """
    Get the name of the text model being used.
    
    Returns:
        Model name string
    """
    try:
        from core.vllm_config import USE_VLLM, VLLM_MODEL_NAME
        if USE_VLLM:
            return VLLM_MODEL_NAME
        else:
            return "Azure OpenAI API"
    except ImportError:
        return "Azure OpenAI API"


def run_evaluation(agent, dataset, evaluator, config: dict):
    """
    Execute the evaluation process.
    
    Args:
        agent: ChatManager instance
        dataset: Dataset instance
        evaluator: Evaluator instance
        config: Evaluation configuration dict
        
    Returns:
        EvaluationResult object
    """
    return evaluator.evaluate(agent, dataset, config)


def save_results(result, text_model_name: str, vision_model_name: Optional[str], 
                 library: str, table_type: str):
    """
    Save evaluation results to CSV and JSON files.
    
    Args:
        result: EvaluationResult object
        text_model_name: Name of text model used
        vision_model_name: Name of vision model used (or None)
        library: Visualization library used
        table_type: single, multiple, or both
        
    Returns:
        Tuple of (detailed_csv_path, scores_json_path)
    """
    # Create unique timestamp for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Extract model names for filename (remove path prefix)
    text_model_short = text_model_name.split('/')[-1] if '/' in text_model_name else text_model_name
    vision_model_short = vision_model_name.split('/')[-1] if vision_model_name and '/' in vision_model_name else (vision_model_name or 'NoVision')
    
    # Extract dataset size
    dataset_size = len(json.load(open('visEval_dataset/visEval.json'))) if table_type == 'all' else len(json.load(open('visEval_dataset/visEval_' + table_type + '.json')))

    # Create results directory
    results_dir = Path("results")
    run_folder_name = f"{timestamp}_{text_model_short}_{vision_model_short}"
    run_folder = results_dir / run_folder_name
    run_folder.mkdir(parents=True, exist_ok=True)
    
    # Create unique filenames
    detailed_csv_path = run_folder / "detailed_results.csv"
    scores_json_path = run_folder / "scores.json"
    
    # Prepare metadata
    run_metadata = {
        "text_model": text_model_name,
        "vision_model": vision_model_name,
        "timestamp": datetime.now().isoformat(),
        "library": library,
        "table_type": table_type,
        "dataset_size": dataset_size
    }
    
    # Save detailed results with model info
    detailed_df = result.detail_records()
    detailed_df['text_model'] = text_model_name
    detailed_df['vision_model'] = vision_model_name if vision_model_name else 'None'
    detailed_df.to_csv(detailed_csv_path, index=False)
    
    # Save scores with metadata
    score = result.score()
    final_output = {
        "metadata": run_metadata,
        "scores": score
    }
    with open(scores_json_path, "w") as f:
        json.dump(final_output, f, indent=2)
    
    return detailed_csv_path, scores_json_path, score


def print_results(text_model_name: str, vision_model_name: Optional[str], 
                  score: dict, detailed_csv_path: Path, scores_json_path: Path,
                  log_folder: Path):
    """
    Print evaluation results to console.
    
    Args:
        text_model_name: Name of text model used
        vision_model_name: Name of vision model used (or None)
        score: Dictionary of evaluation scores
        detailed_csv_path: Path to detailed CSV file
        scores_json_path: Path to scores JSON file
        log_folder: Path to evaluation log folder
    """
    print("\n" + "="*60)
    print("EVALUATION COMPLETE")
    print("="*60)
    print(f"Text Model: {text_model_name}")
    print(f"Vision Model: {vision_model_name or 'None'}")
    print("="*60)
    print(f"\nFinal Scores:")
    for metric, value in score.items():
        print(f"  {metric}: {value:.4f}" if isinstance(value, float) else f"  {metric}: {value}")
    
    print(f"\n✅ Results saved to:")
    print(f"   - {detailed_csv_path}")
    print(f"   - {scores_json_path}")
    print(f"\n📁 Evaluation cache: {log_folder / 'evaluation.log'}")
    print("="*60)


def main():
    """Main evaluation pipeline."""
    # Configuration
    folder = "visEval_dataset"
    table_type = "all"
    library = 'matplotlib'
    log_folder = Path("evaluate_logs")
    
    # Setup models
    vision_model, vision_model_name = setup_vision_model()
    text_model_name = get_text_model_name()
    
    # Initialize components
    dataset = Dataset(Path(folder))
    agent = ChatManager(data_path=folder, log_path="./agent_logs.txt")
    evaluator = Evaluator(webdriver_path=None, vision_model=vision_model)
    
    # Run evaluation
    config = {"library": library, "logs": log_folder}
    result = run_evaluation(agent, dataset, evaluator, config)
    
    # Save and display results
    detailed_csv_path, scores_json_path, score = save_results(
        # result, text_model_name, vision_model_name, library, len(dataset.benchmark)
        result, text_model_name, vision_model_name, library, table_type, 
    )
    print_results(text_model_name, vision_model_name, score, 
                  detailed_csv_path, scores_json_path, log_folder)


if __name__ == "__main__":
    main()
