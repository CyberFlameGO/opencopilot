from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class RetrievalExample:
    # User query
    query: str
    # Relevant documents
    documents: List[str]


@dataclass_json
@dataclass(frozen=True)
class RetrievalDataset:
    examples: List[RetrievalExample]


@dataclass_json
@dataclass(frozen=True)
class RetrievalResult:
    # Returned documents
    documents: List[str]


@dataclass_json
@dataclass(frozen=True)
class RetrievalSingleEvaluation:
    example: RetrievalExample
    result: RetrievalResult
    true_positives: List[str]
    false_positives: List[str]
    false_negatives: List[str]
    precision: float
    recall: float


@dataclass_json
@dataclass(frozen=True)
class RetrievalSummaryEvaluation:
    single_evaluations: List[RetrievalSingleEvaluation]
    average_precision: float
    average_recall: float


@dataclass_json
@dataclass(frozen=True)
class EndToEndExample:
    query: str
    answer: str


@dataclass_json
@dataclass(frozen=True)
class EndToEndResult:
    answer: str
    documents: List[str]


@dataclass_json
@dataclass(frozen=True)
class EndToEndDataset:
    examples: List[EndToEndExample]


@dataclass_json
@dataclass(frozen=True)
class EndToEndSingleEvaluation:
    evaluation: str


@dataclass_json
@dataclass(frozen=True)
class EndToEndSummaryEvaluation:
    single_evaluations: List[EndToEndSingleEvaluation]
    evaluations_count: int
    evaluations_score: float
