from opencopilot.src.eval.entities import RetrievalExample
from opencopilot.src.eval.entities import RetrievalResult
from opencopilot.src.eval.entities import RetrievalSingleEvaluation
from opencopilot.src.eval.retrieval import evaluate_retrieval_single
from opencopilot.src.eval.retrieval import get_confusion_matrix


def test_get_confusion_matrix_one_relevant():
    ground_truth = RetrievalExample(
        query="mock query",
        documents=["A"]
    )
    predicted = RetrievalResult(
        documents=[]
    )
    result = get_confusion_matrix(ground_truth, predicted)
    expected = ([], [], ["A"])  # tp, fp, fn
    assert result == expected


def test_get_confusion_matrix_one_predicted():
    ground_truth = RetrievalExample(
        query="mock query",
        documents=[]
    )
    predicted = RetrievalResult(
        documents=["A"]
    )
    result = get_confusion_matrix(ground_truth, predicted)
    expected = ([], ["A"], [])  # tp, fp, fn
    assert result == expected


def test_get_confusion_matrix_all_empty():
    ground_truth = RetrievalExample(
        query="mock query",
        documents=[]
    )
    predicted = RetrievalResult(
        documents=[]
    )
    result = get_confusion_matrix(ground_truth, predicted)
    expected = ([], [], [])  # tp, fp, fn
    assert result == expected


def test_get_confusion_matrix_all_same():
    ground_truth = RetrievalExample(
        query="mock query",
        documents=["A", "B"]
    )
    predicted = RetrievalResult(
        documents=["A", "B"]
    )
    result = get_confusion_matrix(ground_truth, predicted)
    expected = (["A", "B"], [], [])  # tp, fp, fn
    assert result == expected


def test_get_confusion_matrix_complex():
    ground_truth = RetrievalExample(
        query="mock query",
        documents=["A", "B", "C"]
    )
    predicted = RetrievalResult(
        documents=["C", "D", "E"]
    )
    result = get_confusion_matrix(ground_truth, predicted)
    expected = (["C"], ["D", "E"], ["A", "B"])  # tp, fp, fn
    assert result == expected


def test_evaluate_retrieval_single_nothing_relevant():
    ground_truth = RetrievalExample(
        query="mock query",
        documents=[]
    )
    predicted = RetrievalResult(
        documents=["A", "B"]
    )
    result = evaluate_retrieval_single(ground_truth, predicted)
    expected = RetrievalSingleEvaluation(
        example=ground_truth,
        result=predicted,
        true_positives=[],
        false_positives=["A", "B"],
        false_negatives=[],
        precision=0.0,
        recall=1.0
    )
    assert result == expected


def test_evaluate_retrieval_single_nothing_predicted():
    ground_truth = RetrievalExample(
        query="mock query",
        documents=["A", "B"]
    )
    predicted = RetrievalResult(
        documents=[]
    )
    result = evaluate_retrieval_single(ground_truth, predicted)
    expected = RetrievalSingleEvaluation(
        example=ground_truth,
        result=predicted,
        true_positives=[],
        false_positives=[],
        false_negatives=["A", "B"],
        precision=1.0,
        recall=0.0
    )
    assert result == expected
