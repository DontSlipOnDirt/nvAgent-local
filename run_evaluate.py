import argparse
from pathlib import Path
import os
from core.chat_manager import ChatManager
from viseval import Dataset, Evaluator
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

def _main():
    # load_dotenv()  # Load environment variables from .env file if present

    # config vision model
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
    # webdriver = Path("C:\Program Files\Google\Chrome\Application\chromedriver.exe") # set your chromedriver path here
    log_folder = Path("evaluate_logs")

    # config dataset
    dataset = Dataset(Path(folder))
    # config agent # API config in api_config.py
    agent = ChatManager(data_path=folder,log_path="./test_logs.txt",)

    # config evaluator
    evaluator = Evaluator(webdriver_path=None, vision_model=None)
    # evaluator = Evaluator()
    # evaluate agent
    config = {"library": library, "logs": log_folder}
    result = evaluator.evaluate(agent, dataset, config)
    print(result)
    score = result.score()
    print(f"Score: {score}")


if __name__ == "__main__":
    _main()
