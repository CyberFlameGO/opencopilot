import json
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class UserFeedbackResult:
    conversation_id: str
    prompt: str
    response: str
    correctness: int
    helpfulness: int
    easy_to_understand: int
    free_form_feedback: str


def execute(conversations_dir="conversations") -> List[UserFeedbackResult]:
    result = []
    pathlist = Path(conversations_dir).rglob('*.json')
    for path in pathlist:
        feedbacks = _get_feedbacks_from_file(str(path))
        if feedbacks:
            result += feedbacks
    return result


def _get_feedbacks_from_file(file_path: str):
    result = []
    data = _read_file(file_path)
    data = json.loads(data)
    for item in data:
        feedback = item.get("user_feedback")
        if feedback:
            result.append(UserFeedbackResult(
                conversation_id=file_path.split("/")[-1].replace(".json", ""),
                prompt=item.get("prompt"),
                response=item.get("response"),
                correctness=feedback.get("correctness"),
                helpfulness=feedback.get("helpfulness"),
                easy_to_understand=feedback.get("easy_to_understand"),
                free_form_feedback=feedback.get("free_form_feedback"),
            ))
    return result


def _read_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


if __name__ == '__main__':
    all_feedbacks = execute()
    for f in all_feedbacks:
        print("\n\nFeedback:")
        print(f)
