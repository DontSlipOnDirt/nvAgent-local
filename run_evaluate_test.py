"""
Run evaluation on a small subset for testing.
Usage: python run_evaluate_test.py [num_samples]
Example: python run_evaluate_test.py 50
"""
import sys
from pathlib import Path
from core.chat_manager import ChatManager
from viseval import Dataset, Evaluator
from run_evaluate import (
    setup_vision_model,
    get_text_model_name,
    run_evaluation,
    save_results,
    print_results
)


def main():
    """Run evaluation on a small subset."""
    
    # Get number of samples from command line
    num_samples = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    
    # Configuration
    folder = "visEval_dataset"
    library = 'matplotlib'
    log_folder = Path(f"evaluate_logs_test_{num_samples}")
    
    print(f"\n{'='*60}")
    print(f"Running TEST evaluation on {num_samples} samples")
    print(f"{'='*60}\n")
    
    # Setup models
    vision_model, vision_model_name = setup_vision_model()
    text_model_name = get_text_model_name()
    
    # Initialize components
    dataset = Dataset(Path(folder))
    
    # LIMIT THE DATASET - take only first N samples
    import itertools
    dataset.benchmark = itertools.islice(dataset.benchmark, num_samples)
    
    agent = ChatManager(data_path=folder, log_path=f"./agent_logs_test_{num_samples}.txt")
    evaluator = Evaluator(webdriver_path=None, vision_model=vision_model)
    
    # Run evaluation
    config = {"library": library, "logs": log_folder}
    result = run_evaluation(agent, dataset, evaluator, config)
    
    # Save and display results
    detailed_csv_path, scores_json_path, score = save_results(
        result, text_model_name, vision_model_name, library, "all"
    )
    print_results(text_model_name, vision_model_name, score, 
                  detailed_csv_path, scores_json_path, log_folder)
    
    print(f"\n{'='*60}")
    print(f"TEST evaluation complete! ({num_samples} samples)")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
