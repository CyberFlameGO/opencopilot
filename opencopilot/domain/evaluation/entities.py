from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationInput:
    query: str
    answer: str
    expected_answer: str


@dataclass(frozen=True)
class EvaluationOutput:
    evaluation: str
