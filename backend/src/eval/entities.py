from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List, TypeAlias

# Define Document ID explicitly; it is currently just a URL string, but may in future be something more structured.
DocumentID: TypeAlias = str


@dataclass_json
@dataclass(frozen=True)
class RetrievalExample:
    # User query
    query: str
    # Relevant documents
    documents: List[DocumentID]


@dataclass_json
@dataclass(frozen=True)
class RetrievalDataset:
    examples: List[RetrievalExample]


@dataclass_json
@dataclass(frozen=True)
class RetrievalResult:
    # Returned documents
    documents: List[DocumentID]


@dataclass_json
@dataclass(frozen=True)
class RetrievalSingleEvaluation:
    example: RetrievalExample
    result: RetrievalResult
    true_positives: List[DocumentID]
    false_positives: List[DocumentID]
    false_negatives: List[DocumentID]
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
    documents: List[DocumentID]

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