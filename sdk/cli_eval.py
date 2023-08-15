import json
import os
import time
from dataclasses import dataclass
from typing import Dict
from typing import List
from uuid import uuid4

import requests

from sdk import cli_validate
from sdk.utils import env_utils
from sdk.utils import print_utils
from sdk.utils import request_utils
from sdk.utils.env_utils import get_copilot_name


@dataclass(frozen=True)
class DatasetModel:
    query: str
    answer: str


def main():
    backend_url = env_utils.get_backend_url()
    if not request_utils.query(backend_url):
        print_utils.print_red("\nBackend must be running to run evaluation")
        return
    if not cli_validate.main():
        return

    copilot_name: str = get_copilot_name()
    dataset = _get_dataset(copilot_name)
    if not dataset:
        return
    print_utils.print_yellow(f"Got {len(dataset)} examples from the dataset.")

    predictions = _get_predictions(dataset, backend_url)
    evaluations = _evaluate_dataset(dataset, predictions, backend_url)
    if not evaluations:
        return

    count, score = _get_summary_evaluation(evaluations)
    print_utils.print_green(f"Evaluation score: {score}%, out of {count} evaluations.")
    _save_evaluations(dataset, predictions, evaluations, copilot_name)


def _get_dataset(copilot_name: str) -> List[DatasetModel]:
    dataset_path = f"copilots/{copilot_name}/eval_data/endtoend_human.json"
    return _dataset_from_file(dataset_path)


def _dataset_from_file(
        dataset_path: str,
        limit: int = None
) -> List[DatasetModel]:
    with open(dataset_path, "r") as f:
        dataset_dict = json.load(f)
        if not _validate_dataset(dataset_dict):
            return []
        if limit:
            dataset_dict["examples"] = dataset_dict["examples"][:limit]
    dataset: List[DatasetModel] = []
    for d in dataset_dict["examples"]:
        dataset.append(DatasetModel(
            query=d["query"],
            answer=d["answer"],
        ))
    return dataset


def _validate_dataset(dataset_dict: Dict) -> bool:
    expected_format = '{"examples": [{"query": "", "answer": ""}]}'
    if not isinstance(dataset_dict, dict) or not dataset_dict.get("examples"):
        print_utils.print_red(f'Dataset is missing "examples" object, expected file format: {expected_format}')
        return False
    for d in dataset_dict.get("examples"):
        if not d.get("query") or not d.get("answer"):
            print_utils.print_red(f'Dataset object is invalid, expected file format: {expected_format}')
            return False
    return True


def _get_predictions(
        dataset: List[DatasetModel],
        api_url: str,
) -> List[str]:
    predictions: List[str] = []
    print_utils.print_yellow("Getting LLM responses")
    for example in dataset:
        try:
            data = {"inputs": example.query}
            response = requests.post(
                f"{api_url}/v0/conversation/{str(uuid4())}", json=data
            )
            j = response.json()
            result = j["generated_text"]
            predictions.append(result)

            time.sleep(1)
        except Exception as e:
            predictions.append("UNEXPECTED_ERROR")
    return predictions


def _evaluate_dataset(
        dataset: List[DatasetModel],
        predictions: List[str],
        backend_url: str,
) -> List[str]:
    if len(dataset) != len(predictions):
        print_utils.print_red(
            "Dataset and predictions length are different, aborting.")
        return []
    evaluations: List[str] = []
    for i in range(0, len(dataset)):
        evaluations.append(
            _evaluate_single(
                dataset[i],
                predictions[i],
                backend_url
            )
        )
        time.sleep(1)
    return evaluations


def _evaluate_single(
        example: DatasetModel,
        prediction: str,
        backend_url: str
) -> str:
    try:
        data = {
            "query": example.query,
            "answer": prediction,
            "expected_answer": example.answer
        }
        response = requests.post(
            f"{backend_url}/v0/debug/evaluate", json=data
        )
        j = response.json()
        return j["evaluation"]
    except Exception as e:
        return "UNEXPECTED_ERROR"


def _get_summary_evaluation(evaluations: List[str]):
    """Roll up a list of single evaluations into a summary evaluation."""
    evaluations_count = len(evaluations)
    total_score = 0
    rubric = {"A": 1.0, "B": 0.75, "C": 0.5, "D": 0.25, "F": 0.0}
    for evaluation in evaluations:
        grade = rubric.get(evaluation)
        if grade:  # TODO - failures of grading are implicitly scored as zero
            total_score += grade
    return evaluations_count, round((total_score / evaluations_count) * 100, 4)


def _save_evaluations(
        dataset: List[DatasetModel],
        predictions: List[str],
        evaluations: List[str],
        copilot_name: str
) -> None:
    output_path = f"copilots/{copilot_name}/eval_results/endtoend_human.json"
    os.makedirs(f"copilots/{copilot_name}/eval_results/", exist_ok=True)
    summaries: List[Dict] = []
    for i, d in enumerate(dataset):
        summaries.append({
            "query": d.query,
            "answer": predictions[i],
            "expected_answer": d.answer,
            "llm_evaluation": evaluations[i],
        })
    with open(output_path, "w") as f:
        json.dump(summaries, f, indent=4)
    print_utils.print_green(f"Saved evaluation information to {output_path}. Evaluation is scored A-F with A being the best grade.")
