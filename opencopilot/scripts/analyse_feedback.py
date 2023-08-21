import json
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class UserFeedbackAnalytics:
    correctness: List[int]
    helpfulness: List[int]
    easy_to_understand: List[int]


def execute(conversations_dir="conversations") -> UserFeedbackAnalytics:
    feedbacks = _collect_feedbacks(conversations_dir)
    print("\nRaw feedbacks:")
    print(feedbacks)

    correctness = []
    helpfulness = []
    easy_to_understand = []
    for chat_feedbacks in feedbacks:
        for f in chat_feedbacks:
            if f.get("correctness"):
                correctness.append(f.get("correctness"))
            if f.get("helpfulness"):
                helpfulness.append(f.get("helpfulness"))
            if f.get("easy_to_understand"):
                easy_to_understand.append(f.get("easy_to_understand"))

    print("\nMetrics:")
    _print_metric("correctness", correctness)
    _print_metric("helpfulness", helpfulness)
    _print_metric("easy_to_understand", easy_to_understand)
    total_feedbacks = len(correctness) + len(helpfulness) + len(easy_to_understand)
    print(f"\n  total feedbacks given:", total_feedbacks)
    return UserFeedbackAnalytics(
        correctness=correctness,
        helpfulness=helpfulness,
        easy_to_understand=easy_to_understand
    )


def _print_metric(label: str, metric: List[int]) -> None:
    print(f"  {label}:")
    print(f"    len:", len(metric))
    print(f"    min:", min(metric))
    print(f"    max:", max(metric))
    print(f"    avg:", sum(metric) / len(metric))


def _collect_feedbacks(conversations_dir: str):
    pathlist = Path(conversations_dir).rglob('*.json')
    result = []
    for path in pathlist:
        feedbacks = _get_feedbacks_from_file(str(path))
        if feedbacks:
            result.append(feedbacks)
    return result


def _get_feedbacks_from_file(file_path: str):
    result = []
    data = _read_file(file_path)
    data = json.loads(data)
    for item in data:
        feedback = item.get("user_feedback")
        if feedback:
            result.append(feedback)
    return result


def _read_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


if __name__ == '__main__':
    execute()
